from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, FormView, DetailView
from .models import UserProfile, LoanRequest #, Job, ContactMessage, PredictionHistory, Appointment,Availability, 
from .forms import UserSignupForm, UserProfileForm, LoanRequestForm, AdminAuthenticationForm, AdminProfileForm # ChangePasswordForm, PredictChargesForm, AppointmentForm
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model,logout, login 
from django.shortcuts import get_object_or_404
import requests, logging # random
from django.http import JsonResponse
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.forms import AuthenticationForm
# import json
from django.views.decorators.csrf import csrf_exempt
# from django.conf import settings
# from django.views import View 
# from django.contrib.admin.views.decorators import staff_member_required
# from django.db.models import Avg
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse


from MySbaApp.settings import PREDICTION_SERVICE_URL


class HomeView(TemplateView):
    template_name = 'sbapp/home.html'  # Home Page View Template


class SignupView(CreateView):

    model = UserProfile
    form_class = UserSignupForm
    template_name = 'sbapp/signup.html'
    success_url = reverse_lazy('user_login')


class UserLoginView(LoginView):
    template_name = 'sbapp/user_login.html'
    authentication_form = AuthenticationForm
    redirect_authenticated_user = False

    def form_valid(self, form):
        user = form.get_user()

        # Prevent staff or superusers from logging in through this view
        if user.is_staff or user.is_superuser:
            form.add_error(None, "Admins cannot log in from the user portal.")
            return self.form_invalid(form)  # Re-render login form with error

        # Handle "Remember Me" functionality
        remember_me = self.request.POST.get("remember_me", None) is not None
        if not remember_me:
            self.request.session.set_expiry(0)  # Expire session on browser close
        else:
            self.request.session.set_expiry(1209600)  # Session lasts 2 weeks

        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("user_dashboard")  # Redirect non-admin users to their dashboard

    
class UserDashboardView(LoginRequiredMixin, TemplateView):

    template_name = 'sbapp/user_dashboard.html'

    
class UserProfileView(LoginRequiredMixin, UpdateView):

    model = get_user_model()
    form_class = UserProfileForm
    template_name = 'sbapp/user_profile.html'
    success_url = reverse_lazy('user_profile') 

    def get_object(self, queryset=None):
        return self.request.user
    
    def form_valid(self, form):
        # Explicitly save the form
        user = form.save(commit=False)  # Get the user object without saving it yet
        user.save()
        messages.success(self.request, 'Your profile has been updated successfully!')
        return super().form_valid(form)  # Proceed with the normal response
    
    def form_invalid(self, form):
        """Handles invalid form submissions and provides error messages."""
        messages.error(self.request, 'There was an error updating your profile. Please try again.')
        return super().form_invalid(form)

class LoanRequestCreateView(LoginRequiredMixin, CreateView):
    model = LoanRequest
    form_class = LoanRequestForm
    template_name = 'sbapp/user_loan_request.html'
    success_url = reverse_lazy('user_loan_request_success') # Redirect after successful form submission

    def form_valid(self, form):
        form.instance.user = self.request.user  # Assign the logged-in user
        return super().form_valid(form)

        
class LoanRequestSuccessView(TemplateView):
    template_name = 'sbapp/user_loan_request_success.html'

class LoanRequestStatusView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = "sbapp/user_loan_status.html"  # Render status page directly
    form_class = LoanRequestForm
    success_message = "Your loan request has been submitted successfully."

    def form_valid(self, form):
        """
        Saves the loan request and passes its details to the template.
        """
        loan_request = form.save(commit=False)
        loan_request.user = self.request.user  # Assign the logged-in user
        loan_request.status = "Pending"  # Default status
        loan_request.save()

        # Pass loan request details to the template
        context = self.get_context_data(form=form)
        context.update({
            'loan_request_id': loan_request.id,
            'loan_amount': loan_request.gr_appv,  # Adjust field name if needed
            'loan_status': loan_request.loan_status,
        })
        return self.render_to_response(context)



class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and \
               (self.request.user.is_staff or self.request.user.is_superuser)
    
    def handle_no_permission(self):
        return redirect('admin_login')



# _________________________________________
#
#  region AdminLoginView
# _________________________________________
 

