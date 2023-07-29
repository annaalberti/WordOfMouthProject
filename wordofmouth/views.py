########################################################################################
#  REFERENCES
#  Title: Build A Blog Comment Section - Django Blog #33
#  Author: John Elder
#  Date: 7/16/2020
#  Date Cited: 3/20/2022
#  URL: https://www.youtube.com/watch?v=hZrlh4qU4eQ
#  Software License: Copyright of Codemy.com
#
#  Title: Django documentation
#  Author: Django Software Foundation and individual contributors
#  Date: 2021
#  Date Cited: 5/3/2022
#  Code version: 4.0
#  URL: https://docs.djangoproject.com/en/4.0/intro/
#  Software License: BSD-3-Clause License
#
#  Title: Stack Overflow answer to “Django filter many-to-many with contains”
#  Author: mouad (https://stackoverflow.com/users/479633/mouad)
#  Date: 12/22/2010
#  Date Cited: 5/3/2022
#  URL: https://stackoverflow.com/questions/4507893/django-filter-many-to-many-with-contains
#  Software License: CC BY-SA 2.5
#
########################################################################################

'''
  This file follows the structure of the Django tutorial from
  the 'Django documentation' and adapts multiple methods from
  the tutorial
'''

from urllib import request
from django.dispatch import receiver
from django.views import generic
from django.shortcuts import get_object_or_404, render
from .models import Recipe, RecipeBlock, Ingredient, Step, Image, Comment, Rating
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
import urllib.request
from datetime import timedelta
from django.db.models.query_utils import Q


# view for home page to feed recipe objects to html to show as a list 
class IndexView(generic.ListView):
    template_name = 'wordofmouth/index.html'
    context_object_name = 'recList'

    def get_queryset(self):
        return Recipe.objects.all()


# function for adding like to a recipe
def LikeView(request, pk):
    # get object from db 
    curRecipe = get_object_or_404(Recipe, pk=request.POST.get('input_id'))
    # add user to recipe many to many relationship 
    curRecipe.likes.add(request.user)
    # save the edit 
    curRecipe.save()
    return HttpResponseRedirect(reverse('wordofmouth:recipe_detail', args=(str(pk),)))


# similar idea as LikeView but instead remove the like
def UnlikeView(request, pk):
    curRecipe = get_object_or_404(Recipe, pk=request.POST.get('input_id'))
    curRecipe.likes.remove(request.user)
    curRecipe.save()
    return HttpResponseRedirect(reverse('wordofmouth:recipe_detail', args=(str(pk),)))


def CommentView(request, pk):
    # https://www.youtube.com/watch?v=hZrlh4qU4eQ source for implementing comment section 
    curRecipe = get_object_or_404(Recipe, pk=request.POST.get('comment'))
    curCommentText = request.POST.get('comment_text')
    curComment = Comment(user=request.user, commentText=curCommentText, recipe=curRecipe)

    # avoid posting empty comment 
    if len(curCommentText) != 0:
        curComment = Comment(user=request.user, commentText=curCommentText, recipe=curRecipe)
        curComment.save()

    return HttpResponseRedirect(reverse('wordofmouth:recipe_detail', args=(str(pk),)))


def RateView(request, pk):
    curRecipe = get_object_or_404(Recipe, pk=request.POST.get('rate'))
    curRateNum = request.POST.get('rate_num')
    try:
        curRate = Rating.objects.get(user=request.user, recipe=curRecipe)
        curRate.rating = curRateNum
    except Rating.DoesNotExist:
        curRate = Rating(user=request.user, rating=curRateNum, recipe=curRecipe)
    curRate.save()

    return HttpResponseRedirect(reverse('wordofmouth:recipe_detail', args=(str(pk),)))


class RecipeDetailView(generic.DetailView):
    model = Recipe
    template_name = 'wordofmouth/recipe_detail.html'

# view for home page to feed recipe objects to html to show as a list
class YourRecipesView(generic.ListView):
    template_name = 'wordofmouth/your_recipes.html'
    context_object_name = 'recList'

    def get_queryset(self):
        queryset = {}
        if not self.request.user.is_anonymous:
            userRecipes = Recipe.objects.filter(user=self.request.user)
            
            '''
              Filtering by contents of ManyToManyField contents based on
              a Stack Overflow answer by user mouad
            '''
            likedRecipes = Recipe.objects.filter(likes__in=[self.request.user])

            queryset = {
                'user_recipes': userRecipes,
                'liked_recipes': likedRecipes
            }
        return queryset

