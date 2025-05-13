from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile

class UserProfileAdmin(UserAdmin):
    model = UserProfile
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'user_type', 'registration_id', 'department']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_type', 'registration_id', 'department')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('user_type', 'registration_id', 'department')}),
    )

admin.site.register(UserProfile, UserProfileAdmin)
