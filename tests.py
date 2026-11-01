from unittest.mock import patch
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse
from .models import CarMake, CarModel

class BestCarsTests(TestCase):
    def test_home_lists_actual_dealer_results(self):
        with patch('djangoapp.views.proxy',side_effect=[[{'id':1,'full_name':'Unit Test Dealer','state':'Kansas','city':'Topeka','address':'123 Main St','zip':'66601'}],
                                                    [{'state':'Kansas'}]]):
            response=self.client.get('/')
        self.assertEqual(response.status_code,200)
        self.assertContains(response,'Unit Test Dealer')

    def test_register_login_logout(self):
        response=self.client.post('/djangoapp/register',data='{"userName":"tester","firstName":"Test","lastName":"User","email":"test@example.com","password":"TestPass123!"}',content_type='application/json')
        self.assertEqual(response.status_code,201)
        response=self.client.post('/djangoapp/login',data='{"userName":"tester","password":"TestPass123!"}',content_type='application/json')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json()['status'],'Authenticated')
        response=self.client.get('/djangoapp/logout')
        self.assertEqual(response.json()['userName'],'')

    def test_duplicate_registration_rejected(self):
        User.objects.create_user(username='tester',password='TestPass123!')
        res=self.client.post('/djangoapp/register',data='{"userName":"tester","email":"test@example.com","password":"TestPass123!"}',content_type='application/json')
        self.assertEqual(res.status_code,409)

    def test_car_models_json(self):
        make=CarMake.objects.create(name='Toyota')
        CarModel.objects.create(car_make=make,name='Camry',year=2024,type='Sedan')
        response=self.client.get('/djangoapp/get_cars')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json()['CarModels'][0]['CarMake'],'Toyota')

    def test_review_post_requires_login(self):
        res=self.client.post('/djangoapp/add_review',data='{"dealership":1,"review":"Fantastic"}',content_type='application/json')
        self.assertEqual(res.status_code,302)

    def test_logged_in_review_submission(self):
        user=User.objects.create_user(username='tester',password='TestPass123!')
        self.client.force_login(user)
        with patch('djangoapp.views.proxy',return_value={'id':3,'review':'Fantastic'}) as mock_proxy:
            result=self.client.post('/djangoapp/add_review',data='{"dealership":1,"review":"Fantastic services"}',content_type='application/json')
        self.assertEqual(result.status_code,201)
        self.assertEqual(mock_proxy.call_args.args[0],'/insert_review')
