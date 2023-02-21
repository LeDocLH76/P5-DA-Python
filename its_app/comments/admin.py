from django.contrib import admin
from its_app.comments.models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'description', 'issue',  'author', 'created_time'
    )


admin.site.register(Comment, CommentAdmin)
