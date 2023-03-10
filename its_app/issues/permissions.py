from rest_framework import permissions


class IsIssueOwner(permissions.BasePermission):
    message = 'You are not owner for this issue'

    def has_object_permission(self, request, view, issue_obj):
        user_obj = request.user
        issue_owner_obj = issue_obj.author
        if user_obj != issue_owner_obj:
            return False
        return True
