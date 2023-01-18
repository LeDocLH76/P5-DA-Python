from django.contrib import admin
from its_app.users.models import MyUser


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email')


admin.site.register(MyUser, UserAdmin)
