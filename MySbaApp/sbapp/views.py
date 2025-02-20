from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from .models import UserProfile, Job, ContactMessage, PredictionHistory, Appointment,Availability
from .forms import UserProfileForm, UserSignupForm, ApplicationForm, ChangePasswordForm, PredictChargesForm, AppointmentForm
from django.http import HttpResponse
import pickle
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout, get_user_model
from django.conf import settings
from django.views import View 
import pandas as pd
import os
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import ListView
from django.db.models import Avg
from django.contrib.auth.decorators import login_required
from django.utils import timezone


class HomeView(TemplateView):
    """
    Renders the homepage.

    This view is responsible for rendering the 'home.html' template, which serves as the 
    homepage for the application.

    Attributes:
        template_name (str): The name of the template used to display the response.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'home.html' template.
    """
    template_name = 'sbapp/home.html'  # Home Page View Template


class TestingView(TemplateView):
    """
    Renders the testing page.

    This view is responsible for rendering the 'base_final.html' template, likely used 
    for testing purposes or as part of the home page layout.

    Attributes:
        template_name (str): The name of the template used to display the response.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'base_final.html' template.
    """
    template_name = 'insurance_app/base_final.html'  # Home Page View Template


         
class AboutView(TemplateView):
    """
    Renders the 'About Us' page.

    This view is responsible for rendering the 'about.html' template, which provides 
    information about the application. 

    Attributes:
        template_name (str): The name of the template used to display the response.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'about.html' template.
    """
    template_name = 'insurance_app/about.html'  # About Us View Template


class JoinUsView(TemplateView):
    """
    Displays the 'Join Us' page with a list of job openings.

    This view retrieves all available job listings from the database and renders them 
    in the 'join_us.html' template. The jobs are passed to the template context for display.

    Attributes:
        template_name (str): The name of the template used to display the response.

    Methods:
        get_context_data(**kwargs):
            Retrieves the job listings from the database and adds them to the context 
            for rendering in the template.

    Args:
        request (HttpRequest): The HTTP request object.
        **kwargs: Additional keyword arguments passed to the context.

    Returns:
        dict: The context dictionary containing the list of job openings.
    """
    template_name = 'insurance_app/join_us.html'  # Join Us View Template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['jobs'] = Job.objects.all()
        return context



class ApplyView(TemplateView):
    """
    Handles job application submissions and displays a thank-you page.

    This view renders a template for submitting job applications and processes form submissions 
    via POST requests. If the submitted form is valid, the application is saved, and the user 
    is redirected to a thank-you page.

    Attributes:
        template_name (str): The name of the template used to display the response.

    Methods:
        post(request, *args, **kwargs):
            Processes the application form submission. If valid, saves the data and redirects 
            to the 'apply_thank_you' page. Otherwise, re-renders the form with errors.
    
    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse:
            - If POST and form is valid: Redirects to the 'apply_thank_you' page.
            - If POST and form is invalid: Renders the form with errors.
    """
    template_name = 'apply_thank_you.html'

    def post(self, request, *args, **kwargs):
        # Handle form submission here
        if request.method == 'POST':
            form = ApplicationForm(request.POST, request.FILES)
            if form.is_valid():
                # Process the form (e.g., save data, send email, etc.)
                form.save()  # Save the application in our model 
                return redirect('apply_thank_you')  # Redirect to a thank you page
        else:
            form = ApplicationForm()

        return render(request, self.template_name, {'form': form})


def apply(request):
    """
    Handles job application submissions.

    This view processes POST requests to collect applicant details, including name, email, 
    job ID, and resume. If the form is submitted successfully, a confirmation message is 
    displayed. If the request method is not POST, the user is redirected to the 'join_us' page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse:
            - If POST: Returns a success message confirming the application submission.
            - If GET or other methods: Redirects to the 'join_us' page.
    """
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        job_id = request.POST.get('job_id')
        resume = request.FILES.get('resume')

        return HttpResponse("Application submitted successfully!")
    
    return redirect('join_us')


class HealthAdvicesView(TemplateView):
    """Renders the health advices page.

    Provides a view for the application's health advices page.
    """
    template_name = 'insurance_app/health_advices.html'  # Assur'Cares Section View Template


