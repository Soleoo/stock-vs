from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .forms import UserRegistrationForm

class UserAdmin(BaseUserAdmin):
    form = UserRegistrationForm

    list_display = ('username', 'email', 'full_name', 'phone_number', 'role', 'access_level', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_active', 'role')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'full_name', 'phone_number', 'face_image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Role and Access', {'fields': ('role', 'access_level')}),
        ('Important dates', {'fields': ('last_login', 'last_recognition_time', 'created_at')}),
    )
    readonly_fields = ('created_at',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'full_name', 'password1', 'password2', 'role', 'access_level'),
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