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
#  Title: Django documentation
#  Author: Django Software Foundation and individual contributors
#  Date: 2021
#  Date Cited: 5/03/2022
#  Code version: 4.0
#  URL: https://docs.djangoproject.com/en/4.0/intro/
#  Software License: BSD-3-Clause License
#
#  Title: Stack Overflow answer to “Django's self.client.login(...) does not work in unit tests”
#  Author: Pedro M Duarte
#  Date: 10/23/2015
#  Date Cited: 5/02/2022
#  URL: https://stackoverflow.com/questions/2619102/djangos-self-client-login-does-not-work-in-unit-tests
#  Software License: CC BY-SA 3.0
#
#  Title: Stack Overflow answer to “how to unit test file upload in django”
#  Author: Danilo Cabello (https://stackoverflow.com/users/157931/danilo-cabello)
#  Date: 12/7/2014
#  Date Cited: 5/02/2022
#  URL: https://stackoverflow.com/questions/11170425/how-to-unit-test-file-upload-in-django
#  Software License: CC BY-SA 3.0
#
#  Title: Stack Overflow answer to “How should I write tests for Forms in Django?”
#  Author: Torsten Engelbrecht (https://stackoverflow.com/users/461343/torsten-engelbrecht)
#  Date: 9/5/2011
#  Date Cited: 5/03/2022
#  URL: https://stackoverflow.com/questions/7304248/how-should-i-write-tests-for-forms-in-django
#  Software License: CC BY-SA 3.0
#
#  Title: Stack Overflow question “Django SECURE_SSL_REDIRECT breaks unit
#         tests that use the in-built client”
#  Author: David Downes (https://stackoverflow.com/users/1310032/david-downes)
#  Date: 5/3/2018
#  Date Cited: 5/03/2022
#  URL: https://stackoverflow.com/questions/49626899/django-secure-ssl-redirect-breaks-unit-tests-that-use-the-in-built-client
#  Software License: CC BY-SA 4.0
#
########################################################################################

'''
  This file follows the structure of the Django tutorial from
  the 'Django documentation' and adapts multiple methods from
  the tutorial
'''

'''
  The following tests make frequent use of manually constructed
  for POST data, which was sourced from a Stack Overflow answer by
  user Torsten Engelbrecht. Additionally, all POST requests
  required secure connections after enabling SSL redirects in
  settings.py, which was done by following a Stack Overflow question
  posted by user David Downes.
'''

from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from django.test import Client

from .models import Recipe, RecipeBlock, Ingredient, Step, Image
from gdstorage.storage import GoogleDriveStorage

from datetime import timedelta
from functools import reduce

'''
  Uses the method outlined in a Stack Overflow answer by user
  Pedro M Duarte to create a test user and authenticate the 
  test client
'''
def authenticate(client):
        # login test client
        User.objects.create_user(username='user', password='pass')
        client.login(username='user', password='pass')

