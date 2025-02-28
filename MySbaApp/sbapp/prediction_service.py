import requests
from .prediction_service_data import LoanRequestData, LoanResponseData
from .models import LoanRequest

class PredictionService() :
    def __init__(self) :
        self.api_url = "http://127.0.0.1:8000"
        self.access_token = None

    def authenticate(self, email, password) -> bool:
        method_url = self.api_url + "/" + "auth/login"

        request_data = { 
            "email" : email, 
            "password" : password 
        }

        response = requests.post( 
            method_url, 
            json = request_data 
        )
        
        if response.status_code == 200 :
            api_data = response.json() 
            try :
                self.access_token = api_data["access_token"]
                return True
            except: 
                self.access_token = None
                pass

        return False
    
    def request_prediction(self, db_loan_request : LoanRequest) : 
        method_url = self.api_url + "/" + "/loans/request"

        request_data = LoanRequestData(
            state = str(db_loan_request.state), 
            bank = str(db_loan_request.bank),
            naics = int(db_loan_request.naics[:2]),
            term = int(db_loan_request.term),
            no_emp = int(db_loan_request.no_emp),
            new_exist = int(float(db_loan_request.new_exist)),
            create_job = int(db_loan_request.create_job),
            retained_job = int(db_loan_request.retained_job),
            urban_rural = int(db_loan_request.urban_rural),
            rev_line_cr = 1 if db_loan_request.rev_line_cr=='Y' else 0,
            low_doc = 1 if db_loan_request.low_doc =='Y' else 0,
            gr_appv = int(db_loan_request.gr_appv),
            recession = int(db_loan_request.recession),
            has_franchise = int(db_loan_request.has_franchise)
        )

        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        response = requests.post(
            method_url,
            json = request_data.model_dump_json(),
            headers = headers
        )

        if response.status_code == 200 :
            api_data = response.json()
            try:
                response_data = LoanResponseData.model_validate_json(api_data)
                return response_data.approval_status
            except:
                pass
        
        return None

     

            
            
    # def activate(self, new_password) :
    #     method_url = self.api_url + "/" + "auth/activation"

    #     response = requests.post(
    #         method_url, 
    #         json = { 
    #             "email" : email, 
    #             "new_password" : new_password 
    #         })
        
    #     if response.status_code == 200 :
    #         api_data = response.json() 
    #         try :
    #             self.access_token = api_data["access_token"]
    #             return True
    #         except: 
    #             pass

    #     return False