class AdminLoginView(LoginView):
    template_name = 'sbapp/admin_user_login.html'
    authentication_form = AdminAuthenticationForm  
    redirect_authenticated_user = False  

    def get_success_url(self):
        return reverse_lazy('admin_user_dashboard')

    def form_valid(self, form):
        """
        Handle successful form submission.
        Authenticate the user locally, fetch the JWT token from FastAPI, and store it in the session.
        """
        # Authenticate the user locally
        user = form.get_user()

        # Check if the user has admin privileges
        if not user.is_staff and not user.is_superuser:
            logout(self.request)
            messages.error(self.request, "You don't have admin privileges")
            return self.form_invalid(form)

        # Get the email and password of the authenticated user
        email = user.email
        password = form.cleaned_data['password']

        # Authenticate with the FastAPI /auth/login endpoint
        try:
            fastapi_url = f"{PREDICTION_SERVICE_URL}/auth/login"
            auth_data = {
                "email": email,
                "password": password,
            }
            response = requests.post(fastapi_url, json=auth_data)

            # Check if the request was successful
            if response.status_code == 200:
                # Extract the JWT token from the response
                token_data = response.json()
                jwt_token = token_data.get("access_token")

                if not jwt_token:
                    messages.error(self.request, "Failed to retrieve JWT token from the prediction service.")
                    return self.form_invalid(form)

                # Store the token in the session
                self.request.session["jwt_token"] = jwt_token
            else:
                # Handle failed authentication with FastAPI
                error_message = response.json().get("detail", "Unknown error")
                messages.error(self.request, f"Failed to authenticate with the prediction service: {error_message}")
                return self.form_invalid(form)
        except requests.RequestException as e:
            # Handle network-related errors (e.g., FastAPI server is down)
            messages.error(self.request, f"Network error during authentication: {str(e)}")
            return self.form_invalid(form)
        except Exception as e:
            # Handle unexpected exceptions
            messages.error(self.request, f"Unexpected error during authentication: {str(e)}")
            return self.form_invalid(form)

        # Set session expiry based on "Remember Me"
        if self.request.POST.get('remember_me'):
            self.request.session.set_expiry(1209600)  # 2 weeks
        else:
            self.request.session.set_expiry(0)  # Session expires when browser is closed

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Add additional context data for the template.
        """
        context = super().get_context_data(**kwargs)
        context['is_admin_login'] = True
        return context
    

# _________________________________________
#
#  region AdminDashboardView
# _________________________________________

class AdminDashboardView(AdminRequiredMixin, TemplateView):
    template_name = 'sbapp/admin_user_dashboard.html'


# _________________________________________
#
#  region AdminProfileView
# _________________________________________

class AdminProfileView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserProfile
    form_class = AdminProfileForm
    template_name = "sbapp/admin_user_profile.html"
    success_url = reverse_lazy("admin_user_profile")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.save()
        messages.success(self.request, "Profile updated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error updating your profile. Please check your inputs.")
        return super().form_invalid(form)

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser
    

# _________________________________________
#
#  region SimpleView
# _________________________________________
from django.views import View
from django.shortcuts import render
from .models import LoanRequest

# Configure logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('sbapp.views')

class SimpleDataView(View):
    def get(self, request, *args, **kwargs):
        # Fetch the first loan request for simplicity
        try:
            loan = LoanRequest.objects.first()
            if loan:
                api_data = loan.to_api_data()  # Use the to_api_data method from the model
                
                # Fetch token from FastAPI
                token = self.get_jwt_token()
                
                # Send data to prediction endpoint
                prediction_result = self.send_to_prediction_endpoint(api_data, token)
                
                return render(request, 'sbapp/simple_data.html', {'api_data': api_data, 'token': token, 'prediction_result': prediction_result})
            else:
                return render(request, 'sbapp/simple_data.html', {'api_data': None, 'token': None, 'prediction_result': None})
        except Exception as e:
            print(f"Exception: {str(e)}")
            return render(request, 'sbapp/simple_data.html', {'api_data': None, 'token': None, 'prediction_result': None})

    def get_jwt_token(self):
        """
        Retrieve the JWT token by authenticating with FastAPI's /auth/login endpoint.
        """
        try:
            # Define the FastAPI login endpoint URL
            fastapi_login_url = f"{PREDICTION_SERVICE_URL}/auth/login"
            
            # Replace these with actual credentials or retrieve them from a secure source
            credentials = {
                "email": "mike@test.com",
                "password": "obitochan"
            }
            
            response = requests.post(fastapi_login_url, json=credentials)
            
            if response.status_code == 200:
                token = response.json().get('access_token')
                logger.info(f"Token retrieved successfully: {token}")
                return token
            else:
                logger.error(f"Failed to retrieve token. Status code: {response.status_code}, Response: {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error during token retrieval: {str(e)}")
            print(f"Exception: {str(e)}")
            return None

    def send_to_prediction_endpoint(self, api_data, token):
            """
            Send the formatted data and token to the FastAPI prediction endpoint.
            """
            try:
                if not token:
                    logger.error("No token available.")
                    return None
                
                # Define the FastAPI prediction endpoint URL
                fastapi_prediction_url = f"{PREDICTION_SERVICE_URL}/loans/request"
                
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                }

                print(f"Sending data to prediction endpoint: {api_data}")
                response = requests.post(fastapi_prediction_url, json=api_data, headers=headers)
                print(f"Response status code: {response.status_code}")
                print(f"Response content: {response.content}")
                
                if response.status_code == 200:
                    response_json = response.json()  # Decode the byte string into a Python dictionary
                    print(f"Response JSON: {response_json}")  # Print the full JSON response
                    prediction_result = response_json.get('approval_status')  # Extract the approval_status field
                    logger.info(f"Prediction result received: {prediction_result}")
                    return prediction_result
                else:
                    logger.error(f"Failed to get prediction. Status code: {response.status_code}, Response: {response.text}")
                    return None
            except Exception as e:
                logger.error(f"Error during prediction: {str(e)}")
                print(f"Exception: {str(e)}")
                return None
# _________________________________________
#
#  region AdminLoanRequestView
# _________________________________________

import requests
import json

def get_jwt_token(request):
    """Retrieve JWT token from session or authenticate."""
    if 'jwt_token' in request.session:
        print("JWT Token retrieved from session:", request.session['jwt_token'])
        return request.session['jwt_token']

    response = requests.post(
        f"{PREDICTION_SERVICE_URL}/auth/login",
        json={'email': 'mike@test.com', 'password': 'obitochan'}
    )
    
    if response.status_code == 200:
        token = response.json().get('access_token')
        print("JWT Token retrieved from login:", token)
        request.session['jwt_token'] = token
        return token
    else:
        print("Failed to retrieve JWT token:", response.status_code, response.content)
    return None

def send_api_request(url, method, data=None, headers=None, max_retries=3):
    """Send API request with retry mechanism."""
    for attempt in range(max_retries):
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                print("Sending POST request with data:", data)
                print("Sending POST request with headers:", headers)
                response = requests.post(url, json=data, headers=headers)
            
            if response.status_code == 200:
                print("Response content:", response.json())
                return response.json()
            else:
                print(f"Attempt {attempt + 1}: Failed with status code {response.status_code}")
                print("Response content:", response.text)
                if attempt < max_retries - 1:
                    print("Retrying...")
                else:
                    print("Max retries reached. Exiting.")
                    return None
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1}: Request failed with exception: {e}")
            if attempt < max_retries - 1:
                print("Retrying...")
            else:
                print("Max retries reached. Exiting.")
                return None

    return None


from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils import timezone
from .models import LoanRequest
import json

class AdminLoanRequestView(LoginRequiredMixin, ListView):
    model = LoanRequest
    template_name = 'sbapp/admin_user_loan_request.html'
    context_object_name = 'loan_applications'

    def get_queryset(self):
        return LoanRequest.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add status counts
        context['pending_loans_count'] = LoanRequest.objects.filter(loan_status='Pending').count()
        context['approved_loans_count'] = LoanRequest.objects.filter(loan_status='Approved').count()
        context['rejected_loans_count'] = LoanRequest.objects.filter(loan_status='Rejected').count()
        
        # Enhance loan objects with view state
        for loan in context['loan_applications']:
            if loan.loan_status == 'Pending':
                loan.view_state = 'INITIAL'
                loan.custom_status = 'Pending'
                #loan.last_updated = 'No prediction yet'
            else:
                loan.view_state = 'FINAL'
                loan.custom_status = self.get_custom_status(loan.loan_status)
                #loan.last_updated = loan.updated_at_utc
        
        return context

    def post(self, request, *args, **kwargs):
        predict_id = request.POST.get('predict_id')
        update_id = request.POST.get('update_id')
        status = request.POST.get('status')

        if predict_id:
            self.handle_prediction(predict_id, request)
        elif update_id and status:
            self.handle_status_update(update_id, status, request)

        return JsonResponse({'success': True})

    def handle_prediction(self, loan_id, request):
        loan = LoanRequest.objects.filter(loan_nr_chk_dgt=loan_id).first()
        if not loan:
            return JsonResponse({'error': 'Loan not found'}, status=404)

        token = get_jwt_token(request)
        if not token:
            return JsonResponse({'error': 'Failed to retrieve JWT token'}, status=400)

        api_data = loan.to_api_data()
        headers = {'Authorization': f'Bearer {token}'}

        if response := send_api_request(
            f"{PREDICTION_SERVICE_URL}/loans/request",
            'POST',
            data=api_data,
            headers=headers,
        ):
            print("API Response:", response)
            if approval_status := response.get('approval_status'):
                if approval_status.lower() == 'approve':
                    loan.loan_status = 'Approved'
                elif approval_status.lower() == 'reject':
                    loan.loan_status = 'Rejected'
                else:
                    loan.loan_status = 'Pending'
                #loan.updated_at_utc = timezone.now()
                loan.save()

                # Update loan object with new status
                loan.custom_status = self.get_custom_status(approval_status)
                #loan.last_updated = loan.updated_at_utc
            else:
                self._extracted_from_handle_prediction_31(loan)
        else:
            self._extracted_from_handle_prediction_31(loan)
        return JsonResponse({'success': True})

    def _extracted_from_handle_prediction_31(self, loan):
        # Handle API errors
        loan.view_state = 'ERROR'
        loan.custom_status = 'Prediction failed'
        loan.save()

    def handle_status_update(self, loan_id, new_status, request):
        loan = LoanRequest.objects.filter(loan_nr_chk_dgt=loan_id).first()
        if not loan:
            return JsonResponse({'error': 'Loan not found'}, status=404)

        if new_status not in ['Pending', 'Approved', 'Rejected']:
            return JsonResponse({'error': 'Invalid status'}, status=400)

        loan.loan_status = new_status
        #loan.updated_at_utc = timezone.now()
        loan.save()

        # Update loan object with new status
        loan.custom_status = self.get_custom_status(new_status)
        #loan.last_updated = loan.updated_at_utc

        return JsonResponse({'success': True})

    @staticmethod
    def get_custom_status(status):
        match status:
            case 'Approved': 
                return 'Will be fully repaid'
            case 'Rejected': 
                return 'Will default on repayment'
            case _:
                return 'Pending'



from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import LoanRequest

@csrf_exempt
def update_loan_status(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request'}, status=400)
    update_id = request.POST.get('update_id')
    status = request.POST.get('status')

    loan = LoanRequest.objects.filter(loan_nr_chk_dgt=update_id).first()
    if not loan:
        return JsonResponse({'error': 'Loan not found'}, status=404)

    if status not in ['Pending', 'Approved', 'Rejected']:
        return JsonResponse({'error': 'Invalid status'}, status=400)

    loan.loan_status = status
    loan.updated_at_utc = timezone.now()
    loan.save()

    return JsonResponse({'success': True})


#_________________________________________
#  region AboutView
# _________________________________________
class AboutView(TemplateView):
    template_name = 'sbapp/about.html'  # About Us View Template

# _________________________________________
#
#  region ServicesView
# _________________________________________
class ServicesView(TemplateView):
    template_name = 'sbapp/services.html'  # Services View Template

# _________________________________________
#
#  region BlogView
# _________________________________________
class BlogView(TemplateView):
    template_name = 'sbapp/blog.html'  # Blog View Template

# _________________________________________
#
#  region TestimonialView
# _________________________________________
class TestimonialView(TemplateView):
    template_name = 'sbapp/testimonial.html'  # Testimonial View Template

# _________________________________________
#
#  region ContactView
# _________________________________________
class ContactView(TemplateView):
    template_name = 'sbapp/contact.html'  # Contact View Template

# _________________________________________
#
#  region ContactSupportView
# _________________________________________
class ContactSupportView(TemplateView):
    template_name = 'sbapp/contact_support.html'  # User Contact View Template

# _________________________________________
#
#  region WorkshopsView
# _________________________________________
class WorkshopsView(TemplateView):
    template_name = 'sbapp/workshops.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['workshops'] = [
            {
                'title': 'Introduction to Django', 
                'date': '2025-02-28', 
                'location': 'Online', 
                'description': 'Learn the basics of a successful loan request.'
            },
            {
                'title': 'Different Grant Types', 
                'date': '2025-03-15', 
                'location': 'New York', 
                'description': 'Explore the different grants available.'
            },
            {
                'title': 'AI & ML Workshop', 
                'date': '2025-04-01', 
                'location': 'London', 
                'description': 'Leveraging AI and Machine Learning for successful loan application.'
            }
        ]
        return context
    
# _________________________________________
#
#  region BusinessResourcesView
# _________________________________________
class BusinessResourcesView(LoginRequiredMixin, TemplateView):
    """
    A view providing users with business resources and guides.

    Features:
        - Displays loan application guides
        - Provides financial planning tools
        - Links to helpful external resources
    """
    template_name = "sbapp/business_resources.html"

    def get_context_data(self, **kwargs):
        """
        Adds business resources to the context.
        """
        context = super().get_context_data(**kwargs)

        # Example resources (could be fetched from a database model)
        context['resources'] = [
            {"title": "How to Improve Your Loan Approval Chances", "link": "#"},
            {"title": "Financial Planning for Small Businesses", "link": "#"},
            {"title": "Understanding SBA Loan Programs", "link": "#"},
            {"title": "How to Build Business Credit", "link": "#"},
        ]

        return context
    
# class LoanStatusView(LoginRequiredMixin, TemplateView):
#     """
#     A view to check the status of a user's loan applications.

