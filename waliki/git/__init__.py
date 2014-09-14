import os
import re
import json
from django.contrib.auth.models import User
from django.utils import six
from sh import git

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
            self.commit('.', 'initial commit')

    def commit(self, pathspec, message='', author=None):
        git.add(pathspec)
        kwargs = {}
        if isinstance(author, User) and author.is_authenticated():
            kwargs['author'] = "% <%s>" % (author.get_full_name() or author.username)
        elif isinstance(author, six.string_types):
            kwargs['author'] = author
        git.commit(m=message or 'Update', **kwargs)

    def history(self, page):
        data = [("commit", "%h"),
                ("author", "%an"),
                ("date", "%ad"),
                ("date_relative", "%ar"),
                ("message", "%s")]
        format = "{%s}" % ','.join([""" \"%s\": \"%s\" """ % item for item in data])
        output = git.log('--format=%s' % format, '-z', '--shortstat', page.path)
        output = output.replace('\x00', '').split('\n')[:-1]
        history = []
        for line in output:
            if line.startswith('{'):
                history.append(json.loads(line))
            else:
                insertion = re.match(r'.* (\d+) insertion', line)
                deletion = re.match(r'.* (\d+) deletion', line)
                history[-1]['insertion'] = int(insertion.group(1)) if insertion else 0
                history[-1]['deletion'] = int(deletion.group(1)) if deletion else 0

        max_changes = max([(v['insertion'] + v['deletion']) for v in history]) or 1
        for v in history:
            v.update({'insertion_relative': (v['insertion'] / max_changes) * 100,
                      'deletion_relative': (v['deletion'] / max_changes) * 100})
        return history

    def version(self, page, version):
        try:
            return six.text_type(git.show('%s:%s' % (version, page.path)))
        except:
            return ''