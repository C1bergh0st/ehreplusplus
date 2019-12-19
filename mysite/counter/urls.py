"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('rank/', views.rank, name='rank'),
    path('search/', views.search, name='search'),
    path('issue/create/<int:gangid>/', views.createIssue, name='createIssue'),
    path('issue/all/', views.allIssues, name='allIssues'),
    path('issue/<int:id>/', views.issue, name='issue'),
    path('issue/<int:issue_id>/vote/<str:approve>', views.vote, name='vote'),
    path('profile/<int:id>/', views.profile, name='profile'),
    path('redirectToUserProfile/', views.redirectToUserProfile, name='redirectToUserProfile'),
    path("accounts/profile/", views.redirectToHomePage, name='redirectToHomePage'),
    path("gang/mygangs/", views.mygangs, name='mygangs'),
    path("gang/create/", views.createGang, name='createGang'),
    path("gang/<int:id>/settings/", views.gangSettings, name='gangSettings'),
    path("gang/<int:id>/change/<int:uid>/<str:approve>/", views.gangChange, name='gangChange'),
    path("gang/<int:id>/request/", views.gangRequest, name='gangRequest'),
    path("gang/<int:id>/", views.gang, name='gang'),
]
