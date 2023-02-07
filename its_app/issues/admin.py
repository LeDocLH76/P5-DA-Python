from django.contrib import admin
from its_app.issues.models import Issue


class IssueAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'description',  'project',
        'author', 'assignee', 'created_time'
    )


admin.site.register(Issue, IssueAdmin)