class CybersecurityAwarenessView(TemplateView):
    """Renders the cybersecurity awareness page.

    Provides a view for the application's cybersecurity awareness page.
    """
    template_name = 'insurance_app/cybersecurity_awareness.html'    # Cybersecurity Section View Template


#Welcome view (used to modified homepage)
class WelcomeView(TemplateView):
    """Renders the welcome page.

    Provides a view for the application's welcome page.
    """
    template_name = 'insurance_app/welcome.html' 


#To handle non-client messages submission
def contact_view(request):
    """
    Handles the contact form submission and displays the contact form.

    This view processes POST requests to capture user input (name, email, and message),
    saves the message in the database, and displays a success message before redirecting 
    the user back to the contact page. For GET requests, it renders the contact form.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse:
            - If POST: Redirects to the contact page after saving the message.
            - If GET: Renders the 'contact_form.html' template.
    """
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # Save the message to the database
        ContactMessage.objects.create(name=name, email=email, message=message)

        # Show a success message
        messages.success(request, "Your message has been sent successfully!")
        return redirect('contact')  # Replace 'contact' with the name of your URL pattern

    return render(request, "insurance_app/contact_form.html")


# To handle client messages submission
def contact_view_user(request):
    """
    Handles the contact form submission and displays the contact form for loggedin users.

    This view processes POST requests to capture user input (name, email, and message),
    saves the message in the database, and displays a success message before redirecting 
    the user back to the contact page. For GET requests, it renders the contact form.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse:
            - If POST: Redirects to the contact page after saving the message.
            - If GET: Renders the 'contact_form.html' template.
    """
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # Save the message to the database
        ContactMessage.objects.create(name=name, email=email, message=message)

        # Show a success message
        messages.success(request, "Your message has been sent successfully!")
        return redirect('contact_form')  # Replace 'contact' with the name of your URL pattern

    return render(request, "insurance_app/contact_form_user.html")

@staff_member_required
def message_list_view(request):
    """
    Displays a list of contact messages for staff members.

    This view retrieves all contact messages from the database, orders them by submission 
    time in descending order (most recent first), and renders them in a template. 
    Access to this view is restricted to staff members.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'messages_list.html' template with the following context:
            - `messages` (QuerySet): A list of all contact messages, ordered by submission time.
    """
    messages = ContactMessage.objects.all().order_by('-submitted_at')  # Most recent first
    return render(request, "insurance_app/messages_list.html", {"messages": messages})


@csrf_exempt
def solve_message(request, message_id):
    """
    Handles the deletion of a contact message.

    This view processes a POST request to delete a specific contact message by its ID.
    If the message exists, it is deleted, and a success response is returned.
    If the message does not exist, an error response is returned.
    Only POST requests are allowed; other request methods will result in an error response.

    Args:
        request (HttpRequest): The HTTP request object.
        message_id (int): The ID of the contact message to be deleted.

    Returns:
        JsonResponse:
            - If successful: {'success': True}
            - If the message is not found: {'success': False, 'error': 'Message not found.'} (HTTP 404)
            - If the request method is invalid: {'success': False, 'error': 'Invalid request method.'} (HTTP 400)
    """
    if request.method == 'POST':
        try:
            contact_message = ContactMessage.objects.get(id=message_id)
            contact_message.delete()
            return JsonResponse({'success': True})
        except ContactMessage.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Message not found.'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)


