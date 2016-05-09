import factory
from uuid import uuid4
from django.contrib.auth.models import User

from core.constants import Permissions
from roller_auth.models import UserEmail
from company.models import Company, CompanyUsers
from projects.models import Projects, ProjectUsers

class UserFactory(factory.DjangoModelFactory):

    class Meta:
        model = User

    email = factory.Sequence(lambda x: 'user{0}@test.com'.format(x))
    username = email
    password = 'password'
    is_staff = False
    is_active = True
    is_superuser = False

    @classmethod
    def _prepare(cls, create, **kwargs):
        password = kwargs.pop('password', None)
        user = super(UserFactory, cls)._prepare(create, **kwargs)

        if password:
            user.set_password(password)

        if create:
            user.save()
        return user


class UserEmailFactory(factory.DjangoModelFactory):

    class Meta:
        model = UserEmail

    user = factory.SubFactory(UserFactory)
    email = factory.Sequence(lambda x: 'user{0}@domain.com'.format(x))


class CompanyFactory(factory.DjangoModelFactory):

    class Meta:
        model = Company

    name = factory.Sequence(lambda x: 'Company {0}'.format(x))
    uuid = factory.LazyAttribute(lambda o: str(uuid4()))
    created_by = factory.SubFactory(UserFactory)
    modified_by = factory.SubFactory(UserFactory)


class CompanyUserFactory(factory.DjangoModelFactory):

    class Meta:
        model = CompanyUsers

    user = factory.SubFactory(UserFactory)
    company = factory.SubFactory(CompanyFactory)
    permission = Permissions.OWNER


class ProjectFactory(factory.DjangoModelFactory):
    class Meta:
        model = Projects

    uuid = factory.LazyAttribute(lambda o: str(uuid4()))
    name = factory.Sequence(lambda x: 'Project {0}'.format(x))
    company = factory.SubFactory(CompanyFactory)
    created_by = factory.SubFactory(UserFactory)
    modified_by = factory.SubFactory(UserFactory)


class ProjectUserFactory(factory.DjangoModelFactory):

    class Meta:
        model = ProjectUsers

    user = factory.SubFactory(UserFactory)
    project = factory.SubFactory(ProjectFactory)
    permission = Permissions.OWNER
