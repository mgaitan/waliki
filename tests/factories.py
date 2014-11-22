import factory
from django.contrib.auth.models import User, Group, Permission
from waliki.models import ACLRule, Page, Redirect


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: u'user{0}'.format(n))
    password = factory.PostGenerationMethodCall('set_password', 'pass')
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

    name = factory.Sequence(lambda n: u'Rule {0}'.format(n))
    slug = factory.Sequence(lambda n: u'page{0}'.format(n))

    @factory.post_generation
    def permissions(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for perm in extracted:
                if not isinstance(perm, Permission):
                    perm = Permission.objects.get(content_type__app_label='waliki', codename=perm)
                self.permissions.add(perm)

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


class PageFactory(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda n: u'Page {0}'.format(n))
    slug = factory.Sequence(lambda n: u'page{0}'.format(n))

    @factory.post_generation
    def raw(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            self.raw = extracted

    class Meta:
        model = Page


class RedirectFactory(factory.django.DjangoModelFactory):
    old_slug = factory.Sequence(lambda n: u'old-page{0}'.format(n))
    new_slug = factory.Sequence(lambda n: u'new-page{0}'.format(n))


    class Meta:
        model = Redirect

