from django.shortcuts import render #, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, FormView, DetailView


from .prediction_service import PredictionService
from django.http import HttpResponseRedirect


from .models import UserProfile, LoanRequest #, Job, ContactMessage, PredictionHistory, Appointment,Availability, 
from .forms import UserSignupForm, UserProfileForm, LoanRequestForm #, ApplicationForm, ChangePasswordForm, PredictChargesForm, AppointmentForm
# from django.http import HttpResponse
import random
# from django.http import JsonResponse
# import json
# from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model #, login, logout, 
# from django.conf import settings
# from django.views import View 
# import pandas as pd
# import os
# from django.contrib.admin.views.decorators import staff_member_required
# from django.db.models import Avg
# from django.contrib.auth.decorators import login_required
# from django.utils import timezone
import requests
import logging
from django.contrib.auth.forms import AuthenticationForm


logger = logging.getLogger(__name__)

class HomeView(TemplateView):

    template_name = 'sbapp/home.html'  # Home Page View Template


class SignupView(CreateView):

    model = UserProfile
    form_class = UserSignupForm
    template_name = 'sbapp/signup.html'
    success_url = reverse_lazy('login')


class UserLoginView(LoginView):

    template_name = 'sbapp/login.html'
    authentication_form = AuthenticationForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('user_welcome')
    
    def form_valid(self, form):

        remember_me = self.request.POST.get('remember_me', None) is not None

        if not remember_me:
            self.request.session.set_expiry(0)  # Expire session on browser close
        else:
            self.request.session.set_expiry(1209600)  # Session lasts 2 weeks

        return super().form_valid(form)


class UserWelcomeView(LoginRequiredMixin, TemplateView):
    """
    A view to display the user's welcome dashboard.
    
    This page provides an overview of the user's loan applications, 
    account information, and important updates.
    
    Features:
        - Displays loan application history
        - Shows application status updates
        - Provides access to loan requests and resources
    """
    template_name = 'sbapp/user_welcome.html'

    # def get_context_data(self, **kwargs):
    #     """
    #     Adds loan application history and relevant user info to the context.
    #     """
    #     context = super().get_context_data(**kwargs)
        
        # Fetching the user's loan applications
        # context['loan_applications'] = LoanRequest.objects.filter(username=self.request.user).order_by('-approval_date')
        
        # # Example notifications or messages (could be extended from a model)
        # context['notifications'] = [
        #     "Your latest loan request is under review.",
        #     "Don't forget to check out our business resources!",
        # ]

        # print(LoanRequest.objects.filter(username=self.request.user).exists())

        # return context
    
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

        
    #     # Convert gr_appv to currency format
    #     amount = form.cleaned_data.get('gr_appv')
    #     if amount is not None:
    #         form.instance.gr_appv = f"${amount:,.2f}"
    #     response = super().form_valid(form)
    #     messages.success(self.request, 'Loan request submitted successfully!')
    #     return response

class LoanRequestSuccessView(TemplateView):
    template_name = 'sbapp/user_loan_request_success.html'

    # def post(self, request, *args, **kwargs):
    #     # Si la requête est de type POST, on peut récupérer les données envoyées
    #     param = request.POST.get('mon_parametre', 'valeur_par_defaut')

    #     # Effectuez ici le traitement souhaité, par exemple enregistrer des informations, etc.
    #     print(f'Paramètre reçu: {param}')

    #     # Redirigez ou retournez une réponse après traitement
    #     return HttpResponse("Traitement effectué avec succès.")
    
    # # Vous pouvez également implémenter la méthode get si vous avez besoin de gérer l


#______________________________________________________________________________
#
# region LoanRequestStatusView
#______________________________________________________________________________
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

class AboutView(TemplateView):
    template_name = 'sbapp/about.html'  # About Us View Template

class ServicesView(TemplateView):
    template_name = 'sbapp/services.html'  # Services View Template

class BlogView(TemplateView):
    template_name = 'sbapp/blog.html'  # Blog View Template

class TestimonialView(TemplateView):
    template_name = 'sbapp/testimonial.html'  # Testimonial View Template

