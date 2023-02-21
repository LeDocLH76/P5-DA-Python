from rest_framework import permissions


class IsCommentOwner(permissions.BasePermission):
    message = 'You are not owner for this comment'

    def has_object_permission(self, request, view, comment_obj):
        user_obj = request.user
        comment_owner_obj = comment_obj.author
        if user_obj != comment_owner_obj:
            return False
        return True