#     Displays the submitted applications and their current approval status.
    
#     Features:
#         - Shows pending, approved, and rejected applications
#         - Displays approval dates and financial details
#     """
#     template_name = "sbapp/user_loan_status.html"

#     def get_context_data(self, **kwargs):
#         """
#         Fetches loan applications and adds them to the context.
#         """
#         context = super().get_context_data(**kwargs)
#         user = self.request.user

#         # Retrieve all loan applications for the logged-in user
#         context['loan_applications'] = LoanRequest.objects.filter(user=user).order_by('-approval_date')

#         return context
    






# To handle client messages submission
# def contact_view_user(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         email = request.POST.get("email")
#         message = request.POST.get("message")

#         # Save the message to the database
#         ContactMessage.objects.create(name=name, email=email, message=message)

#         # Show a success message
#         messages.success(request, "Your message has been sent successfully!")
#         return redirect('contact_form')  # Replace 'contact' with the name of your URL pattern

#     return render(request, "insurance_app/contact_form_user.html")






# class UserLoginView(LoginView):
#     template_name = 'sbapp/login.html'
#     authentication_form = AuthenticationForm
#     redirect_authenticated_user = True

#     def get_success_url(self):
#         logger.debug(f"Login successful for user: {self.request.user}")
#         return reverse_lazy('home')
    
