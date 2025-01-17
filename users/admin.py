from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Users

class UsersAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    search_fields = ('email',)
    ordering = ('date_joined',)
    readonly_fields = ('otp_code', 'otp_expiry')

    fieldsets = (
        (None, {
            'fields': ('email', 'is_staff', 'is_active', 'date_joined')
        }),
        (_('OTP Information'), {
            'fields': ('otp_code', 'otp_expiry'),
            'classes': ('collapse',),  # This will make the OTP fields collapsible
        }),
    )

    def has_change_permission(self, request, obj=None):
        # Optionally, you can restrict who can change certain fields
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        # Optionally, you can restrict who can delete users
        return False  # Prevent deletion of users

# Register the Users model with the custom admin class
admin.site.register(Users, UsersAdmin)





