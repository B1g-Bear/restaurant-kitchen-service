from __future__ import annotations
from typing import Any
from django.db import models
from django.contrib.auth.models import User


class Cook(models.Model):
    user: User = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Користувач',
    )
    first_name: str = models.CharField(
        max_length=50,
        verbose_name="Ім'я",
    )
    last_name: str = models.CharField(
        max_length=50,
        verbose_name='Прізвище',
    )
    years_of_experience: int = models.PositiveIntegerField(
        verbose_name='Роки досвіду',
    )
    email: str = models.EmailField(
        max_length=254,
        blank=True,
        verbose_name='Email',
    )
    photo: Any = models.ImageField(
        upload_to='cooks_photos/',
        null=True,
        blank=True,
        verbose_name='Фото',
    )

    class Meta:
        verbose_name = 'Кухар'
        verbose_name_plural = 'Кухарі'

    def __str__(self: Cook) -> str:
        return f'{self.first_name} {self.last_name}'


class DishType(models.Model):
    name: str = models.CharField(
        max_length=50,
        verbose_name='Тип страви',
    )

    class Meta:
        verbose_name = 'Тип страви'
        verbose_name_plural = 'Типи страв'

    def __str__(self: DishType) -> str:
        return self.name


class Ingredient(models.Model):
    name: str = models.CharField(
        max_length=50,
        verbose_name='Назва інгредієнта',
    )
    stock: int = models.PositiveIntegerField(
        default=0,
        verbose_name='Запас',
    )

    class Meta:
        verbose_name = 'Інгредієнт'
        verbose_name_plural = 'Інгредієнти'

    def __str__(self: Ingredient) -> str:
        return f'{self.name} ({self.stock})'


class Dish(models.Model):
    name: str = models.CharField(
        max_length=100,
        verbose_name='Назва страви',
    )
    description: str = models.TextField(
        blank=True,
        verbose_name='Опис',
    )
    price: float = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='Ціна',
    )
    dish_type: DishType = models.ForeignKey(
        DishType,
        on_delete=models.CASCADE,
        verbose_name='Тип страви',
    )
    cooks: Any = models.ManyToManyField(
        Cook,
        related_name='dishes',
        verbose_name='Кухарі',
    )
    ingredients: Any = models.ManyToManyField(
        Ingredient,
        through='DishIngredient',
        blank=True,
        related_name='dishes',
        verbose_name='Інгредієнти',
    )

    class Meta:
        verbose_name = 'Страва'
        verbose_name_plural = 'Страви'

    def __str__(self: Dish) -> str:
        return self.name

    def max_possible(self: Dish) -> int:
        ingredients = DishIngredient.objects.filter(dish=self)
        if not ingredients.exists():
            return 0
        min_portions = float('inf')
        for di in ingredients:
            if di.amount == 0:
                continue
            possible = di.ingredient.stock // di.amount
            min_portions = min(min_portions, possible)
        return min_portions


class DishIngredient(models.Model):
    dish: Dish = models.ForeignKey(
        Dish,
        on_delete=models.CASCADE,
        verbose_name='Страва',
    )
    ingredient: Ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Інгредієнт',
    )
    amount: int = models.PositiveIntegerField(
        default=1,
        verbose_name='Кількість на порцію',
    )

    class Meta:
        verbose_name = 'Інгредієнт страви'
        verbose_name_plural = 'Інгредієнти страви'

    def __str__(self: DishIngredient) -> str:
        return f'{self.ingredient.name} для {self.dish.name}: {self.amount}'
