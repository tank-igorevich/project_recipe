from django.test import TestCase
from django.urls import reverse
from .models import Recipe, Category

class RecipeViewsTest(TestCase):
    def setUp(self):
        # дві категорії
        cat1 = Category.objects.create(name='Desserts')
        cat2 = Category.objects.create(name='Soups')
        # 6 рецептів для перевірки slice
        for i in range(6):
            Recipe.objects.create(
                title=f'Recipe {i}',
                description='Desc',
                ingredients='Ing',
                instructions='Instr',
                category=cat1 if i % 2 else cat2,
            )

    def test_main_shows_last_5(self):
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')
        recipes = response.context['recipes']
        self.assertEqual(len(recipes), 5)
        # перевіримо, що останній створений об’єкт перший в списку
        self.assertEqual(recipes[0].title, 'Recipe 5')

    def test_category_list_counts(self):
        response = self.client.get(reverse('category_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'category_list.html')
        categories = {c.name: c.recipe_count for c in response.context['categories']}
        self.assertEqual(categories['Desserts'], 3)
        self.assertEqual(categories['Soups'], 3)
