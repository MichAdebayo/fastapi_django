import requests

class PredictionService() :
    def __init__(self) :
        self.api_url = "http://127.0.0.1:8000"
        self.current_token = None

    # def current_token(self) -> str :
    #     return self.curent_token

    def authenticate(self, email, password) : #-> bool:
        method_url = self.api_url + "/" + "auth/login"

        api_data = "starting..."

        try:
            response = requests.post(
                method_url, 
                json = { 
                    "email" : email, 
                    "password" : password 
                })
            response.raise_for_status()  # Vérifie que la requête a réussi
            api_data = response.json()  # Récupère les données de l'API au format JSON

            # self.current_token = api_data.get("access_token")
            # return True

        except requests.exceptions.RequestException as e:
            api_data = str(e) 

            # return False
            
        return api_data


