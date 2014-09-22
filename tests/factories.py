import factory
from django.contrib.auth.models import User, Group, Permission
from waliki.models import ACLRule


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: u'user{0}'.format(n))
    password = 'pass'
    email = factory.LazyAttribute(lambda o: '%s@example.org' % o.username)

    class Meta:
        model = User

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for group in extracted:
                self.groups.add(group)


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

    name = factory.Sequence(lambda n: "Group #%s" % n)

    @factory.post_generation
    def users(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for user in extracted:
                self.user_set.add(user)


class ACLRuleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ACLRule
    slug = factory.Sequence(lambda n: u'page{0}'.format(n))

    @classmethod
    def _prepare(cls, create, **kwargs):
        if 'permission' in kwargs and not isinstance(kwargs['permission'], Permission):
            kwargs['permission'] = Permission.objects.get(content_type__app_label='waliki',
                                                          codename=kwargs['permission'])
        return super(ACLRuleFactory, cls)._prepare(create, **kwargs)

    @factory.post_generation
    def users(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for user in extracted:
                self.users.add(user)

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for group in extracted:
                self.groups.add(group)