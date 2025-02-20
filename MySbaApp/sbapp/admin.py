from django.contrib import admin
from .models import LoanRequestUserProfile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class CustomUserAdmin(UserAdmin):
    def save_model(self, request, obj, form, change):
        """Ensure passwords are hashed when saving users in the admin panel."""
        if not change or ('password' in form.changed_data):  # Ensure proper condition check
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)

class LoanRequestUserProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('LoanNr_ChkDgt',)  # Prevent manual input

# Unregister the default UserAdmin and register the custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Register your models here.
admin.site.register(LoanRequestUserProfile, LoanRequestUserProfileAdmin)
