from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User


class RoleUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'bio', 'first_name',
                  'last_name')


class RoleUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'bio', 'first_name',
                  'last_name')
