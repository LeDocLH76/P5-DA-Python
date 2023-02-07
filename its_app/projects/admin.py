from django.contrib import admin
from its_app.projects.models import Project


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'type')


admin.site.register(Project, ProjectAdmin)
