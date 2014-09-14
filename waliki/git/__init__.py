import os
from django.contrib.auth.models import User
from django.utils import six
from sh import git


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

        git.commit(m=message or 'Update' , **kwargs)