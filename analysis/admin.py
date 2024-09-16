from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .forms import UserRegistrationForm

class UserAdmin(BaseUserAdmin):
    form = UserRegistrationForm

    list_display = ('username', 'email', 'is_staff')
    list_filter = ('is_staff',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions')

    actions = ['delete_selected_users']

    def delete_selected_users(self, request, queryset):
        for user in queryset:
            user.delete()

if admin.site.is_registered(User):
    admin.site.unregister(User)

admin.site.register(User, UserAdmin)