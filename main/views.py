from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse
from .models import Manual, Profile
import requests , json
import jwt
import os
from dotenv import load_dotenv
from urllib.parse import urlencode
from django.contrib.auth.models import User
from django.db import models
from .shop_cart import shop_cart

load_dotenv()

def index(request):
    manuals = Manual.objects.all()

    shop_cartinfo = shop_cart(request) 

    shop_items = {
            'manuals': manuals,
            'item': shop_cartinfo.shop_cart,
            'total' : shop_cartinfo.get_total()
        }

    return render(request, 'main/index.html', shop_items)

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, 'Please fill in all fields')
            return redirect('index')

        try:
            user = User.objects.get(email=email)

            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name}')
                return redirect('index')
            else:
                messages.error(request, 'Invalid password')
                return redirect('index')
            
        except User.DoesNotExist:
            messages.error(request, 'User does not exist')
            return redirect('index')

    return redirect('index')

def user_logout(request):
    
    logout(request)

    return redirect('index')

def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
    
        if User.objects.filter(email=email).exists():
            return render(request, 'main/index.html', {'error': 'Email is alredy used'})
        else:
            User.objects.create_user(email=email, password=password, username=username)
            return redirect('index')
    
    return render(request, 'main/index.html')

def google_login(request):
    client_id = os.getenv('GOOGLE_CLIENT_ID')
    redirect_uri = 'http://localhost:8000/auth/callback'
    scope = "openid email profile"
    response_type = "code"
    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'response_type': response_type,
        'scope': scope,
        'access_type': 'offline'
    }   

    url_google = f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"
    return redirect(url_google)

def google_callback(request):
    code = request.GET.get('code')
    token_url = 'https://oauth2.googleapis.com/token'
    data = {
        'client_id': os.getenv('GOOGLE_CLIENT_ID'),
        'client_secret': os.getenv('GOOGLE_CLIENT_SECRET'),
        'code': code,
        'redirect_uri': 'http://localhost:8000/auth/callback',
        'grant_type': 'authorization_code'
    }
    token_response = requests.post(token_url, data=data)
    tokens = token_response.json()
    access_token = tokens.get('access_token')
    id_token = tokens.get('id_token')

    userinfo_url = 'https://www.googleapis.com/oauth2/v3/userinfo'
    headers = {'Authorization': f'Bearer {access_token}'}
    userinfo_response = requests.get(userinfo_url, headers=headers)
    userinfo = userinfo_response.json()

    user = user_exist_vefication(userinfo)
    login(request, user)
    return redirect('index.html')

def user_exist_vefication(userinfo):
    email = userinfo['email']
    try:
        user = User.objects.get(email=email)
        return user
    except User.DoesNotExist:
        user = User.objects.create_user(
            username=email,
            email=email,
            first_name=userinfo.get('name', '')
        )
        Profile.objects.create(
            user=user,
            avatar_url=userinfo.get('picture',''),
            google_id=userinfo.get('sub', '')
        )
        return 

def add_to_cart(request):

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            manual_id = data.get("manual_id")

            if not manual_id:
                return JsonResponse({"error": "No manual_id"}, status=400)

            cart = shop_cart(request)
            cart.add(manual_id)

            print("CART:", cart.shop_cart)

            return JsonResponse({
                "count": len(cart)
            })

        except Exception as e:
            print("ERROR:", e)
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)

def remove_to_cart(request):

    if request.method == 'POST':
        manual_id = request.POST.get('manual_id')

        actual_cart = shop_cart(request)

        actual_cart.remove(manual_id)

        return redirect('index')

def clear_cart(request):

    if request.method == 'POST':

        actual_cart = shop_cart(request)

        actual_cart.clear()

        return redirect('index')
