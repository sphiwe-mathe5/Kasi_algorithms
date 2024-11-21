from django.urls import path
from django.contrib.auth import views as auth_views
from submit import views as user_views
from .views import register

urlpatterns = [
    #path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='submit/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='submit/logout.html'), name='logout'),
    path('profile/', user_views.profile, name='profile'),

]