#     def dispatch(self, request, *args, **kwargs):
#         if self.request.user.is_authenticated:
#             return redirect('home')
#         return super().dispatch(request, *args, **kwargs)
    
#     def form_invalid(self, form):
#         logger.warning(f"Login failed: {form.errors}")
#         return super().form_invalid(form)

#     def form_valid(self, form):
#         remember_me = self.request.POST.get('remember_me', None) is not None

#         if not remember_me:
#             self.request.session.set_expiry(0)  # Expire session on browser close
#         else:
#             self.request.session.set_expiry(1209600)  # Session lasts 2 weeks

#         return super().form_valid(form)
        
            # remember_me = self.request.POST.get('remember_me', None) is not None

            # if not remember_me:
            #     self.request.session.set_expiry(0)  # Expire session on browser close
            # else:
            #     self.request.session.set_expiry(1209600)  # Session lasts 2 weeks

            # # Add the API call here (FastAPI login verification)
            # fastapi_url = "http://localhost:8000/auth/login"  # URL for the FastAPI login endpoint
            # payload = {
            #     'email': form.cleaned_data['email'],
            #     'password': form.cleaned_data['password']
            # }

            # # Send a POST request to FastAPI
            # response = requests.post(fastapi_url, json=payload)

            # if response.status_code == 200 and response.json().get('authenticated'):
            #     # Handle successful login
            #     return super().form_valid(form)
            
            # # Handle failed login (maybe display an error message)
            # form.add_error(None, "Invalid credentials or FastAPI verification failed.")
            # return self.form_invalid(form)



