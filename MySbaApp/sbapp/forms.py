from django import forms
from .models import LoanRequest, UserProfile
# from django.utils.html import format_html
# from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import make_password
# from django.forms import DateInput
# # from .models import Appointment


class UserSignupForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput, label="Password"
    )  # Password field with hidden input

    class Meta:
        model = UserProfile
        fields = ["username", "email", "password"]  # Fields displayed in the form
        #fields = [
        #    "first_name", 'last_name', 'username', 'email', 'address', 'phone_number'
        #]


    def save(self, commit=True):
        user = super().save(
            commit=False
        )  # Create a user object without saving it to the database yet
        user.password = make_password(
            self.cleaned_data["password"]
        )  # Hash the password before saving
        if commit:
            user.save()  # Save the user to the database

        return user

class UserLoginForm(forms.Form):

    username = forms.CharField(
        max_length=150, label="Username"
    )  # Field for the username
    password = forms.CharField(
        widget=forms.PasswordInput, label="Password"
    )  # Password field with hidden input

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = [
            'username', 'first_name', 'last_name', 'email', 'address', 'phone_number',
        ]

class LoanRequestForm(forms.ModelForm):
    class Meta:
        model = LoanRequest
        fields = [ 'name',
            # 'name', 'city', 'state', 'zip', 'bank',
            # 'bank_state', 'naics', 'term','no_emp', 'new_exist',
            #  'create_job', 'retained_job', 'franchise_code',
            # 'urban_rural', 'rev_line_cr', 'low_doc', 'gr_appv', 
        ]

        # widgets = {
        #     'gr_appv': forms.NumberInput(attrs={'step': '0.01'}),
        # }
# class ApprovalSimulationForm(forms.ModelForm):
 
#     class Meta:
#         model = LoanRequest
#         fields = ['State', 'Bank', 'NAICS', "Term", "NoEmp", 
#                   "NewExist", "CreateJob", 'RetainedJob', 'UrbanRural', 
#                   "RevLineCr", "LowDoc", 'GrAppv']


# class ChangePasswordForm(PasswordChangeForm):

#     def __init__(self, *args, **kwargs):
#         """
#         Initializes the ChangePasswordForm with custom labels, help text, and styles.

#         Customizes the labels of the password fields, adds helpful text to 
#         guide users on password requirements, and applies Tailwind CSS styles
#         to the form fields for consistent styling.
#         """
#         super().__init__(*args, **kwargs)

#         # Customize labels for password fields
#         self.fields["old_password"].label = "Current Password"
#         self.fields["new_password1"].label = "New Password"
#         self.fields["new_password2"].label = "Confirm New Password"

#         # Add help text for new password requirements
#         self.fields["new_password1"].help_text = format_html(
#             '<ul class="text-sm text-gray-600 mt-2">'
#             "<li>Your password must be at least 8 characters long.</li>"
#             "<li>Your password cannot be entirely numeric.</li>"
#             "<li>Your password cannot be too similar to your other personal information.</li>"
#             "</ul>"
#         )

#         # Add Tailwind CSS classes to form fields for styling
#         for field in self.fields:
#             self.fields[field].widget.attrs.update(
#                 {
#                     "class": "w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-cyan-400",
#                 })
            

# # class AppointmentForm(forms.ModelForm):

# #     class Meta:
# #         model = Appointment
# #         fields = ['reason', 'date', 'time']
# #         widgets = {
# #             'date': DateInput(attrs={'type': 'date', 'class': 'form-control w-full bg-gray-100 rounded-md p-2'}),
# #         }

# #     def clean_time(self):

# #         time = self.cleaned_data.get('time')
# #         try:
# #             if not time:
# #                 raise forms.ValidationError("This field is required.")
# #             hour, minute = map(int, time.split(":"))
# #             if not (0 <= hour < 24 and 0 <= minute < 60):
# #                 raise forms.ValidationError("Enter a valid time in HH:MM format.")
# #         except ValueError:
# #             raise forms.ValidationError("Time should be in HH:MM format.")
# #         return time