def predict_charges(request):
    """
    Predicts insurance charges based on user input.

    This view handles both GET and POST requests:
    - GET: Renders the insurance form.
    - POST: Processes user input, loads a pre-trained model, makes a prediction, 
      and returns the predicted insurance charge as a JSON response.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse:
            - If GET: Renders the 'insurance_form.html' template.
            - If POST: Returns a JSON response with the predicted insurance charge.
            - If an error occurs: Returns a JSON response with an error message and status 400.
            - If the request method is invalid: Returns a JSON response with status 405.

    Raises:
        - Handles exceptions gracefully and returns an error message if prediction fails.
    """
    prediction = None

    # Handle the GET request - Render the form
    if request.method == 'GET':
        return render(request, 'insurance_app/insurance_form.html', {'prediction': prediction})

    # Handle the POST request - Process the form data and predict
    elif request.method == 'POST':
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)

            # Extract data from the JSON
            height = float(data.get('height'))
            weight = float(data.get('weight'))
            age = int(data.get('age'))
            sex = data.get('sex')
            smoker = data.get('smoker')
            region = data.get('region')
            children = int(data.get('children'))
            bmi = float(data.get('bmi'))
            bmi_category = data.get('bmi_category')

            # Load model from pickle
            model_path = 'insurance_app/model/model_1.pickle'
            with open(model_path, 'rb') as file:
                model = pickle.load(file)

            # Prepare data as a DataFrame (ensure the order matches your model's expected input)
            input_data = pd.DataFrame([{
                'height': height,
                'weight': weight,
                'age': age,
                'sex': sex,
                'smoker': smoker,
                'region': region,
                'children': children,
                'bmi': bmi,
                'BMI_category': bmi_category
            }])

            # Make the prediction
            prediction = round(model.predict(input_data)[0], 2)

            # Ensure prediction is non-negative
            prediction = max(prediction, 0)

            # Return prediction as JSON response
            return JsonResponse({'prediction': prediction})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    # If not GET or POST, return an error
    return JsonResponse({'error': 'Invalid request method'}, status=405)



@login_required
def book_appointment(request):
    """
    Handles appointment booking for authenticated users.

    This view allows users to book an appointment using an appointment form. 
    It also displays the user's upcoming and past appointments.

    Functionality:
    - If the request is POST, it processes the appointment form.
    - Saves the appointment if the form is valid, associating it with the logged-in user.
    - Displays success messages upon successful booking.
    - Redirects back to the booking page after submission.
    - If the request is GET, it renders the appointment form.
    - Retrieves and displays the user's upcoming and past appointments.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the `book_appointment.html` template with:
            - `today` (date): The current date.
            - `form` (AppointmentForm): The form for booking an appointment.
            - `upcoming_appointments` (QuerySet): The user's upcoming appointments, ordered by date.
            - `past_appointments` (QuerySet): The user's past appointments, ordered by date (descending).
    """
    today = timezone.now().date()  # Get today's date in YYYY-MM-DD format
    
    # Handle form submission (POST request)
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            # Save the appointment data
            appointment = form.save(commit=False)
            appointment.user = request.user  # Associate the logged-in user
            appointment.save()

            messages.success(request, 'Your appointment has been booked successfully!')
            return redirect('book_appointment')  # Redirect to the same page after saving
    else:
        form = AppointmentForm()

    # Get upcoming and past appointments for display
    upcoming_appointments = Appointment.objects.filter(
        user=request.user, date__gte=today
    ).order_by('date')

    past_appointments = Appointment.objects.filter(
        user=request.user, date__lt=today
    ).order_by('-date')

    return render(request, 'insurance_app/book_appointment.html', {
        'today': today,
        'form': form,
        'upcoming_appointments': upcoming_appointments,
        'past_appointments': past_appointments,
    })


def get_available_times(request):
    """
    Retrieves available time slots for a given date.

    This function handles a GET request with a 'date' parameter and returns 
    the available time slots for that date in JSON format. If no availability 
    is found, an empty list is returned.

    Args:
        request (HttpRequest): The HTTP request object containing GET parameters.

    Returns:
        JsonResponse: A JSON response containing the available time slots in the format:
            {
                "times": [list of available time slots]
            }
            If no availability is found or no date is provided, an empty list is returned.
    """
    if date := request.GET.get('date'):
        try:
            availability = Availability.objects.get(date=date)
            return JsonResponse({"times": availability.time_slots})
        except Availability.DoesNotExist:
            return JsonResponse({"times": []})
    return JsonResponse({"times": []})



class SignupView(CreateView):
    """
    View for handling user sign-up using Django's generic CreateView.

    This view allows users to register by filling out a sign-up form. 
    Upon successful registration, users are redirected to the login page.

    Attributes:
        model (Model): The model associated with the sign-up process (UserProfile).
        form_class (Form): The form class used for user registration (UserSignupForm).
        template_name (str): The path to the HTML template for rendering the sign-up form.
        success_url (str): The URL to redirect to upon successful registration (login page).
    """
    model = UserProfile
    form_class = UserSignupForm
    template_name = 'insurance_app/signup.html'
    success_url = reverse_lazy('login')