# class HealthAdvicesView(TemplateView):
#     """Renders the health advices page.

#     Provides a view for the application's health advices page.
#     """
#     template_name = 'insurance_app/health_advices.html'  # Assur'Cares Section View Template


# class CybersecurityAwarenessView(TemplateView):
#     """Renders the cybersecurity awareness page.

#     Provides a view for the application's cybersecurity awareness page.
#     """
#     template_name = 'insurance_app/cybersecurity_awareness.html'    # Cybersecurity Section View Template


# #Welcome view (used to modified homepage)
# class WelcomeView(TemplateView):
#     """Renders the welcome page.

#     Provides a view for the application's welcome page.
#     """
#     template_name = 'insurance_app/welcome.html' 


# #To handle non-client messages submission
# def contact_view(request):
#     """
#     Handles the contact form submission and displays the contact form.

#     This view processes POST requests to capture user input (name, email, and message),
#     saves the message in the database, and displays a success message before redirecting 
#     the user back to the contact page. For GET requests, it renders the contact form.

#     Args:
#         request (HttpRequest): The HTTP request object.

#     Returns:
#         HttpResponse:
#             - If POST: Redirects to the contact page after saving the message.
#             - If GET: Renders the 'contact_form.html' template.
#     """
#     if request.method == "POST":
#         name = request.POST.get("name")
#         email = request.POST.get("email")
#         message = request.POST.get("message")

#         # Save the message to the database
#         ContactMessage.objects.create(name=name, email=email, message=message)

#         # Show a success message
#         messages.success(request, "Your message has been sent successfully!")
#         return redirect('contact')  # Replace 'contact' with the name of your URL pattern

#     return render(request, "insurance_app/contact_form.html")




# @staff_member_required
# def message_list_view(request):
#     """
#     Displays a list of contact messages for staff members.

#     This view retrieves all contact messages from the database, orders them by submission 
#     time in descending order (most recent first), and renders them in a template. 
#     Access to this view is restricted to staff members.

#     Args:
#         request (HttpRequest): The HTTP request object.

#     Returns:
#         HttpResponse: Renders the 'messages_list.html' template with the following context:
#             - `messages` (QuerySet): A list of all contact messages, ordered by submission time.
#     """
#     messages = ContactMessage.objects.all().order_by('-submitted_at')  # Most recent first
#     return render(request, "insurance_app/messages_list.html", {"messages": messages})


