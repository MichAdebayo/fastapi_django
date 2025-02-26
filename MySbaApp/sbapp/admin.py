from django.contrib import admin
from .models import LoanRequest , UserProfile
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    def save_model(self, request, obj, form, change):
        """Ensure passwords are hashed when saving users in the admin panel."""
        if not change or ('password' in form.changed_data):  # Ensure proper condition check
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)

class LoanRequestAdmin(admin.ModelAdmin):
    readonly_fields = ('loan_nr_chk_dgt',)  # Prevent manual input

# register the custom UserAdmin
admin.site.register(UserProfile, CustomUserAdmin)
admin.site.register(LoanRequest, LoanRequestAdmin)
