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
                raise Page.EditionConflict(_('Automatic merge failed. Please, fix the conflict and save the page.'))
            else:
                raise
        return there_were_changes


    def history(self, page):
        data = [("commit", "%h"),
                ("author", "%an"),
                ("date", "%ad"),
                ("date_relative", "%ar"),
                ("message", "%s")]
        format = "{%s}" % ','.join([""" \"%s\": \"%s\" """ % item for item in data])
        output = git.log('--format=%s' % format, '-z', '--shortstat', page.abspath)
        output = output.replace('\x00', '').replace('}{', '}\n\n{').split('\n')[:-1]
        history = []
        for line in output:
            if line.startswith('{'):
                history.append(json.loads(line))
            else:
                insertion = re.match(r'.* (\d+) insertion', line)
                deletion = re.match(r'.* (\d+) deletion', line)
                history[-1]['insertion'] = int(insertion.group(1)) if insertion else 0
                history[-1]['deletion'] = int(deletion.group(1)) if deletion else 0

        max_changes = float(max([(v['insertion'] + v['deletion']) for v in history])) or 1.0
        for v in history:
            v.update({'insertion_relative': (v['insertion'] / max_changes) * 100,
                      'deletion_relative': (v['deletion'] / max_changes) * 100})
        return history

    def version(self, page, version):
        try:
            return six.text_type(git.show('%s:%s' % (version, page.path)))
        except:
            return ''

    def last_version(self, page):
        try:
            return six.text_type(git.log("--pretty=format:%h", "-n 1", page.path))
        except ErrorReturnCode:
            return None

    def whatchanged(self):
        pages = []
        log = git.whatchanged("--pretty=format:%an//%ae//%h//%s//%ar").stdout.decode('utf8')
        logs = re.findall(r'((.*)\/\/(.*)//(.*)//(.*)//(.*))?\n:.*\t(.*)', log, flags=re.MULTILINE)
        for log in logs:
            if log[0]:
                log = list(log[1:])
                log[-1] = [log[-1]]
                pages.append(list(log))
            else:
                pages[-1].append(log[-1])
        return pages