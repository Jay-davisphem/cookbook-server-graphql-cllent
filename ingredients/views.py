from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

from graphene_django.views import GraphQLView


class PGView(LoginRequiredMixin, GraphQLView):
    pass


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("graphql")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})
