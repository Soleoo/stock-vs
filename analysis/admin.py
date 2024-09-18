from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Product, ProductItem
from .forms import UserRegistrationForm

class UserAdmin(BaseUserAdmin):
    form = UserRegistrationForm

    list_display = ('username', 'email', 'full_name', 'phone_number', 'role', 'access_level', 'user_id', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_active', 'role')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'full_name', 'phone_number', 'face_image', 'user_id')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Role and Access', {'fields': ('role', 'access_level')}),
        ('Important dates', {'fields': ('last_login', 'last_recognition_time', 'created_at')}),
    )
    readonly_fields = ('created_at',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'full_name', 'password1', 'password2', 'role', 'access_level', 'user_id'),
        }),
    )
    search_fields = ('username', 'email', 'full_name')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions')

    actions = ['delete_selected_users']

    def delete_selected_users(self, request, queryset):
        for user in queryset:
            user.delete()

if admin.site.is_registered(User):
    admin.site.unregister(User)

admin.site.register(User, UserAdmin)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'stock', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'updated_at')

    def delete_selected_users(self, request, queryset):
        for item in queryset:
            item.delete()

@admin.register(ProductItem)
class ProductItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'serial_number', 'created_at', 'updated_at')
    search_fields = ('serial_number',)
    list_filter = ('created_at', 'updated_at')
    raw_id_fields = ('product',)

    actions = ['delete_selected_users']

    def delete_selected_users(self, request, queryset):
        for item in queryset:
            item.delete()