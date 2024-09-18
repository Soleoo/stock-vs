from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>', views.product_detail, name='product_detail'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<int:pk>/edit/', views.product_update, name='product_update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('products/<int:product_id>/items/', views.product_item_list, name='product_item_list'),
    path('product-items/create/', views.product_item_create, name='product_item_create'),
    path('product-items/<str:serial_number>/', views.product_item_detail, name='product_items_detail'),
    path('product-items/<int:pk>/edit/', views.product_item_update, name='product_item_update'),
    path('product-items/<int:pk>/delete/', views.product_item_delete, name='product_item_delete'),
    path('generate_serial_and_qrcode/', views.generate_serial_and_qrcode, name='generate_serial_and_qrcode'),
    path('scan-qrcode/', views.scan_qrcode, name='scan_qrcode')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)