import os
import re
import json
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils import six
from waliki.models import Page
from waliki import settings
from sh import git, ErrorReturnCode


git = git.bake("--no-pager")


class Git(object):
    __shared_state = {}     # it's a Borg

    def __init__(self):
        self.__dict__ = self.__shared_state
        from waliki.settings import WALIKI_DATA_DIR
        self.content_dir = WALIKI_DATA_DIR
        os.chdir(self.content_dir)
        if not os.path.isdir(os.path.join(self.content_dir, '.git')):
            git.init()
            git.config("user.email", settings.WALIKI_COMMITTER_EMAIL)
            git.config("user.name", settings.WALIKI_COMMITTER_NAME)

        self.git = git

    def commit(self, page, message='', author=None, parent=None):
        path = page.path
        kwargs = {}
        if isinstance(author, User) and author.is_authenticated():
            kwargs['author'] = u"%s <%s>" % (author.get_full_name() or author.username, author.email)
        elif isinstance(author, six.string_types):
            kwargs['author'] = author

        try:
            there_were_changes = parent and parent != self.last_version(page)
            status = git.status('--porcelain', path).stdout.decode('utf8')[:2]
            if parent and status != "UU":
                git.stash()
                git.checkout('--detach', parent)
                try:
                    git.stash('pop')
                except:
                    git.checkout('--theirs', path)

            if status == 'UU':
                # See http://stackoverflow.com/a/8062976/811740
                kwargs['i'] = True

            git.add(path)
            git.commit(path, allow_empty_message=True, m=message, **kwargs)
            last = self.last_version(page)
            if parent and status != "UU":
                git.checkout('master')
                git.merge(last)
        except ErrorReturnCode as e:
            # TODO: make this more robust!
            error = e.stdout.decode('utf8')
            if 'CONFLICT' in error:
                # For '-i' attribute see http://stackoverflow.com/q/5827944/811740
                git.commit(path, allow_empty_message=True, m=_('Merged with conflict'), i=True, **kwargs)
                raise Page.EditionConflict(_('Automatic merge failed. Please, fix the conflict and save the page.'))
            else:
                raise
        return there_were_changes


    def history(self, page):
        GIT_COMMIT_FIELDS = ['commit', 'author', 'date', 'date_relative', 'message']
        GIT_LOG_FORMAT = '%x1f'.join(['%h', '%an', '%ad', '%ar', '%s']) + '%x1e'
        output = git.log('--format=%s' % GIT_LOG_FORMAT, '--follow', '-z', '--shortstat', page.abspath)
        output = output.split('\n')
        history = []
        for line in output:
            if '\x1f' in line:
                log = line.strip('\x1e\x00').split('\x1f')
                history.append(dict(zip(GIT_COMMIT_FIELDS, log)))
            else:
                insertion = re.match(r'.* (\d+) insertion', line)
                deletion = re.match(r'.* (\d+) deletion', line)
                history[-1]['insertion'] = int(insertion.group(1)) if insertion else 0
                history[-1]['deletion'] = int(deletion.group(1)) if deletion else 0

        max_changes = float(max([(v['insertion'] + v['deletion']) for v in history])) or 1.0
        for v in history:
            v.update({'insertion_relative': str((v['insertion'] / max_changes) * 100),
                      'deletion_relative': str((v['deletion'] / max_changes) * 100)})
        return history

    def version(self, page, version):
        try:
            return git.show('%s:%s' % (version, page.path)).stdout.decode('utf8')
        except:
            return ''

    def last_version(self, page):
        try:
            return six.text_type(git.log("--pretty=format:%h", "-n 1", page.path))
        except ErrorReturnCode:
            return None

    def whatchanged(self, skip=0, max_count=None):
        GIT_LOG_FORMAT = '%x1f'.join(['%an', '%ae', '%h', '%s', '%ar'])
        pages = []

        args = ["--pretty=format:%s" % GIT_LOG_FORMAT, '--skip=%d' % skip]
        if max_count:
            args.append('--max-count=%d' % max_count)
        raw_log = git.whatchanged(*args).stdout.decode('utf8')
        logs = re.findall(r'((.*)\x1f(.*)\x1f(.*)\x1f(.*)\x1f(.*))?\n:.*\t(.*)', raw_log, flags=re.MULTILINE | re.UNICODE)
        for log in logs:
            if log[0]:
                log = list(log[1:])
                log[-1] = [log[-1]]
                pages.append(list(log))
            else:
                pages[-1][-1].append(log[-1])
        return pages

    def pull(self, remote):
        log = git.pull('-s', 'recursive', '-X', 'ours', remote, 'HEAD').stdout.decode('utf8')
        return log

    def diff(self, page, new, old):
        return git.diff('--no-color', new, old, '--', page.path).stdout.decode('utf8')

    def total_commits(self, to='HEAD', page=None):
        args = ['rev-list', to, '--count']
        if page:
            args += ['--', page.path]
        return git(*args).stdout.decode('utf8')[:-1]

    def mv(self, page, old_path, author, message):
        status = git.status('--porcelain', old_path).stdout.decode('utf8')[1:2]
        if status == 'D':
            git.rm(old_path)
        self.commit(page, author=author, message=message)
