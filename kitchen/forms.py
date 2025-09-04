from django import forms
from django.forms.models import inlineformset_factory

from .models import Dish, Ingredient, Cook, DishIngredient


class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = [
            'name',
            'description',
            'price',
            'dish_type',
            'cooks',
            'ingredients',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3},
            ),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'dish_type': forms.Select(attrs={'class': 'form-select'}),
            'cooks': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'ingredients': forms.SelectMultiple(
                attrs={'class': 'form-select'}
            ),

        }


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'stock']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class CookForm(forms.ModelForm):
    class Meta:
        model = Cook
        fields = [
            'user',
            'first_name',
            'last_name',
            'email',
            'years_of_experience',
            'photo',
        ]
        widgets = {
            'user': forms.Select(attrs={'class': 'form-select'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'years_of_experience': forms.NumberInput(
                attrs={'class': 'form-control'},
            ),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


DishIngredientFormSet = inlineformset_factory(
    Dish,
    DishIngredient,
    fields=('ingredient', 'amount'),
    extra=1,
    can_delete=True,
    widgets={
        'ingredient': forms.Select(attrs={'class': 'form-select'}),
        'amount': forms.NumberInput(attrs={'class': 'form-control'}),
    },
)
