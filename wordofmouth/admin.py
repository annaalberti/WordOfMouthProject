########################################################################################
# REFERENCES
#  Title: Django documentation
#  Author: Django Software Foundation and individual contributors
#  Date: 2021
#  Date Cited: 5/03/2022
#  Code version: 4.0
#  URL: https://docs.djangoproject.com/en/4.0/intro/
#  Software License: BSD-3-Clause License
#
#  Title: django-polymorphic documentation
#  Author: Chris Glass, Diederik van der Boor, Charlie Denton,
#          Jerome Leclanche, and individual contributors
#  Date: 11/18/2021
#  Date Cited: 5/03/2022
#  Code version: 3.1
#  URL: https://django-polymorphic.readthedocs.io/en/stable/
#  Software License: BSD-3-Clause License
#
########################################################################################

'''
  This file follows the structure of the Django tutorial from
  the 'Django documentation' and adapts multiple methods from
  the tutorial
'''

from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin
from polymorphic.admin import PolymorphicChildModelAdmin
from polymorphic.admin import PolymorphicChildModelFilter

from .models import Rating, Recipe, RecipeBlock, Ingredient, Step, Image, Comment

'''
  Adds a polymorphic RecipeBlock object to the admin interface
  using the django-polymorphic library, the documentation for
  which can be found at the URL at the top of this document
'''
class RecipeBlockAdmin(PolymorphicChildModelAdmin):
    base_model = RecipeBlock

class IngredientAdmin(RecipeBlockAdmin):
    base_model = Ingredient

class IngredientAdmin(RecipeBlockAdmin):
    base_model = Step
    
class IngredientAdmin(RecipeBlockAdmin):
    base_model = Image

class commentAdmin(RecipeBlockAdmin):
    base_model = Comment

class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 0

class StepInline(admin.TabularInline):
    model = Step
    extra = 0

class ImageInline(admin.TabularInline):
    model = Image
    extra = 0

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientInline, StepInline, ImageInline, CommentInline]
    list_display = ('title', 'intro')

admin.site.register(Comment)
admin.site.register(Rating)
admin.site.register(Recipe, RecipeAdmin)
