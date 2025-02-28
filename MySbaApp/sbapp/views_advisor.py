
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from django.views.generic import ListView

from django.shortcuts import render 

from typing import Any

from .models import LoanRequest 
from .forms import LoanRequestForm 

from .prediction_service import PredictionService

from datetime import datetime, timezone # date, 
#from zoneinfo import ZoneInfo


#______________________________________________________________________________
#
# region AdvisorLoanRequestListView
#______________________________________________________________________________
class AdvisorLoanListView(LoginRequiredMixin, ListView) : 
    model = LoanRequest
    template_name = 'sbapp/advisor_loan_list.html'
    context_object_name = 'loan_requests'

    # def __init__(self, **kwargs) :
    #     super().__init__(**kwargs)
    #     self.local_timezone = ZoneInfo('Europe/Paris') 
        
    def get_context_data(self, **kwargs):
        self.object_list = LoanRequest.objects.all()
        context = super().get_context_data(**kwargs)
        match self.request.method :
            case "GET" : context['form'] = LoanRequestForm(self.request.GET) 
            case "POST" : context['form'] = LoanRequestForm(self.request.POST) 
            case _ :  raise Exception("Unknown request type")

        for loan_request in context["loan_requests"] :
            match loan_request.loan_simulation_status : 
                case "Pending" :
                    loan_request.simulation_view_state = "INITIAL"
                    loan_request.custom_simulation_status = "Pending"
                    loan_request.custom_simulation_date = "no simulation date"
                case _ :
                    loan_request.simulation_view_state = "FINAL"
                    loan_request.custom_simulation_status = self.get_custom_simulation_status(loan_request.loan_simulation_status)
                    loan_request.custom_simulation_date = loan_request.loan_simulation_date_utc

            match loan_request.loan_advisor_approval_status : 
                case "Pending" :
                    loan_request.advisor_view_state = "INITIAL"
                    loan_request.custom_advisor_approval_status = loan_request.loan_advisor_approval_status
                    loan_request.custom_advisor_approval_date = "no approval date"
  
                case _ : 
                    loan_request.advisor_view_state = "FINAL"
                    loan_request.custom_advisor_approval_status = loan_request.loan_advisor_approval_status
                    loan_request.custom_advisor_approval_date = loan_request.loan_advisor_approval_date_utc 

        return context
    
    def post(self, request, *args, **kwargs):
        simulate_loan_id = request.POST.get('SIMULATE')
        approve_loan_id = request.POST.get('APPROVE')
        reject_loan_id = request.POST.get('REJECT')

        context = self.get_context_data(**kwargs)
    
        if simulate_loan_id :
            loan_request = self.get_loan_from_context(simulate_loan_id, context)
            if loan_request :
                loan_object_in_db = LoanRequest.objects.get(loan_nr_chk_dgt=simulate_loan_id)

                approval_status = self.request_simulation(loan_object_in_db)
                if approval_status :
                    loan_object_in_db.loan_simulation_status = approval_status
                    loan_object_in_db.loan_simulation_date_utc = datetime.now(timezone.utc).date()
                    loan_object_in_db.save()

                    loan_request.simulation_view_state = "FINAL"
                    loan_request.custom_simulation_status = self.get_custom_simulation_status(loan_object_in_db.loan_simulation_status)
                    loan_request.custom_simulation_date = loan_object_in_db.loan_simulation_date_utc

                else :
                    loan_request.simulation_view_state = "WORKING"
                    loan_request.custom_simulation_status = "something wrong happened"

            else :
                loan_request.simulation_view_state = "WORKING"
                loan_request.custom_simulation_status = "something wrong happened"

        elif reject_loan_id :
            loan_request = self.get_loan_from_context(reject_loan_id, context)
            if loan_request :
                loan_object_in_db = LoanRequest.objects.get(loan_nr_chk_dgt=reject_loan_id)
                loan_object_in_db.loan_advisor_approval_status = "REJECTED"
                loan_object_in_db.loan_advisor_approval_date_utc = datetime.now(timezone.utc).date()
                loan_object_in_db.save()

                loan_request.advisor_view_state = "FINAL"
                loan_request.custom_advisor_approval_status = loan_object_in_db.loan_advisor_approval_status
                loan_request.custom_advisor_approval_date = loan_object_in_db.loan_advisor_approval_date_utc

        elif approve_loan_id :
            loan_request = self.get_loan_from_context(approve_loan_id, context)
            if loan_request :
                loan_object_in_db = LoanRequest.objects.get(loan_nr_chk_dgt=approve_loan_id)
                loan_object_in_db.loan_advisor_approval_status = "APPROVED"
                loan_object_in_db.loan_advisor_approval_date_utc = datetime.now(timezone.utc).date()
                loan_object_in_db.save()

                loan_request.advisor_view_state = "FINAL"
                loan_request.custom_advisor_approval_status = loan_object_in_db.loan_advisor_approval_status
                loan_request.custom_advisor_approval_date = loan_object_in_db.loan_advisor_approval_date_utc

        return render(request, self.template_name, context)
    
    def get_loan_from_context(self, loan_id : int, context: dict[str, Any]):
        for loan_request in context["loan_requests"] :
            if loan_request.loan_nr_chk_dgt == loan_id :
                return loan_request
            
        return None

    def request_simulation(self, selected_loan_request : LoanRequest) :
        api_service = PredictionService()
        if not api_service.authenticate("user1.fakemail@fakeprovider.com", "otherpass1") :
            return None
        
        loan_prediction = api_service.request_prediction(selected_loan_request)
        if not loan_prediction :
            return None
        
        return loan_prediction
    
    def get_custom_simulation_status(self, approval_status : str ) -> str :
        match approval_status : 
            case "Pending" : return "Pending"
            case "Approved" : return "Will be repaid in full"
            case "Not approved" : return "Will be impossible to recover"
            case _ : return "Undefined simulation status"

      