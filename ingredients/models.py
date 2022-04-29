from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        "auth.User", related_name="categories", on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "owner"], name="unique user category"
            )
        ]

    def __str__(self):
        return f"{self.name}"


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    notes = models.TextField()
    category = models.ForeignKey(
        Category, related_name="ingredients", on_delete=models.CASCADE
    )

    constraints = [
        models.UniqueConstraint(fields=["name"], name="unique name ingredient")
    ]

    def __str__(self):
        return f"{self.name}"
