from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views import generic
from .forms import SignupForm

class SignupView(generic.CreateView):
    form_class = SignupForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        # Authentifiez l'utilisateur après la création du compte
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
