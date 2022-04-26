from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views

from ingredients.views import PGView, register
from graphene_django.views import GraphQLView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
    path("graphql/", csrf_exempt(PGView.as_view(graphiql=True)), name='graphql'),
]
