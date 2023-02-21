from rest_framework import permissions


class IsIssueOwner(permissions.BasePermission):
    message = 'You are not owner for this issue'

    def has_object_permission(self, request, view, issue_obj):
        user_obj = request.user
        issue_owner_obj = issue_obj.author
        if user_obj != issue_owner_obj:
            return False
        return True


class IsIssueOwnerOrAssignee(permissions.BasePermission):
    message = 'You are not owner or assignee for this issue'

    def has_object_permission(self, request, view, issue_obj):
        user_obj = request.user
        issue_owner_obj = issue_obj.author
        issue_assignee_obj = issue_obj.assignee
        if (
            user_obj == issue_owner_obj
            or
            user_obj == issue_assignee_obj
        ):
            return True
        return False
