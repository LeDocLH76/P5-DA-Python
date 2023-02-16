from rest_framework import permissions

from its_app.projects.models import Contributor


class IsProjectOwner(permissions.BasePermission):
    message = 'You are not project owner for this project'

    def has_object_permission(self, request, view, project_obj):
        user_role = request.user.contributor_set.get(project=project_obj).role
        if user_role != Contributor.OWNER:
            return False
        return True
