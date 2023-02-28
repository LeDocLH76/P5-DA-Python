from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from its_app.projects.models import Project


class Command(BaseCommand):
    help = """Create groups BasicUser & ProjectContributor
 with appropriate permissions."""

    def handle(self, *args, **kwargs):
        BasicUser, created = Group.objects.get_or_create(
            name='BasicUser'
        )
        ProjectContributor, created = Group.objects.get_or_create(
            name='ProjectContributor'
        )
        self.stdout.write("Groups: Done")
        content_type = ContentType.objects.get_for_model(Project)
        project_permissions = Permission.objects.filter(
            content_type=content_type
        )
        for perm in project_permissions:
            self.stdout.write(perm.codename)
            if perm.codename == "add_project":
                BasicUser.permissions.add(perm)
                ProjectContributor.permissions.add(perm)
            elif perm.codename == "view_project":
                BasicUser.permissions.add(perm)
                ProjectContributor.permissions.add(perm)
            else:
                ProjectContributor.permissions.add(perm)
        self.stdout.write("Permissions: Done")
