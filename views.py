"""Authenticated dealership web app and JSON API proxy to local Node services."""
import json
import os
import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel

DEALER_API = os.environ.get('DEALER_API', 'http://127.0.0.1:3030').rstrip('/')
SENTIMENT_API = os.environ.get('SENTIMENT_API', 'http://127.0.0.1:5050').rstrip('/')

def proxy(endpoint, method='GET', payload=None):
    try:
        response = requests.request(method, DEALER_API + endpoint, json=payload, timeout=6)
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError):
        return None

def json_body(request):
    try:
        value = json.loads(request.body or b'{}')
        return value if isinstance(value, dict) else None
    except (ValueError, UnicodeError):
        return None

@csrf_exempt
def login_user(request):
    if request.method != 'POST': return HttpResponseNotAllowed(['POST'])
    data = json_body(request)
    if data is None: return JsonResponse({'error': 'Valid JSON object required'}, status=400)
    username = data.get('userName', '')
    user = authenticate(request, username=username, password=data.get('password',''))
    if user is None: return JsonResponse({'userName':username, 'status':'Unauthenticated'}, status=401)
    login(request, user)
    return JsonResponse({'userName': user.username, 'status': 'Authenticated'})

def logout_user(request):
    if request.method not in ('GET','POST'): return HttpResponseNotAllowed(['GET','POST'])
    logout(request)
    return JsonResponse({'userName':''})

@csrf_exempt
def register_user(request):
    if request.method != 'POST': return HttpResponseNotAllowed(['POST'])
    data = json_body(request)
    if data is None: return JsonResponse({'error': 'Valid JSON required'}, status=400)
    username = data.get('userName','').strip()
    email = data.get('email','').strip()
    password = data.get('password','')
    if not username or not email or len(password) < 8:
        return JsonResponse({'error':'Username, email and password (8+ characters) required'},status=400)
    try:
        User.objects.create_user(username=username,email=email,password=password,
                                 first_name=data.get('firstName','').strip(),last_name=data.get('lastName','').strip())
    except IntegrityError:
        return JsonResponse({'error':'Username already exists'},status=409)
    return JsonResponse({'userName':username,'status':'Registered'},status=201)

def get_cars(request):
    cars = list(CarModel.objects.select_related('car_make').order_by('car_make__name','name')
                .values('id','name','type','year','car_make__name'))
    return JsonResponse({'CarModels':[{'CarMake':x['car_make__name'], 'CarModel':x['name'],
                                      'ModelYear':x['year'], 'ModelType':x['type']} for x in cars]})

def get_dealers(request,state=None):
    data = proxy('/fetchDealers' + ('/'+state if state else ''))
    if data is None: return JsonResponse({'error':'Dealership service unavailable'},status=503)
    return JsonResponse({'status':200,'dealers':data})

def get_dealer(request,dealer_id):
    data = proxy('/fetchDealer/'+str(dealer_id))
    if data is None: return JsonResponse({'error':'Dealership service unavailable'},status=503)
    return JsonResponse({'status':200,'dealer':data if isinstance(data,list) else [data]})

def get_reviews(request,dealer_id):
    data = proxy('/fetchReviews/dealer/'+str(dealer_id))
    if data is None: return JsonResponse({'error':'Review service unavailable'},status=503)
    return JsonResponse({'status':200,'reviews':data})



@csrf_exempt
@login_required
def add_review(request):
    if request.method != 'POST': return HttpResponseNotAllowed(['POST'])
    data = json_body(request)
    if data is None: return JsonResponse({'error':'Valid JSON required'},status=400)
    text = str(data.get('review','')).strip()
    try: dealer_id = int(data.get('dealership',0))
    except (ValueError,TypeError): return JsonResponse({'error':'Invalid dealer ID'}, status=400)
    if not text or dealer_id <= 0: return JsonResponse({'error':'Dealer and review required'},status=400)
    allowed = ('purchase','purchase_date','car_make','car_model','car_year')
    payload = {key:data.get(key) for key in allowed}
    payload.update({'name':request.user.username,'dealership':dealer_id,'review':text})
    result = proxy('/insert_review','POST',payload)
    if result is None: return JsonResponse({'error':'Review service unavailable'},status=503)
    return JsonResponse({'status':201,'review':result},status=201)

def home(request):
    state = request.GET.get('state','').strip()
    data = proxy('/fetchDealers' + ('/'+state if state else ''))
    states = sorted({d['state'] for d in (proxy('/fetchDealers') or []) if isinstance(d,dict) and d.get('state')})
    return render(request,'home.html',{'dealers':data or [],'states':states,'selected_state':state,
                                       'service_error':data is None})

def dealer_page(request,dealer_id):
    detail = proxy('/fetchDealer/'+str(dealer_id))
    if isinstance(detail,list): detail = detail[0] if detail else None
    reviews = proxy('/fetchReviews/dealer/'+str(dealer_id))
    return render(request,'dealer.html',{'dealer':detail,'reviews':reviews or [],'dealer_id':dealer_id})

@login_required
def post_review_page(request,dealer_id):
    detail = proxy('/fetchDealer/'+str(dealer_id))
    if isinstance(detail,list): detail=detail[0] if detail else None
    makes = CarMake.objects.prefetch_related('models').all()
    if request.method == 'POST':
        text = request.POST.get('review','').strip()
        if not text: return render(request,'post_review.html',{'dealer':detail,'dealer_id':dealer_id,
                                            'makes':makes,'error':'Review is required'})
        data = {'dealership':dealer_id, 'name':request.user.username,'review':text,
                'purchase':request.POST.get('purchase') == 'on',
                'purchase_date':request.POST.get('purchase_date',''),
                'car_make':request.POST.get('car_make',''),
                'car_model':request.POST.get('car_model',''),
                'car_year':request.POST.get('car_year','')}
        saved = proxy('/insert_review','POST',data)
        if saved is not None: return redirect('dealer-page',dealer_id=dealer_id)
        return render(request,'post_review.html',{'dealer':detail,'dealer_id':dealer_id,
                                       'makes':makes,'error':'Unable to save review'})
    return render(request,'post_review.html',{'dealer':detail,'dealer_id':dealer_id,'makes':makes})
