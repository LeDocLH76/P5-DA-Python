from django.contrib.auth import forms as auth_forms
from django.contrib.auth import get_user_model


class UserCreationForm(auth_forms.UserCreationForm):
    """CustomUser creation form"""

    class Meta(auth_forms.UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email')


class UserChangeForm(auth_forms.UserChangeForm):
    """CustomUser change form"""

    class Meta(auth_forms.UserChangeForm.Meta):
        model = get_user_model()