class AddRecipeViewTests(TestCase):
    def test_reachable(self):
        """
        test if page is reachable
        """
        url = reverse('wordofmouth:add_recipe')
        response = self.client.get(url, secure=True)
        self.assertEqual(response.status_code, 200)

    def test_anon(self):
        """
        test that login is required to view page
        """
        url = reverse('wordofmouth:add_recipe')
        response = self.client.get(url, secure=True)
        self.assertContains(response, 'Please login to access this page')
        
    def test_auth(self):
        """
        test that page does not prompt for login when already logged in
        """
        
        # login
        authenticate(self.client)
        
        # load page
        url = reverse('wordofmouth:add_recipe')
        response = self.client.get(url, secure=True)
        self.assertNotContains(response, 'Please login to access this page')
        
    def test_addempty(self):
        """
        test that a simple into/title/time only recipe can be added
        """
        
        # login
        authenticate(self.client)
        
        # post form
        form_data = {
            'Title' : 'recipe',
            'Intro' : 'intro',
            'Time[days]' : '0',
            'Time[hours]' : '0',
            'Time[minutes]' : '0',
            'Time[seconds]' : '0',
            }
        url = reverse('wordofmouth:add_recipe')
        response = self.client.post(url, form_data, secure=True)
        
        # check that recipe was created
        self.assertEquals(len(Recipe.objects.all()), 1)
        
        # check that fields are correct
        self.assertEquals(Recipe.objects.all()[0].title, 'recipe')
        self.assertEquals(Recipe.objects.all()[0].intro, 'intro')

    def test_addcomplex(self):
        """
        test that a multifield recipe can be submitted
        """
        
        # login
        authenticate(self.client)
        
        # post form
        form_data = {
            'Title' : 'recipe',
            'Intro' : 'intro',
            'Time[days]' : '0',
            'Time[hours]' : '1',
            'Time[minutes]' : '2',
            'Time[seconds]' : '3',
            'Ingredient[]' : ['I1', 'I2', 'I3'],
            'Quantity[]' : ['1', '2', '3'],
            'Unit[]' : ['cup', 'lbs', 'oz'],
            'Step[]' : ['S1', 'S2', 'S3'],
            }
        url = reverse('wordofmouth:add_recipe')
        response = self.client.post(url, form_data, secure=True)
        
        # check that recipe was created
        self.assertEquals(len(Recipe.objects.all()), 1)
        
        # check that intro/title fields are correct
        self.assertEquals(Recipe.objects.all()[0].title, 'recipe')
        self.assertEquals(Recipe.objects.all()[0].intro, 'intro')
        
        # check correct number of components
        self.assertEquals(len(Recipe.objects.all()[0].recipeblock_set.all()), 6)
        
        # check correct number of ingredients vs step fields
        self.assertEquals(
            reduce(lambda a, b:
                a + b.isStep,
                Recipe.objects.all()[0].recipeblock_set.all(),
                0
            ),
            3
        )

'''
  Google Drive Storage tests written by following the associated
  documentation for django-googledrive-storage for which a URL is
  provided at the top of this document, as well its implementation
  details visible on its GitHub page.
'''
class GoogleDriveTests(TestCase):

    def test_exists(self):
        """
        simple test to see if Google Drive storage can be accessed
        """
        gd_storage = GoogleDriveStorage()
        self.assertTrue(gd_storage.exists('/'))

    def test_upload_delete(self):
        """
        test if an image file can be successfully uploaded then deleted
        """
        gd_storage = GoogleDriveStorage()
        
        # make sure file not present in GD
        gd_storage.delete('/gd_test.png')
        self.assertFalse(gd_storage.exists('/gd_test.png'),
            'Cannot test upload because file already exists')
        
        '''
          Follows the method used in a Stack Overflow answer by user
          Danilo Cabello to create a fake PNG image file to test Google
          Drive upload
        '''
        img = SimpleUploadedFile("gd_test.png", b"PNG", content_type="image/png")
        gd_storage.save(name='/gd_test.png', content=img)
        
        # make sure image upload successful
        self.assertTrue(gd_storage.exists('/gd_test.png'),
            'Image upload failed')
        
        # delete newly uploaded image
        gd_storage.delete('/gd_test.png')
        
        # make sure image removal successful
        self.assertFalse(gd_storage.exists('/gd_test.png'),
            'Image delete failed')

