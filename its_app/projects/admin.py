from django.contrib import admin
from its_app.projects.models import Project


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description')


admin.site.register(Project, ProjectAdmin)
