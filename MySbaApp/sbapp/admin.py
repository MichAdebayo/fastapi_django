from django.contrib import admin
from sbapp.models import LoanRequest, UserProfile
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    def save_model(self, request, obj, form, change):
        """Ensure passwords are hashed when saving users in the admin panel."""
        if 'password' in form.changed_data:  # Only hash if password is changed
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)

class LoanRequestAdmin(admin.ModelAdmin):
    readonly_fields = ('loan_nr_chk_dgt',)  # Prevent manual input

# Register custom admin models
admin.site.register(UserProfile, CustomUserAdmin)
admin.site.register(LoanRequest, LoanRequestAdmin)
