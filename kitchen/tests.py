from django.test import TestCase
from django.contrib.auth.models import User
from .models import Cook, Dish, DishType, Ingredient, DishIngredient


class CookModelTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.cook = Cook.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            years_of_experience=5,
            email='john@example.com'
        )

    def test_str_method(self) -> None:
        self.assertEqual(str(self.cook), 'John Doe')


class DishModelTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='cookuser', password='12345')
        self.cook = Cook.objects.create(
            user=self.user,
            first_name='Jane',
            last_name='Smith',
            years_of_experience=3,
            email='jane@example.com'
        )
        self.dish_type = DishType.objects.create(name='Soup')
        self.dish = Dish.objects.create(
            name='Tomato Soup',
            description='Delicious tomato soup',
            price=5.50,
            dish_type=self.dish_type
        )
        self.dish.cooks.add(self.cook)

    def test_str_method(self) -> None:
        self.assertEqual(str(self.dish), 'Tomato Soup')

    def test_max_possible_empty(self) -> None:
        self.assertEqual(self.dish.max_possible(), 0)

    def test_max_possible_with_ingredients(self) -> None:
        ingredient1 = Ingredient.objects.create(name='Tomato', stock=10)
        ingredient2 = Ingredient.objects.create(name='Water', stock=5)
        DishIngredient.objects.create(dish=self.dish, ingredient=ingredient1, amount=2)
        DishIngredient.objects.create(dish=self.dish, ingredient=ingredient2, amount=1)
        self.assertEqual(self.dish.max_possible(), 5)


class IngredientModelTest(TestCase):
    def setUp(self) -> None:
        self.ingredient = Ingredient.objects.create(name='Salt', stock=10)

    def test_str_method(self) -> None:
        self.assertEqual(str(self.ingredient), 'Salt (10)')


class DishIngredientModelTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='chefuser', password='12345')
        self.cook = Cook.objects.create(
            user=self.user,
            first_name='Mike',
            last_name='Brown',
            years_of_experience=2,
            email='mike@example.com'
        )
        self.dish_type = DishType.objects.create(name='Salad')
        self.dish = Dish.objects.create(
            name='Caesar Salad',
            description='Classic Caesar salad',
            price=7.00,
            dish_type=self.dish_type
        )
        self.dish.cooks.add(self.cook)
        self.ingredient = Ingredient.objects.create(name='Lettuce', stock=5)
        self.dish_ingredient = DishIngredient.objects.create(
            dish=self.dish,
            ingredient=self.ingredient,
            amount=2
        )

    def test_str_method(self) -> None:
        self.assertEqual(str(self.dish_ingredient), 'Lettuce для Caesar Salad: 2')
