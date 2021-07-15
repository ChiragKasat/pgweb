import factory
from factory.django import DjangoModelFactory
from pgweb.core.models import Version, UserProfile, Organisation, OrganisationEmail, OrganisationType, OrganisationEmail, ImportedRSSFeed, ImportedRSSItem
from pgweb.quotes.models import Quote
from django.contrib.auth.models import User, Group
import datetime


class VersionFactory(DjangoModelFactory):
    class Meta:
        model = Version

    tree = 13.3
    latestminor = 0
    reldate = datetime.datetime.today()
    current = False
    supported = True
    testing = 0
    docsloaded = datetime.datetime.now()
    firstreldate = datetime.datetime.today()
    eoldate = datetime.datetime.today()


class QuoteFactory(DjangoModelFactory):
    class Meta:
        model = Quote

    approved = False
    quote = "Test"
    who = "test name"
    org = "PostgreSQL"
    link = "https://postgresql.org"


class GroupFactory(DjangoModelFactory):
    class Meta:
        model = Group

    name = "test users"


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.Faker('email')
    password = factory.Faker('password')
    email = factory.LazyAttribute(lambda u: '%s%s@test.invalid' % (u.first_name.lower(), u.last_name.lower()))
    is_staff = False
    is_superuser = False

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for group in extracted:
                self.groups.add(group)


class UserProfileFactory(DjangoModelFactory):
    class Meta:
        model = UserProfile

    user = factory.SubFactory(UserFactory)
    sshkey = ""
    block_oauth = False


class OrganisationTypeFactory(DjangoModelFactory):
    class Meta:
        model = OrganisationType

    typename = "test"


class OrganisationFactory(DjangoModelFactory):
    class Meta:
        model = Organisation

    name = factory.Sequence(lambda n: "PostgreSQL%s" % n)
    address = "test address"
    url = "https://www.postgresql.org/"
    orgtype = factory.SubFactory(OrganisationTypeFactory)

    @factory.post_generation
    def managers(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for user in extracted:
                self.managers.add(user)
    mailtemplate = "default"


class OrganisationEmailFactory(DjangoModelFactory):
    class Meta:
        model = OrganisationEmail

    org = factory.SubFactory(OrganisationFactory)
    address = factory.Faker('address')
    confirmed = False
    token = factory.Faker('first_name')


class ImportedRSSFeedFactory(DjangoModelFactory):
    class Meta:
        model = ImportedRSSFeed

    internalname = "planet"
    url = "https://planet.postgresql.org/"
    purgepattern = "/"


class ImportedRSSItemFactory(DjangoModelFactory):
    class Meta:
        model = ImportedRSSItem

    feed = factory.SubFactory(ImportedRSSFeedFactory)
    title = "title"
    url = "https://www.postgresql.org/"
    posttime = datetime.datetime.now()
