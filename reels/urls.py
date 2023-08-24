from django.urls import path
from . import views

urlpatterns = [
    path('instagram_oauth/', views.instagram_oauth, name='instagram_oauth'),
    path('instagram_oauth/callback/', views.instagram_oauth_callback, name='instagram_oauth_callback'),
]

