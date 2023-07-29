from django.urls import path

from . import views

app_name = 'wordofmouth'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('recipes/<int:pk>/', views.RecipeDetailView.as_view(), name='recipe_detail'),
    path('recipes/<int:pk>/edit/', views.EditRecipeView.as_view(), name = 'edit_recipe'),
    path('recipes/<int:pk>/fork/', views.ForkRecipeView.as_view(), name = 'fork_recipe'),
    path('recipes/<int:pk>/like', views.LikeView, name = 'like_post'),
    path('recipes/<int:pk>/unlike', views.UnlikeView, name = 'unlike_post'),
    path('recipes/<int:pk>/comment', views.CommentView, name = 'comment_post'),
    path('recipes/<int:pk>/rate', views.RateView, name = 'rate_post'),
    path('recipes/<int:rpk>/comment/<int:cpk>/delete', views.deleteComment, name='deleteComment'),
    path('recipes/<int:rpk>/comment/<int:cpk>/edit', views.editCommentView, name='editCommentView'),
    path('recipes/<int:rpk>/comment/<int:cpk>/enter-edit', views.editComment, name='editComment'),
    path('recipes/<int:rpk>/delete', views.deleteRecipe, name='deleteRecipe'),
    path('add/', views.add_Recipe_View, name='add_recipe'),
    path('your_recipes/', views.YourRecipesView.as_view(), name='your_recipes'),
    path('search_recipes/', views.search_recipes, name='search_recipes'),
]
