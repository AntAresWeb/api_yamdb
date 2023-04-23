from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import RoleUserCreationForm


class SignUpView(CreateView):
    form_class = RoleUserCreationForm
    success_url = reverse_lazy('homepage')
    template_name = 'users/signup.html'
