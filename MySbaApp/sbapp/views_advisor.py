
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from django.views.generic import ListView

from django.shortcuts import render 

from .models import LoanRequest 
from .forms import LoanRequestForm 

from .prediction_service import PredictionService


#______________________________________________________________________________
#
# region AdvisorLoanRequestListView
#______________________________________________________________________________
class AdvisorLoanListView(LoginRequiredMixin, ListView) : 
    model = LoanRequest
    template_name = 'sbapp/advisor_loan_list.html'
    context_object_name = 'loan_requests'

    def get_context_data(self, **kwargs):
        self.object_list = LoanRequest.objects.all()
        context = super().get_context_data(**kwargs)
        match self.request.method :
            case "GET" : context['form'] = LoanRequestForm(self.request.GET) 
            case "POST" : context['form'] = LoanRequestForm(self.request.POST) 
            case _ :  raise Exception("Unknown request type")

        for loan_request in context["loan_requests"] :
            loan_request.custom_simulation_status = loan_request.loan_simulation_status
            loan_request.custom_simulation_date = loan_request.loan_simulation_date_utc
            loan_request.custom_simlation_message = "SIMULATION MESSAGE"
            loan_request.custom_advisor_approval_status = loan_request.loan_advisor_approval_status
            loan_request.custom_advisor_approval_date = loan_request.loan_advisor_approval_date_utc
            loan_request.custom_advisor_message = "ADVISOR MESSAGE"

        return context
    
    def post(self, request, *args, **kwargs):
        simulate_loan_id = request.POST.get('SIMULATE')
        approve_loan_id = request.POST.get('APPROVE')
        reject_loan_id = request.POST.get('REJECT')

        context = self.get_context_data(**kwargs)
    
        if simulate_loan_id :
            api_service = PredictionService()
            data = api_service.authenticate("user1.fakemail@fakeprovider.com", "otherpass1")

            if not data : 
                message = "connection impossible"

            for loan_request in context["loan_requests"] :
                if loan_request.loan_nr_chk_dgt == simulate_loan_id :
                    loan_request.custom_simutation_message = message


        elif reject_loan_id :
            pass 

        elif approve_loan_id :
            pass


        return render(request, self.template_name, context)