from django.urls import path
from django.contrib.auth import views as auth_views 
from .views import ( HomeView, SignupView, UserLoginView, UserDashboardView, UserProfileView, 
                    BusinessResourcesView, LoanRequestCreateView, LoanRequestSuccessView, WorkshopsView, LoanRequestStatusView,
                    AboutView, ServicesView, BlogView, TestimonialView, ContactView, ContactSupportView, AdminLoginView,
                    AdminDashboardView, AdminProfileView, AdminLoanRequestView, SimpleDataView, update_loan_status) # solve_message,predict_charges,AdminLoanRequestListView
                    # JoinUsView, ApplyView, TemplateView, apply,contact_view, contact_view_user,
                    #,message_list_view, ChangePasswordView, PredictChargesView, UserLogoutView, PredictionHistoryView,book_appointment,get_available_times)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('signup/', SignupView.as_view(), name='signup'),

    # User
    path('user/login/', UserLoginView.as_view(), name='user_login'),
    path('user/dashboard/', UserDashboardView.as_view(), name='user_dashboard'),
    path('update/profile/', UserProfileView.as_view(), name='user_profile'),
    path('loan/request/', LoanRequestCreateView.as_view(), name='user_loan_request'),
    path('user/loan-status/',  LoanRequestStatusView.as_view(), name='user_loan_status'),
    path('user/loan-request/success/', LoanRequestSuccessView.as_view(), name='user_loan_request_success'),

    # Admin
    path('admin-user/login/', AdminLoginView.as_view(), name='admin_user_login'),
    path('admin-user/dashboard/', AdminDashboardView.as_view(), name='admin_user_dashboard'),

    path('simple-data/', SimpleDataView.as_view(), name='simple_data'),
    path('admin-user/loan-requests/', AdminLoanRequestView.as_view(), name='admin_user_loan_request'),
    path('admin-user/loan-requests/<str:loan_nr_chk_dgt>/predict/', AdminLoanRequestView.as_view(), name='predict_loan'),
    path('admin-user/update-loan-status/', update_loan_status, name='update_user_loan_status'),


    path('admin-user/profile/', AdminProfileView.as_view(), name='admin_user_profile'),

    # Other pages
    path('business-resource/', BusinessResourcesView.as_view(), name='business_resources'),
    path('workshops/', WorkshopsView.as_view(), name='workshops'),
    path('about/', AboutView.as_view(), name='about'),
    path('services/', ServicesView.as_view(), name='services'),
    path('blog/', BlogView.as_view(), name='blog'),
    path('testimonial/', TestimonialView.as_view(), name='testimonial'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('contact-support/', ContactSupportView.as_view(), name='contact_support'),

    # Password (Change or Reset) URLs
    path('reset-password/', auth_views.PasswordResetView.as_view(template_name='sbapp/reset_password.html'), name='reset_password'),]
    #path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='insurance_app/password_reset_done.html'), name='password_reset_done'),
    #path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='insurance_app/password_reset_confirm.html'), name='password_reset_confirm'),
    #path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='insurance_app/password_reset_complete.html'), name='password_reset_complete'),
    #path('changepassword/', ChangePasswordView.as_view(), name='changepassword')], 
    # path('logout/', UserLogoutView.as_view(), name='logout_user'), 