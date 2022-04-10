from django.urls import path
from . import views

app_name='newsapp'
urlpatterns=[
	path('',views.index,name='index'),
    path('subscribe-source',views.source,name='source'),
    path('feeds',views.feeds,name='feeds'),

    # Category wise news
    path('business-news',views.business,name='business'),
    path('health-news',views.health,name='health'),
    path('science-news',views.science,name='science'),
    path('sports-news',views.sports,name='sports'),
    path('technology-news',views.technology,name='technology'),
    path('entertainment-news',views.entertainment,name='entertainment'),

    # News from different sources
    path('bbc-news',views.bbc,name='bbc'),
    path('cbc-news',views.cbc,name='cbc'),
    path('toi-news',views.toi,name='toi'),
    path('techradar-news',views.techradar,name='techradar'),
    path('news24-news',views.news24,name='news24'),


    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('registration',views.registration,name='registration'),
    path('forgot-password',views.forgotPassword,name='forgotPassword'),
    path('reset-password',views.resetPassword,name='resetPassword'),
]