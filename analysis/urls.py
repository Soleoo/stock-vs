from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    # outras rotas
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
]