# @csrf_exempt
# def solve_message(request, message_id):
#     """
#     Handles the deletion of a contact message.

#     This view processes a POST request to delete a specific contact message by its ID.
#     If the message exists, it is deleted, and a success response is returned.
#     If the message does not exist, an error response is returned.
#     Only POST requests are allowed; other request methods will result in an error response.

#     Args:
#         request (HttpRequest): The HTTP request object.
#         message_id (int): The ID of the contact message to be deleted.

#     Returns:
#         JsonResponse:
#             - If successful: {'success': True}
#             - If the message is not found: {'success': False, 'error': 'Message not found.'} (HTTP 404)
#             - If the request method is invalid: {'success': False, 'error': 'Invalid request method.'} (HTTP 400)
#     """
#     if request.method == 'POST':
#         try:
#             contact_message = ContactMessage.objects.get(id=message_id)
#             contact_message.delete()
#             return JsonResponse({'success': True})
#         except ContactMessage.DoesNotExist:
#             return JsonResponse({'success': False, 'error': 'Message not found.'}, status=404)
#     return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)


# @login_required
# def book_appointment(request):
#     """
#     Handles appointment booking for authenticated users.

#     This view allows users to book an appointment using an appointment form. 
#     It also displays the user's upcoming and past appointments.

#     Functionality:
#     - If the request is POST, it processes the appointment form.
#     - Saves the appointment if the form is valid, associating it with the logged-in user.
#     - Displays success messages upon successful booking.
#     - Redirects back to the booking page after submission.
#     - If the request is GET, it renders the appointment form.
#     - Retrieves and displays the user's upcoming and past appointments.

#     Args:
#         request (HttpRequest): The HTTP request object.

#     Returns:
#         HttpResponse: Renders the `book_appointment.html` template with:
#             - `today` (date): The current date.
#             - `form` (AppointmentForm): The form for booking an appointment.
#             - `upcoming_appointments` (QuerySet): The user's upcoming appointments, ordered by date.
#             - `past_appointments` (QuerySet): The user's past appointments, ordered by date (descending).
#     """
#     today = timezone.now().date()  # Get today's date in YYYY-MM-DD format
    
#     # Handle form submission (POST request)
#     if request.method == 'POST':
#         form = AppointmentForm(request.POST)
#         if form.is_valid():
#             # Save the appointment data
#             appointment = form.save(commit=False)
#             appointment.user = request.user  # Associate the logged-in user
#             appointment.save()

#             messages.success(request, 'Your appointment has been booked successfully!')
#             return redirect('book_appointment')  # Redirect to the same page after saving
#     else:
#         form = AppointmentForm()

#     # Get upcoming and past appointments for display
#     upcoming_appointments = Appointment.objects.filter(
#         user=request.user, date__gte=today
#     ).order_by('date')

#     past_appointments = Appointment.objects.filter(
#         user=request.user, date__lt=today
#     ).order_by('-date')

#     return render(request, 'insurance_app/book_appointment.html', {
#         'today': today,
#         'form': form,
#         'upcoming_appointments': upcoming_appointments,
#         'past_appointments': past_appointments,
#     })


# def get_available_times(request):
#     """
#     Retrieves available time slots for a given date.

#     This function handles a GET request with a 'date' parameter and returns 
#     the available time slots for that date in JSON format. If no availability 
#     is found, an empty list is returned.

#     Args:
#         request (HttpRequest): The HTTP request object containing GET parameters.

#     Returns:
#         JsonResponse: A JSON response containing the available time slots in the format:
#             {
#                 "times": [list of available time slots]
#             }
#             If no availability is found or no date is provided, an empty list is returned.
#     """
#     if date := request.GET.get('date'):
#         try:
#             availability = Availability.objects.get(date=date)
#             return JsonResponse({"times": availability.time_slots})
#         except Availability.DoesNotExist:
#             return JsonResponse({"times": []})
#     return JsonResponse({"times": []})







# class ChangePasswordView(PasswordChangeView):
#     """
#     Handles password change requests.

#     This view allows users to change their password. If the form is valid, it saves the new 
#     password, displays a success message, and redirects the user to their profile page.

#     Attributes:
#         form_class (Form): The form used for password change.
#         template_name (str): The name of the template used to display the response.
#         success_url (str): The URL to redirect to after a successful password change.

#     Methods:
#         form_valid(form):
#             Processes the form submission. Saves the new password, shows a success message, 
#             and returns the response.

#     Args:
#         request (HttpRequest): The HTTP request object.
#         form (Form): The form containing the user's input.

