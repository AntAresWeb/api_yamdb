from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from api_yamdb.api_yamdb.users.models import RoleUser


class RoleUserCreationForm(UserCreationForm):
    class Meta:
        model = RoleUser
        fields = ('username', 'email', 'role', 'bio', 'first_name')

class RoleUserChangeForm(UserChangeForm):
    class Meta:
        model = RoleUser
        fields = ('username', 'email', 'role', 'bio', 'first_name')