def getRecipeData(post, files):
    getTitle = post["Title"]
    getIntro = post["Intro"]
    getTime = timedelta(
        days=int(post["Time[days]"]) if post["Time[days]"] else 0,
        hours=int(post["Time[hours]"] if post["Time[hours]"] else 0),
        minutes=int(post["Time[minutes]"] if post["Time[minutes]"] else 0),
        seconds=int(post["Time[seconds]"] if post["Time[seconds]"] else 0),
    )
    getSteps = post.getlist("Step[]")
    getImages = files.getlist("Image[]")
    getSavedUrls = post.getlist("OldImg[]")
    getImageEntries = post.getlist("Entry[]")
    getIngredients = zip(post.getlist("Ingredient[]"),
                         post.getlist("Quantity[]"),
                         post.getlist("Unit[]"))
    
    return {
        'title': getTitle,
        'intro': getIntro,
        'time': getTime,
        'ingredients': getIngredients,
        'steps': getSteps,
        'images': getImages,
        'savedUrls': getSavedUrls,
        'imageEntries': getImageEntries,
    }


def setRecipeData(userRecipe, rData):
    for ingredient in rData['ingredients']:
        if ingredient[0]:
            Ingredient.objects.create(
                recipe=userRecipe,
                name=ingredient[0],
                quantity=ingredient[1],
                unit = ingredient[2],
            )
    for step in rData['steps']:
        if step:
            Step.objects.create(recipe=userRecipe, text=step)
    for entry in rData['imageEntries']:
        if entry[0] == '1':
            Image.objects.create(recipe=userRecipe, src=rData['images'].pop(0))
        elif entry[1] == '1':
            Image.objects.create(recipe=userRecipe, src=rData['savedUrls'][0])
        rData['savedUrls'].pop(0)


def add_Recipe_View(request):
    if request.POST:
        rData = getRecipeData(request.POST, request.FILES)
        userRecipe = Recipe.objects.create(
            title=rData['title'],
            intro=rData['intro'],
            time=rData['time'],
            user=request.user
        )
        setRecipeData(userRecipe, rData)
        return HttpResponseRedirect(reverse('wordofmouth:recipe_detail', args=(userRecipe.id,)))
    return render(request, "wordofmouth/add_recipe.html")


class EditRecipeView(generic.DetailView):
    model = Recipe
    template_name = 'wordofmouth/edit_recipe.html'

    def post(self, request, *args, **kwargs):
        rData = getRecipeData(request.POST, request.FILES)
        
        userRecipe = self.get_object()
        userRecipe.title = rData['title']
        userRecipe.intro = rData['intro']
        userRecipe.time = rData['time']
        userRecipe.save()
        
        recipeBlocks = userRecipe.recipeblock_set.all()
        for recipeBlock in recipeBlocks:
            recipeBlock.delete()
        
        setRecipeData(userRecipe, rData)
        return HttpResponseRedirect(reverse('wordofmouth:recipe_detail', args=(userRecipe.id,)))


class ForkRecipeView(generic.DetailView):
    model = Recipe
    template_name = 'wordofmouth/edit_recipe.html'

    def post(self, request, *args, **kwargs):
        rData = getRecipeData(request.POST, request.FILES)
        parentRecipe = self.get_object()
        userRecipe = Recipe.objects.create(
            title=rData['title'],
            intro=rData['intro'],
            time=rData['time'],
            user=request.user
        )
        userRecipe.parent.add(parentRecipe)
        parentRecipe.children.add(userRecipe)
        userRecipe.save()
        
        setRecipeData(userRecipe, rData)
        return HttpResponseRedirect(reverse('wordofmouth:recipe_detail', args=(userRecipe.id,)))

def search_recipes(request):
    args = {}
    if request.method == "POST":
        searched = request.POST['searched']
        args = {
            'searched': searched,
            'recipes': Recipe.objects.filter(
                Q(title__icontains=searched) |
                Q(intro__icontains=searched)
            ),
        }
    return render(request, 'wordofmouth/search_recipes.html', args)

def deleteComment(request, rpk, cpk):
    curComment = Comment.objects.filter(pk=request.POST.get('commentPK'))
    curComment.delete()
    return HttpResponseRedirect(reverse('wordofmouth:recipe_detail', args=(rpk,)))

def editCommentView(request, rpk, cpk):
    recipe = Recipe.objects.get(pk = rpk)
    curComment = Comment.objects.get(user=request.user, recipe=recipe, pk=cpk).commentText
    context = {"comment":curComment, 'rpk':rpk, 'cpk':cpk}
    return render(request, 'wordofmouth/edit_comment_view.html', context)

def editComment(request, rpk, cpk):
    curRecipe = get_object_or_404(Recipe, pk=rpk)
    curComment = Comment.objects.get(user=request.user, recipe=curRecipe, pk=cpk)
    # avoid posting empty comment 
    curCommentText = request.POST.get('comment_text')
    if len(curCommentText) != 0:
        curComment.commentText = curCommentText
        curComment.save()

    return HttpResponseRedirect(reverse('wordofmouth:recipe_detail', args=(rpk,)))

def deleteRecipe(request, rpk):
    curRecipe = get_object_or_404(Recipe, pk=rpk)
    curRecipe.delete()
    return HttpResponseRedirect(reverse('wordofmouth:index'))