class CustomLoginView(LoginView):
    """
    Custom login view extending Django's built-in LoginView.

    Attributes:
        template_name (str): The path to the login template.
        redirect_authenticated_user (bool): Redirects authenticated users away from the login page.

    Methods:
        get_success_url():
            Returns the URL to redirect to after a successful login.
        
        dispatch(request, *args, **kwargs):
            Redirects authenticated users directly to the profile page.

        form_valid(form):
            Handles session expiration based on the 'remember me' checkbox.
            - If 'remember me' is checked, the session lasts for 2 weeks.
            - Otherwise, the session expires when the browser is closed.
    """
    template_name = 'insurance_app/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        """
        Returns the URL to redirect to after a successful login.

        Returns:
            str: The reverse_lazy URL of the 'welcome' page.
        """
        return reverse_lazy('welcome')

    def dispatch(self, request, *args, **kwargs):
        """
        Overrides dispatch method to redirect authenticated users to the profile page.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            HttpResponse: Redirects authenticated users to 'profile' or processes the request normally.
        """
        if self.request.user.is_authenticated:
            return redirect('profile')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Handles session expiration based on the 'remember me' checkbox.

        If 'remember me' is checked, the session lasts for 2 weeks (1209600 seconds).
        Otherwise, the session expires when the browser is closed.

        Args:
            form (AuthenticationForm): The authentication form containing user credentials.

        Returns:
            HttpResponse: The response after processing a valid login form.
        """
        remember_me = self.request.POST.get('remember_me', None) is not None

        if not remember_me:
            self.request.session.set_expiry(0)  # Expire session on browser close
        else:
            self.request.session.set_expiry(1209600)  # Session lasts 2 weeks

        return super().form_valid(form)


