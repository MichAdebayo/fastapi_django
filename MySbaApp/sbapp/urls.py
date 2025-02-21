from django.urls import path
from django.contrib.auth import views as auth_views 
from .views import ( HomeView, SignupView, CustomLoginView,)# , TemplateView, solve_message,predict_charges,, UserProfileView, AboutView, 
                    # JoinUsView, ApplyView, TemplateView, apply,contact_view, contact_view_user,
                    # HealthAdvicesView, CybersecurityAwarenessView,message_list_view, ChangePasswordView, 
                    # PredictChargesView, UserLogoutView,WelcomeView, PredictionHistoryView,book_appointment,get_available_times,TestingView)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),]
    # path('logout/', UserLogoutView.as_view(), name='logout_user'), 
    # path('welcome/', WelcomeView.as_view(), name='welcome'),]