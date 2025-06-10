from django.contrib import admin
from django.urls import path

from . import views

from django.contrib.auth import views as auth_views

from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to my site!")

urlpatterns = [
    path('/',home),
    path('admin/', admin.site.urls),
    path('register/', views.register,name='register'),
    path('login/', views.login,name='login'),
    path('logout/', views.logout_view,name='logout'),
    path('profile/', views.profile,name='profile'),
    
    # Password reset urls
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