#     Returns:
#         HttpResponse: Redirects to the profile page upon successful password change.
#     """
#     form_class = ChangePasswordForm  
#     template_name = 'insurance_app/changepassword.html'
#     success_url = reverse_lazy('profile')
    
#     def form_valid(self, form):
#         # Save the new password
#         response = super().form_valid(form)
#         # Add a success message
#         messages.success(self.request, 'Your password has been changed successfully!')
#         return response


# class UserLogoutView(LoginRequiredMixin, View):
#     """
#     Handles user logout requests with a confirmation step.

#     This view provides a confirmation page for users who want to log out, and handles 
#     the actual logout process when the user submits the request.

#     Attributes:
#         template_name (str): The name of the template used to display the logout confirmation page.
#         next_page (str): The URL to redirect to after the logout process is complete.

#     Methods:
#         get(request):
#             Displays the logout confirmation page to the user.

#         post(request):
#             Handles the logout action. Logs the user out and renders the confirmation page.

#     Args:
#         request (HttpRequest): The HTTP request object.

#     Returns:
#         HttpResponse: 
#             - GET request: Renders the logout confirmation page.
#             - POST request: Logs the user out and renders the confirmation page.
#     """
#     template_name = 'insurance_app/logout_user.html'
#     next_page = reverse_lazy('logout_user')

#     def get(self, request):
#         # Handle GET requests with confirmation page
#         user = self.request.user
#         return render(request, self.template_name, {'user': user})
    
#     def post(self, request):
#         # Handle actual logout
#         user = self.request.user
#         logout(request)
#         return render(request, self.template_name, {'user': user})



# class PredictChargesView(LoginRequiredMixin, UpdateView):
#     """
#     Allows users to update their profile and predicts insurance charges based on input.

#     This view allows logged-in users to update their profile information, such as age, 
#     height, weight, number of children, and smoking status. Upon successful form submission, 
#     it uses a pre-trained model to predict the user's insurance charges based on the updated 
#     information and displays the prediction.

#     Attributes:
#         model (Model): The model representing the user profile.
#         form_class (Form): The form class used for capturing user input.
#         template_name (str): The name of the template used for rendering the form and prediction results.
#         success_url (str): The URL to redirect to after successful form submission.

#     Methods:
#         get_object(queryset=None):
#             Returns the current user object for updating the profile.

#         form_valid(form):
#             Validates and processes the form data, updates the user profile, 
#             generates a prediction, and displays the prediction results.

#         form_invalid(form, error_message):
#             Handles invalid form submissions and returns an error message.

#         categorize_bmi(bmi):
#             Categorizes the user's BMI into weight categories (underweight, normal, overweight, obese).

#         categorize_age(age):
#             Categorizes the user's age into life stages (young adult, early adulthood, mid adulthood, late adulthood).

#         preprocess_data(data):
#             Prepares the input data by performing necessary transformations and encoding for prediction.

#         load_model():
#             Loads the pre-trained model from a pickle file for prediction.

#     Args:
#         request (HttpRequest): The HTTP request object.
#         form (Form): The form containing user input.
#         prediction_value (float): The predicted insurance charges based on the user's profile.

#     Returns:
#         HttpResponse: 
#             - On success: Renders the template with the predicted charges and recent prediction history.
#             - On error: Returns a form with an error message.
#     """
#     model = get_user_model()
#     form_class = PredictChargesForm
#     template_name = 'insurance_app/predict.html'
#     success_url = reverse_lazy('predict')

#     def get_object(self, queryset=None):
#         return self.request.user

#     def form_valid(self, form):
#         user_profile = self.get_object()
        
#         # Update and save user profile
#         user_profile.age = form.cleaned_data['age']
#         user_profile.weight = form.cleaned_data['weight']
#         user_profile.height = form.cleaned_data['height']
#         user_profile.num_children = form.cleaned_data['num_children']
#         user_profile.smoker = form.cleaned_data['smoker']
#         user_profile.save()  # Uncommented to persist changes

#         # Validate inputs
#         if user_profile.height <= 0:
#             return self.form_invalid(form, "Invalid height value")

#         # Calculate BMI using model property
#         try:
#             bmi = user_profile.bmi
#         except ZeroDivisionError:
#             return self.form_invalid(form, "Invalid height value (cannot be zero)")

#         # Create prediction data
#         prediction_data = {
#             "age": user_profile.age,
#             "bmi": bmi,
#             "smoker": user_profile.smoker,
#             "children": user_profile.num_children,
#             "region": user_profile.region,
#             "sex": user_profile.sex
#         }

#         # Preprocess and predict
#         preprocessed_data = self.preprocess_data(prediction_data)
#         model = self.load_model()
        
#         if not model:
#             return self.form_invalid(form, "Failed to load prediction model")

#         predicted_charges = model.predict(preprocessed_data)
#         prediction_value = round(predicted_charges[0], 2)

