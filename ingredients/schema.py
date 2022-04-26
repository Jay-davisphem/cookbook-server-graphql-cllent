import graphene
import graphql_jwt
from graphene_django import DjangoObjectType

from .models import Category, Ingredient


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name", "ingredients")


class IngredietType(DjangoObjectType):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "notes", "category")


class Query(graphene.ObjectType):
    all_ingredients = graphene.List(IngredietType)
    category_by_name = graphene.Field(CategoryType, name=graphene.String(required=True))

    def resolve_all_ingredients(root, info):
        return Ingredient.objects.select_related("category").all()

    def resolve_category_by_name(root, info, name):
        try:
            return Category.objects.get(name=name.capitalize())
        except Category.DoesNotExist:
            return None


class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(mutation=Mutation, query=Query)
