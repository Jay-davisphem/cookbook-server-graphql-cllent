import graphene
import graphql_jwt
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required

from django.contrib.auth.models import User
from .models import Category, Ingredient


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("username", "email")


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name", "owner", "ingredients")


class IngredietType(DjangoObjectType):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "notes", "category")


class Query(graphene.ObjectType):
    viewer = graphene.Field(UserType, token=graphene.String(required=True))
    all_ingredients = graphene.List(IngredietType
    category_by_name = graphene.Field(
        CategoryType,
        name=graphene.String(required=True),
    )

    @login_required
    def resolve_viewer(self, info, **kwargs):
        return info.context.user

    def resolve_all_ingredients(self, info):
        return Ingredient.objects.select_related("category").all()
    def resolve_category_by_name(self, info, name):
        try:
            return Category.objects.get(name=name.capitalize())
        except Category.DoesNotExist:
            return None


class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()


schema = graphene.Schema(mutation=Mutation, query=Query)