#         # Save prediction history
#         PredictionHistory.objects.create(
#             user=user_profile,
#             age=user_profile.age,
#             weight=user_profile.weight,
#             height=user_profile.height,
#             num_children=user_profile.num_children,
#             smoker=user_profile.smoker,
#             region=user_profile.region,
#             sex=user_profile.sex,
#             predicted_charges=prediction_value
#         )

#         return self.render_to_response(self.get_context_data(
#             form=form,
#             predicted_charges=prediction_value,
#             recent_predictions=user_profile.insurance_predictions.all()[:5]
#         ))

#     def form_invalid(self, form, error_message):
#         messages.error(self.request, error_message)
#         return super().form_invalid(form)

#     def categorize_bmi(self, bmi):
#         if bmi < 18.5:
#             return "under_weight"
#         elif 18.5 <= bmi < 25:
#             return "normal_weight"
#         elif 25 <= bmi < 30:
#             return "over_weight"
#         else:
#             return "obese"

#     def categorize_age(self, age):
#         if 18 < age < 26:
#             return "young_adult"
#         elif 26 <= age < 36:
#             return "early_adulthood"
#         elif 36 <= age < 46:
#             return "mid_adulthood"
#         else:
#             return "late_adulthood"

#     def preprocess_data(self, data):
#         # Define the expected columns (must match the model's input requirements)
#         expected_columns = [
#             "smoker",
#             "age",
#             "bmi",
#             "age_category_young_adult",
#             "age_category_early_adulthood",
#             "bmi_category_over_weight",
#             "bmi_category_obese",
#             "children_str_0",
#         ]

#         # Create a DataFrame from the input data
#         df = pd.DataFrame([data])

#         # Convert smoker to binary (1 for "Yes", 0 for "No")
#         df["smoker"] = df["smoker"].map({"Yes": 1, "No": 0})

#         # Categorize age and bmi
#         df["age_category"] = df["age"].apply(self.categorize_age)
#         df["bmi_category"] = df["bmi"].apply(self.categorize_bmi)

#         # Convert children to string (for one-hot encoding)
#         df["children_str"] = df["children"].apply(lambda x: str(x))

#         # Perform one-hot encoding for categorical columns
#         df = pd.get_dummies(df, columns=["age_category", "bmi_category", "children_str"], dtype=(int))

#         # Ensure all expected columns are present
#         for col in expected_columns:
#             if col not in df.columns:
#                 df[col] = 0  # Add missing columns with default value 0

#         # Reorder columns to match the model's expectations
#         df = df[expected_columns]

#         return df

#     def load_model(self):
#         try:
#             model_path = os.path.join(settings.BASE_DIR, 'insurance_app/model/model.pkl')
#             with open(model_path, "rb") as file:
#                 model = pickle.load(file)
#             return model
#         except FileNotFoundError:
#             print("Error: The model file 'model.pkl' was not found.")
#             return None
#         except pickle.UnpicklingError:
#             print("Error: The file could not be unpickled. Ensure it is a valid pickle file.")
#             return None


# class PredictionHistoryView(LoginRequiredMixin, ListView):
#     """
#     Displays a list of prediction history for a logged-in user.

#     This view allows logged-in users to view their past insurance charge predictions, 
#     including the predicted charges and related details. The list is paginated, and users 
#     can see statistics such as the total number of predictions and the average predicted charges.

#     Attributes:
#         model (Model): The model representing the prediction history.
#         template_name (str): The name of the template used for rendering the prediction history page.
#         context_object_name (str): The name of the context variable for the list of predictions.
#         paginate_by (int): The number of predictions to display per page.

#     Methods:
#         get_queryset():
#             Returns a queryset containing the user's prediction history, 
#             ordered by timestamp and limited to the logged-in user.

#         get_context_data(**kwargs):
#             Adds extra context to the template, including the user profile, 
#             total predictions, and average predicted charges.

#     Args:
#         request (HttpRequest): The HTTP request object.
#         predictions (QuerySet): A list of `PredictionHistory` objects related to the current user.
#         total_predictions (int): The total number of prediction records for the current user.
#         average_charges (float): The average of the predicted charges for the user's history.

#     Returns:
#         HttpResponse:
#             - Renders the template with the user's prediction history, total number of predictions, 
#               and the average predicted charges.
#     """
#     model = PredictionHistory
#     template_name = 'insurance_app/prediction_history.html'
#     context_object_name = 'predictions'
#     paginate_by = 10

#     def get_queryset(self):
#         return self.model.objects.filter(user=self.request.user)\
#             .select_related('user')\
#             .order_by('-timestamp')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context.update({
#             'user_profile': self.request.user,
#             'total_predictions': self.get_queryset().count(),
#             'average_charges': self.get_queryset().aggregate(
#                 Avg('predicted_charges')
#             )['predicted_charges__avg']
#         })
#         return context