# test the like function of recipe 
class LikeTests(TestCase):

    # test to see if a user can like a recipe 
    def test_like_recipe(self):
        demoRecipe = Recipe.objects.create(
            title="test_recipe_1",
            intro="here is intro to my recipe",
            time=timedelta(hours=1),
        )
        # test to see demoRecipe has default 0 likes 
        self.assertEqual(0, demoRecipe.likes.count())

        # login
        authenticate(self.client)

        # user django test func to mimic pressing the like button 
        form_data = {'input_id' : demoRecipe.pk}
        url = reverse('wordofmouth:like_post', args=(demoRecipe.pk,))
        response = self.client.post(url, form_data, secure=True)

        # test to see the page did not respond 404 and the number if like become 1 
        self.assertNotEqual(response.status_code, 404)
        self.assertEqual(1, demoRecipe.likes.count())
    
    def test_unlike_recipe(self):
        demoRecipe = Recipe.objects.create(
            title="test_recipe_1",
            intro="here is intro to my recipe",
            time=timedelta(hours=1),
        )
        # test to see demoRecipe has default 0 likes 
        self.assertEqual(0, demoRecipe.likes.count())

        # login
        authenticate(self.client)

        # user django test func to mimic pressing the like button 
        form_data = {'input_id' : demoRecipe.pk}
        url = reverse('wordofmouth:like_post', args=(demoRecipe.pk,))
        response = self.client.post(url, form_data, secure=True)

        # test to see the page did not respond 404 and the number if like become 1 
        self.assertNotEqual(response.status_code, 404)
        self.assertEqual(1, demoRecipe.likes.count())

        # unlike the recipe now 
        form_data = {'input_id' : demoRecipe.pk}
        url = reverse('wordofmouth:unlike_post', args=(demoRecipe.pk,))
        response = self.client.post(url, form_data, secure=True)
        self.assertNotEqual(response.status_code, 404)
        self.assertEqual(0, demoRecipe.likes.count())
    
    def test_recipe_display_numlikes(self):
        demoRecipe = Recipe.objects.create(
            title="test_recipe_1",
            intro="here is intro to my recipe",
            time=timedelta(hours=1),
        )
        # test to see demoRecipe has default 0 likes 
        self.assertEqual(0, demoRecipe.likes.count())

        # login 
        authenticate(self.client)

        # user django test func to mimic pressing the like button 
        form_data = {'input_id' : demoRecipe.pk}
        url = reverse('wordofmouth:like_post', args=(demoRecipe.pk,))
        response = self.client.post(url, form_data, secure=True)
        url2 = reverse('wordofmouth:recipe_detail', args=(demoRecipe.pk,))
        response2 = self.client.get(url2, secure=True)
        # test to see if the response has the correct output
        self.assertContains(response2, '- 1')


class commentTest(TestCase):
    def test_create_comment(self):
        demoRecipe = Recipe.objects.create(
            title="test_recipe_1",
            intro="here is intro to my recipe",
            time=timedelta(hours=1),
        )
        
        # login
        authenticate(self.client)
        
        form_data = {'comment' : demoRecipe.pk, "comment_text" : "new comment!!!"}
        url = reverse('wordofmouth:comment_post', args=(demoRecipe.pk,))
        response = self.client.post(url, form_data, secure=True)
        # self.assertContains(response, 'new comment!!!')
        url2 = reverse('wordofmouth:recipe_detail', args=(demoRecipe.pk,))
        response2 = self.client.get(url2, secure=True)
        # test to see if the response has the correct output
        self.assertContains(response2, 'new comment!!!')


class ratingTest(TestCase):
    def test_create_rating(self):
        demoRecipe = Recipe.objects.create(
            title="test_recipe_1",
            intro="here is intro to my recipe",
            time=timedelta(hours=1),
        )
        
        # login
        authenticate(self.client)
        
        form_data = {'rate' : demoRecipe.pk, "rate_num" : 5}
        url = reverse('wordofmouth:rate_post', args=(demoRecipe.pk,))
        response = self.client.post(url, form_data, secure=True)
        url2 = reverse('wordofmouth:recipe_detail', args=(demoRecipe.pk,))
        response2 = self.client.get(url2, secure=True)
        
        # test to see if the response has the correct output
        self.assertContains(response2, 'Rating: 5')

class HeaderTests(TestCase):
    #test to see if header links are all functional in header bar
    def test_header_links(self):
        # login
        authenticate(self.client)

        # load page
        url = reverse('wordofmouth:add_recipe')
        response = self.client.get(url, secure=True)
        self.assertNotContains(response, 'Please login to access this page')