class UserProfileView(LoginRequiredMixin, UpdateView):
    """
    A view for authenticated users to update their own profile information.

    This class-based view handles user profile updates by combining Django's
    LoginRequiredMixin with UpdateView functionality. It ensures only authenticated
    users can access the profile edit page and automatically handles form validation
    and saving.

    Attributes:
        model (User): The user model instance being edited (uses get_user_model()
            for custom user model compatibility)
        form_class (UserProfileForm): The form class used for profile updates
        template_name (str): Path to the profile editing template
        success_url (str): URL to redirect to after successful update

    Methods:
        get_object: Retrieves the current user's profile for editing
        form_valid: Handles successful form submissions and adds user feedback

    Features:
        - Requires authentication through LoginRequiredMixin
        - Pre-populates form with current user data
        - Displays success messages using Django's messages framework
        - Automatic redirect to profile page after update
    """

    model = get_user_model()
    form_class = UserProfileForm
    template_name = 'insurance_app/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        """Retrieve the current logged-in user instance for editing.
        
        Overrides default UpdateView behavior to automatically use the
        request's user without needing a URL parameter.
        
        Args:
            queryset: Optional queryset (not used in this implementation)
            
        Returns:
            User: The currently authenticated user instance
        """
        return self.request.user
    
    def form_valid(self, form):
        """Handle valid form submission and provide user feedback.
        
        Args:
            form: Validated UserProfileForm instance
            
        Returns:
            HttpResponseRedirect: Redirect to success_url
        """
        response = super().form_valid(form)
        messages.success(self.request, 'Your profile has been updated!')
        return response


class ChangePasswordView(PasswordChangeView):
    """
    Handles password change requests.

    This view allows users to change their password. If the form is valid, it saves the new 
    password, displays a success message, and redirects the user to their profile page.

    Attributes:
        form_class (Form): The form used for password change.
        template_name (str): The name of the template used to display the response.
        success_url (str): The URL to redirect to after a successful password change.

    Methods:
        form_valid(form):
            Processes the form submission. Saves the new password, shows a success message, 
            and returns the response.

    Args:
        request (HttpRequest): The HTTP request object.
        form (Form): The form containing the user's input.

    Returns:
        HttpResponse: Redirects to the profile page upon successful password change.
    """
    form_class = ChangePasswordForm  
    template_name = 'insurance_app/changepassword.html'
    success_url = reverse_lazy('profile')
    
    def form_valid(self, form):
        # Save the new password
        response = super().form_valid(form)
        # Add a success message
        messages.success(self.request, 'Your password has been changed successfully!')
        return response


class UserLogoutView(LoginRequiredMixin, View):
    """
    Handles user logout requests with a confirmation step.

    This view provides a confirmation page for users who want to log out, and handles 
    the actual logout process when the user submits the request.

    Attributes:
        template_name (str): The name of the template used to display the logout confirmation page.
        next_page (str): The URL to redirect to after the logout process is complete.

    Methods:
        get(request):
            Displays the logout confirmation page to the user.

        post(request):
            Handles the logout action. Logs the user out and renders the confirmation page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: 
            - GET request: Renders the logout confirmation page.
            - POST request: Logs the user out and renders the confirmation page.
    """
    template_name = 'insurance_app/logout_user.html'
    next_page = reverse_lazy('logout_user')

    def get(self, request):
        # Handle GET requests with confirmation page
        user = self.request.user
        return render(request, self.template_name, {'user': user})
    
    def post(self, request):
        # Handle actual logout
        user = self.request.user
        logout(request)
        return render(request, self.template_name, {'user': user})



class PredictChargesView(LoginRequiredMixin, UpdateView):
    """
    Allows users to update their profile and predicts insurance charges based on input.

    This view allows logged-in users to update their profile information, such as age, 
    height, weight, number of children, and smoking status. Upon successful form submission, 
    it uses a pre-trained model to predict the user's insurance charges based on the updated 
    information and displays the prediction.

    Attributes:
        model (Model): The model representing the user profile.
        form_class (Form): The form class used for capturing user input.
        template_name (str): The name of the template used for rendering the form and prediction results.
        success_url (str): The URL to redirect to after successful form submission.

    Methods:
        get_object(queryset=None):
            Returns the current user object for updating the profile.

        form_valid(form):
            Validates and processes the form data, updates the user profile, 
            generates a prediction, and displays the prediction results.

        form_invalid(form, error_message):
            Handles invalid form submissions and returns an error message.

        categorize_bmi(bmi):
            Categorizes the user's BMI into weight categories (underweight, normal, overweight, obese).

        categorize_age(age):
            Categorizes the user's age into life stages (young adult, early adulthood, mid adulthood, late adulthood).

        preprocess_data(data):
            Prepares the input data by performing necessary transformations and encoding for prediction.

        load_model():
            Loads the pre-trained model from a pickle file for prediction.

    Args:
        request (HttpRequest): The HTTP request object.
        form (Form): The form containing user input.
        prediction_value (float): The predicted insurance charges based on the user's profile.

    Returns:
        HttpResponse: 
            - On success: Renders the template with the predicted charges and recent prediction history.
            - On error: Returns a form with an error message.
    """
    model = get_user_model()
    form_class = PredictChargesForm
    template_name = 'insurance_app/predict.html'
    success_url = reverse_lazy('predict')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        user_profile = self.get_object()
        
        # Update and save user profile
        user_profile.age = form.cleaned_data['age']
        user_profile.weight = form.cleaned_data['weight']
        user_profile.height = form.cleaned_data['height']
        user_profile.num_children = form.cleaned_data['num_children']
        user_profile.smoker = form.cleaned_data['smoker']
        user_profile.save()  # Uncommented to persist changes

        # Validate inputs
        if user_profile.height <= 0:
            return self.form_invalid(form, "Invalid height value")

        # Calculate BMI using model property
        try:
            bmi = user_profile.bmi
        except ZeroDivisionError:
            return self.form_invalid(form, "Invalid height value (cannot be zero)")

        # Create prediction data
        prediction_data = {
            "age": user_profile.age,
            "bmi": bmi,
            "smoker": user_profile.smoker,
            "children": user_profile.num_children,
            "region": user_profile.region,
            "sex": user_profile.sex
        }

        # Preprocess and predict
        preprocessed_data = self.preprocess_data(prediction_data)
        model = self.load_model()
        
        if not model:
            return self.form_invalid(form, "Failed to load prediction model")

        predicted_charges = model.predict(preprocessed_data)
        prediction_value = round(predicted_charges[0], 2)

        # Save prediction history
        PredictionHistory.objects.create(
            user=user_profile,
            age=user_profile.age,
            weight=user_profile.weight,
            height=user_profile.height,
            num_children=user_profile.num_children,
            smoker=user_profile.smoker,
            region=user_profile.region,
            sex=user_profile.sex,
            predicted_charges=prediction_value
        )

        return self.render_to_response(self.get_context_data(
            form=form,
            predicted_charges=prediction_value,
            recent_predictions=user_profile.insurance_predictions.all()[:5]
        ))

    def form_invalid(self, form, error_message):
        messages.error(self.request, error_message)
        return super().form_invalid(form)

    def categorize_bmi(self, bmi):
        if bmi < 18.5:
            return "under_weight"
        elif 18.5 <= bmi < 25:
            return "normal_weight"
        elif 25 <= bmi < 30:
            return "over_weight"
        else:
            return "obese"

    def categorize_age(self, age):
        if 18 < age < 26:
            return "young_adult"
        elif 26 <= age < 36:
            return "early_adulthood"
        elif 36 <= age < 46:
            return "mid_adulthood"
        else:
            return "late_adulthood"

    def preprocess_data(self, data):
        # Define the expected columns (must match the model's input requirements)
        expected_columns = [
            "smoker",
            "age",
            "bmi",
            "age_category_young_adult",
            "age_category_early_adulthood",
            "bmi_category_over_weight",
            "bmi_category_obese",
            "children_str_0",
        ]

        # Create a DataFrame from the input data
        df = pd.DataFrame([data])

        # Convert smoker to binary (1 for "Yes", 0 for "No")
        df["smoker"] = df["smoker"].map({"Yes": 1, "No": 0})

        # Categorize age and bmi
        df["age_category"] = df["age"].apply(self.categorize_age)
        df["bmi_category"] = df["bmi"].apply(self.categorize_bmi)

        # Convert children to string (for one-hot encoding)
        df["children_str"] = df["children"].apply(lambda x: str(x))

        # Perform one-hot encoding for categorical columns
        df = pd.get_dummies(df, columns=["age_category", "bmi_category", "children_str"], dtype=(int))

        # Ensure all expected columns are present
        for col in expected_columns:
            if col not in df.columns:
                df[col] = 0  # Add missing columns with default value 0

        # Reorder columns to match the model's expectations
        df = df[expected_columns]

        return df

    def load_model(self):
        try:
            model_path = os.path.join(settings.BASE_DIR, 'insurance_app/model/model.pkl')
            with open(model_path, "rb") as file:
                model = pickle.load(file)
            return model
        except FileNotFoundError:
            print("Error: The model file 'model.pkl' was not found.")
            return None
        except pickle.UnpicklingError:
            print("Error: The file could not be unpickled. Ensure it is a valid pickle file.")
            return None


class PredictionHistoryView(LoginRequiredMixin, ListView):
    """
    Displays a list of prediction history for a logged-in user.

    This view allows logged-in users to view their past insurance charge predictions, 
    including the predicted charges and related details. The list is paginated, and users 
    can see statistics such as the total number of predictions and the average predicted charges.

    Attributes:
        model (Model): The model representing the prediction history.
        template_name (str): The name of the template used for rendering the prediction history page.
        context_object_name (str): The name of the context variable for the list of predictions.
        paginate_by (int): The number of predictions to display per page.

    Methods:
        get_queryset():
            Returns a queryset containing the user's prediction history, 
            ordered by timestamp and limited to the logged-in user.

        get_context_data(**kwargs):
            Adds extra context to the template, including the user profile, 
            total predictions, and average predicted charges.

    Args:
        request (HttpRequest): The HTTP request object.
        predictions (QuerySet): A list of `PredictionHistory` objects related to the current user.
        total_predictions (int): The total number of prediction records for the current user.
        average_charges (float): The average of the predicted charges for the user's history.

    Returns:
        HttpResponse:
            - Renders the template with the user's prediction history, total number of predictions, 
              and the average predicted charges.
    """
    model = PredictionHistory
    template_name = 'insurance_app/prediction_history.html'
    context_object_name = 'predictions'
    paginate_by = 10

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)\
            .select_related('user')\
            .order_by('-timestamp')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'user_profile': self.request.user,
            'total_predictions': self.get_queryset().count(),
            'average_charges': self.get_queryset().aggregate(
                Avg('predicted_charges')
            )['predicted_charges__avg']
        })
        return context