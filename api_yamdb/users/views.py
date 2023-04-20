from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from api_yamdb.api_yamdb.users.forms import RoleUserCreationForm


# Create your views here.
class SignUpView(CreateView):
    form_class = RoleUserCreationForm
    success_url = reverse_lazy('homepage')
    template_name = 'users/signup.html'

    # def post(self, request, *args, **kwargs):
    #     form = RoleUserCreationForm(request.POST)
    #     if form.is_valid():
    #         user = form.save(commit=False)
    #         user.save()
