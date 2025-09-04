from typing import Dict
from django.views.generic import (
    ListView, CreateView, UpdateView,
    DeleteView, TemplateView, DetailView
)
from django.urls import reverse_lazy
from django.db.models import Q, QuerySet
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpRequest, HttpResponse

from .models import Dish, Cook, Ingredient
from .forms import DishForm, DishIngredientFormSet, CookForm, IngredientForm


class HomeView(TemplateView):
    template_name = 'kitchen/home.html'


class DishListView(ListView):
    model = Dish
    template_name = 'kitchen/dish_list.html'
    context_object_name = 'dishes'
    paginate_by = 5

    def get_queryset(self: 'DishListView') -> QuerySet[Dish]:
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
        return queryset


def dish_create(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = DishForm(request.POST)
        formset = DishIngredientFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            dish = form.save()
            formset.instance = dish
            formset.save()
            return redirect('dish_list')
    else:
        form = DishForm()
        formset = DishIngredientFormSet()
    return render(
        request,
        'kitchen/dish_form.html',
        {'form': form, 'formset': formset}
    )


def dish_update(request: HttpRequest, pk: int) -> HttpResponse:
    dish = get_object_or_404(Dish, pk=pk)
    if request.method == 'POST':
        form = DishForm(request.POST, instance=dish)
        formset = DishIngredientFormSet(request.POST, instance=dish)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('dish_list')
    else:
        form = DishForm(instance=dish)
        formset = DishIngredientFormSet(instance=dish)
    return render(
        request,
        'kitchen/dish_form.html',
        {'form': form, 'formset': formset}
    )


class DishDetailView(DetailView):
    model = Dish
    template_name = 'kitchen/dish_detail.html'
    context_object_name = 'dish'


class DishDeleteView(DeleteView):
    model = Dish
    template_name = 'kitchen/dish_confirm_delete.html'
    success_url = reverse_lazy('dish_list')


class CookListView(ListView):
    model = Cook
    template_name = 'kitchen/cook_list.html'
    context_object_name = 'cooks'


class CookDetailView(DetailView):
    model = Cook
    template_name = 'kitchen/cook_detail.html'
    context_object_name = 'cook'

    def get_context_data(
            self: 'CookDetailView', **kwargs: object
    ) -> Dict[str, object]:
        context = super().get_context_data(**kwargs)
        context['dishes'] = self.object.dishes.all()
        return context


class CookCreateView(CreateView):
    model = Cook
    form_class = CookForm
    template_name = 'kitchen/cook_form.html'
    success_url = reverse_lazy('cook_list')


class CookUpdateView(UpdateView):
    model = Cook
    form_class = CookForm
    template_name = 'kitchen/cook_form.html'
    success_url = reverse_lazy('cook_list')


class CookDeleteView(DeleteView):
    model = Cook
    template_name = 'kitchen/cook_confirm_delete.html'
    success_url = reverse_lazy('cook_list')


class IngredientListView(ListView):
    model = Ingredient
    template_name = 'kitchen/ingredient_list.html'
    context_object_name = 'ingredients'
    ordering = ['name']


class IngredientCreateView(CreateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'kitchen/ingredient_form.html'
    success_url = reverse_lazy('ingredient_list')


class IngredientUpdateView(UpdateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'kitchen/ingredient_form.html'
    success_url = reverse_lazy('ingredient_list')
