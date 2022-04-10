from newsapp.models import Category
from django.http import response
from django.shortcuts import render,redirect
import requests
from .models import Category, UserCategory, UserSource, Source
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.core.mail import send_mail
import environ

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()
API_KEY = env('KEY')

# Create your views here.

# REGISTRATION
def registration(request):
    if request.method == 'POST':
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        email = request.POST['mail']
        password = request.POST['password']
        password2 = request.POST['password2']
        print(fname,' ',lname,' ',password)
        if User.objects.filter(email=email).exists():
            messages.info(request,'Email Already Registered')
            return redirect('/registration')
        else:
            user = User.objects.create_user(first_name=fname,last_name=lname,username=email, password = password,email=email)
            user.save()
            subject = 'Confirmation Mail'
            message = f'Hello {user.first_name},\n You have successfully registered to NewsApp. '
            email_from = 'newsapp.alert@gmail.com'
            recepient_list = [user.email,] 
            send_mail(subject,message,email_from,recepient_list)
            return redirect('/login')
    else:
        return render(request,'register.html')

# LOGIN
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')        
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('/login')
    else:
        return render(request,'login.html')

# LOGOUT
def logout(request):
    auth.logout(request)
    return redirect('/')

# FORGOT PASSWORD
def forgotPassword(request):
    if request.method == 'POST':
        username = request.POST['username']
        users=User.objects.all()
        for user in users:
            if user.username == username:
                request.session['name'] = username
                subject = 'Reset Password Mail'
                message = f'Hello {user.first_name}, There is an attempt to reset your password.\nClick the below link to reset your password.\n \nhttp://127.0.0.1:8000/reset-password'
                email_from = 'newsapp.alert@gmail.com'
                recepient_list = [user.email,] 
                send_mail(subject,message,email_from,recepient_list)
                messages.success(request,'A link to reset your password is sent to your registered mail. ')
                return redirect('/forgot-password')        
        else:
            messages.info(request,'Invalid Email')
            return redirect('/forgot-password')
    else:
        return render(request,'forgetPassword.html')

# RESET PASSWORD
def resetPassword(request):
    if request.method == 'POST':
        username = request.session.get('name')
        password1 = request.POST['password']
        password2 = request.POST['password2']
        if password1 == password2:
            user = User.objects.get(username=username)
            user.set_password(password1)
            user.save();
            return redirect('/login')
        else:
            messages.info(request,'Password not matched')
            return redirect('/reset-password')
    else:
        return render(request,'resetPassword.html')

# HOME PAGE/ TOP STORIES
def index(request):
    url = f'https://newsapi.org/v2/top-headlines?pageSize=20&language=en&apiKey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    articles = data['articles']
    context = {
        'articles' : articles
    }
    return render(request,'index.html',context)

# SUBSCRIBE SOURCE
def source(request):
    source_user = {}
    a={}
    sources = Source.objects.all()
    if request.method == 'POST':
        source = request.POST.getlist('source[]')
        source_lst = [int(i) for i in source]
        current_user = request.user
        for s in sources:
            if s.id in source_lst:
                subscription = True
            else:
                subscription  = False
            if UserSource.objects.filter(user_id=current_user.id,source_id=s.id).exists():
                obj = UserSource.objects.filter(user_id=current_user.id).get(source_id=s.id)
                obj.subscription = subscription
                obj.save();
            else:
                obj1 = UserSource(subscription = subscription,user_id=current_user.id, source_id=s.id)
                obj1.save();
        return redirect('/feeds')
    else:
        current_user = request.user
        user_source = UserSource.objects.filter(user_id=current_user.id)
        for i in user_source:
            source_user = {i.source_id : i.subscription}
            a.update(source_user)
        context = {
        'sources' : sources,
        'a':a
        }
    return render(request,'subscribe.html',context)

#  PERSONALIZED FEED
def feeds(request):
    current_user = request.user
    source_list=[]
    sources = Source.objects.all()
    categories = Category.objects.all()
    user_source = UserSource.objects.filter(user_id=current_user.id)
    for x in user_source:
        for y in sources:
            if x.subscription == True:
                if x.source_id == y.id:
                    source_list.append(y.source)
    source = ','.join(source_list)
    print(source)
    url1 = f'https://newsapi.org/v2/top-headlines?sources={source}&language=en&apiKey={API_KEY}'
    #url1 = f'https://newsapi.org/v2/sources?language=en&apiKey={API_KEY}'
    response1 = requests.get(url1)    
    data1 = response1.json()
    articles = data1['articles']
    context = {
            'articles' : articles,
            'categories' : categories
        }
    return render(request,'feeds.html',context)

# CATEGORY WISE NEWS

# BUSINESS NEWS
def business(request):
    url = f'https://newsapi.org/v2/top-headlines?pageSize=20&language=en&category=business&apiKey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    articles = data['articles']
    context = {
        'articles' : articles
    }
    return render(request,'category/business_news.html',context)

# HEALTH NEWS
def health(request):
    url = f'https://newsapi.org/v2/top-headlines?pageSize=20&language=en&category=health&apiKey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    articles = data['articles']
    context = {
        'articles' : articles
    }
    return render(request,'category/health_news.html',context)

# SCIENCE NEWS
def science(request):
    url = f'https://newsapi.org/v2/top-headlines?pageSize=20&language=en&category=science&apiKey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    articles = data['articles']
    context = {
        'articles' : articles
    }
    return render(request,'category/science_news.html',context)

# SPORTS NEWS
def sports(request):
    url = f'https://newsapi.org/v2/top-headlines?pageSize=20&language=en&category=sports&apiKey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    articles = data['articles']
    context = {
        'articles' : articles
    }
    return render(request,'category/sports_news.html',context)

# TECHNOLOGY NEWS
def technology(request):
    url = f'https://newsapi.org/v2/top-headlines?pageSize=20&language=en&category=technology&apiKey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    articles = data['articles']
    context = {
        'articles' : articles
    }
    return render(request,'category/technology_news.html',context)

# ENTERTAINMENT NEWS
def entertainment(request):
    url = f'https://newsapi.org/v2/top-headlines?pageSize=20&language=en&category=entertainment&apiKey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    articles = data['articles']
    context = {
        'articles' : articles
    }
    return render(request,'category/entertainment_news.html',context)


# NEWS SOURCES

# BBC-NEWS
def bbc(request):
    url = f'https://newsapi.org/v2/everything?pageSize=20&sources=bbc-news&language=en&apiKey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    articles = data['articles']
    context = {
        'articles' : articles
    }
    return render(request,'source/bbc.html',context)

# CBC-NEWS
def cbc(request):
    url = f'https://newsapi.org/v2/everything?pageSize=20&sources=cbc-news&language=en&apiKey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    articles = data['articles']
    context = {
        'articles' : articles
    }
    return render(request,'source/cbc.html',context)

# THE TIMES OF INDIA
def toi(request):
    url = f'https://newsapi.org/v2/everything?pageSize=20&sources=the-times-of-india&language=en&apiKey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    articles = data['articles']
    context = {
        'articles' : articles
    }
    return render(request,'source/toi.html',context)

# TECHRADAR
def techradar(request):
    url = f'https://newsapi.org/v2/everything?pageSize=20&sources=techradar&language=en&apiKey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    articles = data['articles']
    context = {
        'articles' : articles
    }
    return render(request,'source/techradar.html',context)

# NEWS24
def news24(request):
    url = f'https://newsapi.org/v2/everything?pageSize=20&sources=news24&language=en&apiKey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    articles = data['articles']
    context = {
        'articles' : articles
    }
    return render(request,'source/news24.html',context)