class ContactView(TemplateView):
    template_name = 'sbapp/contact.html'  # Contact View Template

class ContactSupportView(TemplateView):
    template_name = 'sbapp/contact_support.html'  # User Contact View Template

from django.views.generic import TemplateView

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
    


#______________________________________________________________________________
#
# region LoanApprovalStatus
#______________________________________________________________________________
class LoanApprovalStatus(TemplateView):
    model = LoanRequestForm
    template_name = "sbapp/admin_loan_approval_status.html"
    context_object_name = 'loan_request'

    template_name = 'mon_template.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
        
    #     # Effectuer un appel à une API externe
    #     url = "http://127.0.0.1:8000/auth/login"
    #     try:
    #         response = requests.get(url)
    #         response.raise_for_status()  # Vérifie que la requête a réussi
    #         api_data = response.json()  # Récupère les données de l'API au format JSON
    #     except requests.exceptions.RequestException as e:
    #         # Gérer l'exception si l'appel API échoue
    #         api_data = None
    #         context['error'] = f"Erreur lors de l'appel à l'API : {str(e)}"
        
    #     # Ajouter l'objet Client (ici, le client n°4 par exemple) au contexte
    #     try:
    #         client = Client.objects.get(id=4)  # Récupère le client n°4
    #         context['client'] = client
    #     except Client.DoesNotExist:
    #         context['client'] = None
    #         context['error'] = "Client non trouvé"

    #     # Ajouter les données de l'API au contexte
    #     context['api_data'] = api_data

    #     return context


   
    


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


# def predict_charges(request):
#     """
#     Predicts insurance charges based on user input.

#     This view handles both GET and POST requests:
#     - GET: Renders the insurance form.
#     - POST: Processes user input, loads a pre-trained model, makes a prediction, 
#       and returns the predicted insurance charge as a JSON response.

#     Args:
#         request (HttpRequest): The HTTP request object.

#     Returns:
#         HttpResponse:
#             - If GET: Renders the 'insurance_form.html' template.
#             - If POST: Returns a JSON response with the predicted insurance charge.
#             - If an error occurs: Returns a JSON response with an error message and status 400.
#             - If the request method is invalid: Returns a JSON response with status 405.

#     Raises:
#         - Handles exceptions gracefully and returns an error message if prediction fails.
#     """
#     prediction = None

#     # Handle the GET request - Render the form
#     if request.method == 'GET':
#         return render(request, 'insurance_app/insurance_form.html', {'prediction': prediction})

#     # Handle the POST request - Process the form data and predict
#     elif request.method == 'POST':
#         try:
#             # Parse the JSON data from the request body
#             data = json.loads(request.body)

#             # Extract data from the JSON
#             height = float(data.get('height'))
#             weight = float(data.get('weight'))
#             age = int(data.get('age'))
#             sex = data.get('sex')
#             smoker = data.get('smoker')
#             reg ion = data.get('reg ion')
#             children = int(data.get('children'))
#             bmi = float(data.get('bmi'))
#             bmi_category = data.get('bmi_category')

#             # Load model from pickle
#             model_path = 'insurance_app/model/model_1.pickle'
#             with open(model_path, 'rb') as file:
#                 model = pickle.load(file)

#             # Prepare data as a DataFrame (ensure the order matches your model's expected input)
#             input_data = pd.DataFrame([{
#                 'height': height,
#                 'weight': weight,
#                 'age': age,
#                 'sex': sex,
#                 'smoker': smoker,
#                 'region': region,
#                 'children': children,
#                 'bmi': bmi,
#                 'BMI_category': bmi_category
#             }])

#             # Make the prediction
#             prediction = round(model.predict(input_data)[0], 2)

#             # Ensure prediction is non-negative
#             prediction = max(prediction, 0)

#             # Return prediction as JSON response
#             return JsonResponse({'prediction': prediction})

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)

#     # If not GET or POST, return an error
#     return JsonResponse({'error': 'Invalid request method'}, status=405)



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
#             "re gion": user_profile.reg ion,
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
#             reg ion=user_profile.reg ion,
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