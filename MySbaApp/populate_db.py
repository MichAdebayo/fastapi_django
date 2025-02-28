import os
import django

def populate_users():

    users = []

    users.append(UserProfile.objects.create_superuser('bank', 'bankname@advisors.com', 'bankpass'))
    users.append(UserProfile.objects.create_user('Nico', 'nico@customers.com', 'nicopass'))
    users.append(UserProfile.objects.create_user('Mike', 'mike@customers.com', 'mikepass'))
    users.append(UserProfile.objects.create_user('Max_', 'max_@customers.com', 'max_pass'))
    users : list[UserProfile] = users

    # Enregistrer l'utilisateur
    for user in users :
        user.save()
        print(f"Utilisateur {user.username} créé avec succès.")

def populate_loans() :

    datas = []
    datas.append( {"user_id": 2, "term" : 6,  "amount" : 50000 } )
    datas.append( {"user_id": 2, "term" : 30,  "amount" : 50000 } )
    datas.append( {"user_id": 2, "term" : 60, "amount" : 50000 } )
    datas.append( {"user_id": 3, "term" : 6, "amount" : 50000 } )
    datas.append( {"user_id": 3, "term" : 30, "amount" : 50000 } ) 
    datas.append( {"user_id": 3, "term" : 60, "amount" : 50000 } )
    datas.append( {"user_id": 4, "term" : 6, "amount" : 50000 } )
    datas.append( {"user_id": 4, "term" : 30, "amount" : 50000 } ) 
    datas.append( {"user_id": 4, "term" : 60, "amount" : 50000 } )

    loans = [] 

    for data in datas :
        loans.append(LoanRequest.objects.create(
                user_id = int(data["user_id"]), 
                loan_simulation_status = 'Pending',
                loan_simulation_date_utc = None,
                loan_advisor_approval_status ='Pending',
                loan_advisor_approval_date_utc = None,
                name = "Simplon",
                city = "Lille",
                no_emp = 0, 
                franchise_code = 0, 
                state = "OH", #LoanRequest.StateType.choices[0][0],
                zip = None, 
                bank = "CAPITAL ONE NATL ASSOC",
                bank_state = "OH", #LoanRequest.BankStateType.choices[0][0],
                new_exist = '1.0' , #LoanRequest.BusinessType.choices[0][0], 
                term = data["term"], 
                naics="54", 
                approval_date = None,   
                approval_fy = "",
                create_job = 0,
                retained_job = 3,
                rev_line_cr = "N", # LoanRequest.RevLineCrType.choices[0][0], 
                low_doc = "N", #LoanRequest.LowDocType.choices[0][0],
                chg_off_date = None,
                disbursement_date = None,
                disbursement_gross = 0.0,
                balance_gross = 0.0,
                chg_off_prin_gr = 0.0, 
                gr_appv = float(data["amount"]),
                sba_appv = 0.0))

    loans : list[LoanRequest] = loans

    for loan in loans :
        loan.save()
        print(f"LoanRequest {loan.loan_nr_chk_dgt} créée avec succès par l'utilisateur {loan.user_id}.")


if __name__  == "__main__":
    # Configuration de Django
    os.environ['DJANGO_SETTINGS_MODULE'] = 'MySbaApp.settings'  # Remplace 'ton_projet' par le nom de ton projet Django
    django.setup()

    from django.contrib.auth.models import User
    from sbapp.models import UserProfile, LoanRequest

    populate_users()
    populate_loans()