class ForkRecipeViewTests(TestCase):
    # test to see if forking creates and links new child recipe
    def test_makechild(self):
        # login
        authenticate(self.client)
        
        # fork
        demoRecipe = Recipe.objects.create(
            title="test_recipe_1",
            intro="here is intro to my recipe",
            time=timedelta(hours=1),
        )
        form_data = {
            'Title' : 'forked recipe',
            'Intro' : 'new intro',
            'Time[days]' : '0',
            'Time[hours]' : '1',
            'Time[minutes]' : '2',
            'Time[seconds]' : '3',
            }
        url = reverse('wordofmouth:fork_recipe', args=(demoRecipe.pk,))
        response = self.client.post(url, form_data, secure=True)
        
        # check children
        child = demoRecipe.children.all()
        self.assertEqual(len(child), 1)
        
    # test to see if forked child has a parent
    def test_parent(self):
        # login
        authenticate(self.client)
        
        # fork
        demoRecipe = Recipe.objects.create(
            title="test_recipe_1",
            intro="here is intro to my recipe",
            time=timedelta(hours=1),
        )
        form_data = {
            'Title' : 'forked recipe',
            'Intro' : 'new intro',
            'Time[days]' : '0',
            'Time[hours]' : '1',
            'Time[minutes]' : '2',
            'Time[seconds]' : '3',
            }
        url = reverse('wordofmouth:fork_recipe', args=(demoRecipe.pk,))
        response = self.client.post(url, form_data, secure=True)
        
        # check parent
        child = demoRecipe.children.all()
        self.assertEqual(len(child[0].parent.all()), 1)
        self.assertEqual(child[0].parent.all()[0], demoRecipe)
        
    # test to see if inheritance preserved on delete
    def test_inheritance(self):
        # login
        authenticate(self.client)
        
        demoRecipe = Recipe.objects.create(
            title="test_recipe_1",
            intro="here is intro to my recipe",
            time=timedelta(hours=1),
        )
        form_data = {
            'Title' : 'forked recipe',
            'Intro' : 'new intro',
            'Time[days]' : '0',
            'Time[hours]' : '1',
            'Time[minutes]' : '2',
            'Time[seconds]' : '3',
            }
        
        # fork a child and grandchild
        url = reverse('wordofmouth:fork_recipe', args=(demoRecipe.pk,))
        response = self.client.post(url, form_data, secure=True)
        forkRecipe1 = demoRecipe.children.all()[0]
        
        url = reverse('wordofmouth:fork_recipe', args=(forkRecipe1.pk,))
        response = self.client.post(url, form_data, secure=True)
        forkRecipe2 = forkRecipe1.children.all()[0]
        
        # check parent/child/grandchild relationships
        self.assertEqual(demoRecipe.children.all()[0], forkRecipe1)
        self.assertEqual(forkRecipe1.children.all()[0], forkRecipe2)
        self.assertEqual(forkRecipe2.parent.all()[0], forkRecipe1)
        self.assertEqual(forkRecipe1.parent.all()[0], demoRecipe)
        
        # delete child
        forkRecipe1.delete()
        
        # check that original recipe and grandchild are now parent/child
        self.assertEqual(len(demoRecipe.children.all()), 1)
        self.assertEqual(len(forkRecipe2.parent.all()), 1)
        self.assertEqual(demoRecipe.children.all()[0], forkRecipe2)
        self.assertEqual(forkRecipe2.parent.all()[0], demoRecipe)


class SearchRecipeViewTests(TestCase):
    def test_searched_blank_input(self):

        url = reverse('wordofmouth:search_recipes')
        response = self.client.get(url, secure=True)
        self.assertContains(response, 'Hey')

    def test_searched_recipe_input(self):

        demoRecipe = Recipe.objects.create(
            title="test_recipe_1",
            intro="here is intro to my recipe",
            time=timedelta(hours=1),
        )
        form_data = {
            'Title': 'forked recipe',
            'Intro': 'new intro',
            'Time[days]': '0',
            'Time[hours]': '1',
            'Time[minutes]': '2',
            'Time[seconds]': '3',
        }
        url = reverse('wordofmouth:add_recipe')
        #response = self.client.post(url, form_data)

        form_data = {
            'searched': 'pancake',
        }

        url = reverse('wordofmouth:search_recipes')
        response = self.client.post(url, form_data, secure=True)
        self.assertContains(response, 'pancake')
