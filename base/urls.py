from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('logout', views.logoutUser, name="logout"),

    path('settings', views.settings, name="settings"),
    path('profile/<str:pk>/', views.profile, name="profile"),

    path('upload', views.upload, name="upload"),

    path('like-post/<str:id>', views.like_post, name="like-post"),
]