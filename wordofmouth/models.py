########################################################################################
# REFERENCES
#  Title: django-googledrive-storage documentation
#  Author: Gian Luca Dalla Torre and individual contributors
#  Date: 11/28/2021
#  Date Cited: 5/02/2022
#  Code version: 1.6.0
#  URL: https://django-googledrive-storage.readthedocs.io/en/latest/
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
#  Title: Django documentation
#  Author: Django Software Foundation and individual contributors
#  Date: 2021
#  Date Cited: 5/03/2022
#  Code version: 4.0
#  URL (1): https://docs.djangoproject.com/en/4.0/intro/
#  URL (2): https://docs.djangoproject.com/en/4.0/ref/models/fields/#django.db.models.ManyToManyField
#  Software License: BSD-3-Clause License
#
#  Title: Stack Overflow answer to “Using Pre_delete Signal in django”
#  Author: Josh Smeaton (https://stackoverflow.com/users/10583/josh-smeaton)
#  Date: 12/13/2012
#  Date Cited: 5/02/2022
#  URL: https://stackoverflow.com/questions/13857007/using-pre-delete-signal-in-django
#  Software License: CC BY-SA 3.0
#
########################################################################################

'''
  This file follows the structure of the Django tutorial from
  the 'Django documentation' and adapts multiple methods from
  the tutorial
'''

from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from polymorphic.models import PolymorphicModel
from gdstorage.storage import GoogleDriveStorage


'''
  Define Google Drive Storage using the
  django-googledrive-storage library, for which the
  documentation can be found at the URL at the top
  of this document.
'''
gd_storage = GoogleDriveStorage()

# Create your models here.

class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length = 150)
    intro = models.CharField(max_length = 600)
    time = models.DurationField()
    
    '''
      ManyToManyField relationships sourced from the 'Django documentation'
    '''
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    parent = models.ManyToManyField('self', blank=True, symmetrical=False)
    children = models.ManyToManyField('self', related_name='child', blank=True, symmetrical=False)

    def calc_rating(self):
        ratings = [rate.rating for rate in self.rating_set.all()]
        return sum(ratings)/len(ratings) if ratings else 0

'''
  Handle deleting Recipe objects by defining a reciever for the pre_delete
  signal and manually deleting recipeBlocks to avoid ForeignKey errors
  caused by PolymorphicModel. Also maintains fork history. Sourced from
  a Stack Overflow question answered by user Josh Smeaton. 
'''
@receiver(pre_delete, sender=Recipe, dispatch_uid='recipe_delete_signal')
def onRecipeDelete(sender, instance, using, **kwargs):
    # delete polymorphic elements (avoids ForeignKey errors)
    recipeBlocks = instance.recipeblock_set.all()
    for recipeBlock in recipeBlocks:
        recipeBlock.delete()
    # preserve fork ancestry
    children = instance.children.all()
    if children:
        parents = instance.parent.all()
        for child in children:
            child.parent.set(instance.parent.all())
            if parents:
                parents[0].children.add(child)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    commentText = models.CharField(max_length = 4000)
    postTime = models.TimeField(auto_now_add=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    rating = models.IntegerField(default=0)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

'''
  Define a polymorphic RecipeBlock object using the
  django-polymorphic library, for which the documentation 
  can be found at the URL at the top of this document.
'''
class RecipeBlock(PolymorphicModel):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    isIngredient = isStep = isImage = False

'''
  The following classes inherit from the RecipeBlock
  object using the django-polymorphic library, for
  which the documentation can be found at the URL at
  the top of this document.
'''
class Ingredient(RecipeBlock):
    name = models.CharField(max_length = 150)
    quantity = models.CharField(max_length = 150)
    unit = models.CharField(max_length = 150)
    isIngredient = True

class Step(RecipeBlock):
    text = models.CharField(max_length = 4000)
    isStep = True

'''
  Uses Google Drive Storage as a storage location
  through the django-googledrive-storage library,
  for which the documentation can be found at the
  URL at the top of this document.
'''
class Image(RecipeBlock):
    src = models.ImageField(upload_to='img', storage=gd_storage)
    isImage = True
