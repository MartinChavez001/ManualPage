from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import Manual, Profile
import requests
import jwt
import os
from dotenv import load_dotenv
from urllib.parse import urlencode
from django.contrib.auth.models import User
from django.db import models

load_dotenv()

def index(request):
    manuals = Manual.objects.all()
    return render(request, 'main/index.html', {'manuals' : manuals})

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
    return redirect('index')

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
        return user