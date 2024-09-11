from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .forms import UserRegistrationForm

class UserAdmin(BaseUserAdmin):
    form = UserRegistrationForm

    list_display = ('username', 'email', 'is_staff')
    list_filter = ('is_staff',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff',)}),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)
    filter_horizontal = ()

    actions = ['delete_selected_users']

    def delete_selected_users(self, request, queryset):
        queryset.delete()
    delete_selected_users.short_description = "Delete selected users"

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
