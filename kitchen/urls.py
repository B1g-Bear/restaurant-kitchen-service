from django.urls import path

from .views import (
    HomeView,
    DishListView,
    DishDetailView,
    dish_create,
    dish_update,
    DishDeleteView,
    CookListView,
    CookCreateView,
    CookUpdateView,
    CookDeleteView,
    CookDetailView,
    IngredientListView,
    IngredientCreateView,
    IngredientUpdateView,
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('dishes/', DishListView.as_view(), name='dish_list'),
    path('dishes/add/', dish_create, name='dish_add'),
    path('dishes/<int:pk>/', DishDetailView.as_view(), name='dish_detail'),
    path('dishes/<int:pk>/edit/', dish_update, name='dish_edit'),
    path('dishes/<int:pk>/delete/', DishDeleteView.as_view(),
         name='dish_delete'
         ),
    path('cooks/', CookListView.as_view(), name='cook_list'),
    path('cooks/add/', CookCreateView.as_view(), name='cook_add'),
    path('cooks/<int:pk>/', CookDetailView.as_view(), name='cook_detail'),
    path('cooks/<int:pk>/edit/', CookUpdateView.as_view(), name='cook_edit'),
    path('cooks/<int:pk>/delete/', CookDeleteView.as_view(),
         name='cook_delete'
         ),
    path('ingredients/', IngredientListView.as_view(), name='ingredient_list'),
    path(
        'ingredients/add/',
        IngredientCreateView.as_view(),
        name='ingredient_add',
    ),
    path(
        'ingredients/<int:pk>/edit/',
        IngredientUpdateView.as_view(),
        name='ingredient_edit',
    ),
]
