import graphene
import graphql_jwt
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required

from django.contrib.auth.models import User
from .models import Category, Ingredient


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("username",)


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name", "owner", "ingredients")


class IngredietType(DjangoObjectType):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "notes", "category")


class CreateUser(graphene.Mutation):
    message = graphene.String()
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String()

    def mutate(self, info, **kwargs):
        user = User.objects.create_user(
            username=kwargs.get("username"), email=kwargs.get("email")
        )
        user.set_password(kwargs.get("password"))
        user.save()
        return CreateUser(
            user=user, message=f"Successfully created user {user.username}"
        )


class CreateCategory(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        name = graphene.String(required=True)

    @login_required
    def mutate(self, info, name):
        owner = info.context.user
        Category.objects.create(owner=owner, name=name)
        return CreateCategory(ok=True)


class CreateIngredients(graphene.Mutation):
    ok = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        names = graphene.List(graphene.String, required=True)
        notes = graphene.List(graphene.String)
        category_id = graphene.ID()

    @login_required
    def mutate(self, info, names, category_id, notes=None):
        not_null = "Null list value"

        is_cat = False
        if category_id:
            category = Category.objects.get(pk=category_id)
            is_cat = True
        if is_cat:
            if notes:
                if len(names) == len(notes):
                    for i in range(len(names)):
                        Ingredient.objects.create(
                            name=names[i], notes=notes[i], category=category
                        )
                    return CreateIngredients(
                        ok=True,
                        message=f"Successfully created a neat set of ingredients",
                    )
                else:
                    for i in range(len(names)):
                        Ingredients.objects.create(names=names[i], category=category)
                    return CreateIngredients(
                        ok=True,
                        message=f"Successfully created a partially neat set of ingredients",
                    )
        else:
            return CreateIngredients(
                ok=False, message=f"Unsuccessful! Please, supply category ID."
            )


# DeleteIngredients, DeleteCategory, UpdateIngredient and UpdateCategory to be implemented when needed

class Query(graphene.ObjectType):
    viewer = graphene.Field(UserType)  # token=graphene.String(required=True))
    all_ingredients = graphene.List(IngredietType)
    all_categories = graphene.List(CategoryType)
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

    def resolve_all_categories(self, info):
        return Category.objects.all()


class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()
    create_user = CreateUser.Field()
    create_category = CreateCategory.Field()
    create_ingredient = CreateIngredients.Field()


schema = graphene.Schema(mutation=Mutation, query=Query)
