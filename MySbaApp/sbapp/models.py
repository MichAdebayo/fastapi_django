import contextlib
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import RegexValidator
from datetime import datetime, date
from django.conf import settings
import random
from phonenumber_field.modelfields import PhoneNumberField


#______________________________________________________________________________
#
# region Newscast
#______________________________________________________________________________
class Newscast(models.Model) :
    """
    Table news: Stocke les actualités publiées sur la page d’accueil.
    """

    id =  models.IntegerField(primary_key=True,unique=True, db_index=True)
    title =  models.CharField(max_length=255)
    content =  models.TextField()
    publication_date_utc = models.DateField()
    published_by = models.ForeignKey('UserProfile', on_delete=models.CASCADE)

    class Meta:
        db_table = 'sba_news'  


#______________________________________________________________________________
#
# region Message
#______________________________________________________________________________
class Message (models.Model) :
    """
    Table messages: Stocke les messages échangés entre clients et conseillers.
    """

    id =  models.IntegerField(primary_key=True,unique=True, db_index=True)
    user_id = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    content =  models.TextField()
    issue_time_utc = models.DateTimeField()
    

    class Meta:
        db_table = 'sba_messages'  
    

#______________________________________________________________________________
#
# region UserProfile
#______________________________________________________________________________
class UserProfile(AbstractUser):
    """
    Table users: Stocke les informations des clients et conseillers.
    """

    class Meta:
        db_table = 'sba_users'  

    ### 🔹 Other Contact Information ###
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True)

    # Additional fields
    # date_of_birth = models.DateField(null=True, blank=True)
    # gender = models.CharField(
    #     max_length=10,
    #     choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
    #     null=True, blank=True
    # )
    # occupation = models.CharField(max_length=255, blank=True, null=True)
    # company_name = models.CharField(max_length=255, blank=True, null=True)
    # marital_status = models.CharField(
    #     max_length=15,
    #     choices=[('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced'), ('Widowed', 'Widowed')],
    #     null=True, blank=True
    # )
    # nationality = models.CharField(max_length=100, blank=True, null=True)
    # profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
    
    
#______________________________________________________________________________
#
# region LoanResponseInfo
#______________________________________________________________________________
class LoanResponseInfo(models.Model) :
    """
    Table loan_response_info : Stocke les données relatives à une prédiction.
    """
    
    approval_status = models.CharField(max_length=15)
    approval_proba_0 = models.DecimalField(max_digits = 7, decimal_places=6)
    approval_proba_1 = models.DecimalField(max_digits = 7, decimal_places=6)
    feat_imp_state = models.DecimalField(max_digits = 8, decimal_places=2)
    feat_imp_bank = models.DecimalField(max_digits = 8, decimal_places=2)
    feat_imp_naics = models.DecimalField(max_digits = 8, decimal_places=2)
    feat_imp_term = models.DecimalField(max_digits = 8, decimal_places=2) 
    feat_imp_no_emp = models.DecimalField(max_digits = 8, decimal_places=2)
    feat_imp_new_exist = models.DecimalField(max_digits = 8, decimal_places=2) 
    feat_imp_create_job = models.DecimalField(max_digits = 8, decimal_places=2)  
    feat_imp_retained_job = models.DecimalField(max_digits = 8, decimal_places=2)  
    feat_imp_urban_rural = models.DecimalField(max_digits = 8, decimal_places=2)  
    feat_imp_rev_line_cr = models.DecimalField(max_digits = 8, decimal_places=2) 
    feat_imp_low_doc = models.DecimalField(max_digits = 8, decimal_places=2)  
    feat_imp_gr_appv = models.DecimalField(max_digits = 8, decimal_places=2)  
    feat_imp_recession = models.DecimalField(max_digits = 8, decimal_places=2)  
    feat_imp_has_franchise = models.DecimalField(max_digits = 8, decimal_places=2)

    class Meta:
        db_table = 'sba_loan_data'  

#______________________________________________________________________________
#
# region LoanRequest
#______________________________________________________________________________
class LoanRequest(models.Model):
    """
    Table loan_requests: Stocke les demandes de prêt et leur statut.
    """

    class Meta:
        db_table = 'sba_loan_requests'  

    ### 🔹 Loan Identifier ###
    PREFIX = 1000  # Prefix for LoanNr_ChkDgt
    loan_nr_chk_dgt = models.CharField(primary_key=True, max_length=10, unique=True, db_index=True)

    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='loan_requests')
    data = models.ForeignKey('LoanResponseInfo', on_delete=models.CASCADE, related_name='loan_requests', null=True)

    loan_simulation_status = models.CharField(max_length=15, default='Pending')
    loan_simulation_date_utc = models.DateField(null=True, blank=True, help_text="Date simulation commitment issued")

    loan_advisor_approval_status = models.CharField(max_length=15, default='Pending')
    loan_advisor_approval_date_utc = models.DateField(null=True, blank=True, help_text="Date advisor commitment issued")
        
    ### Enterprise Name
    name = models.CharField(max_length=255, blank=True, help_text="Full Name of the Enterprise")
    
    ### 🔹 City where enterprise is located ###
    city = models.CharField(max_length=255)
    
    ### 🔹 Number of Employees ###
    no_emp = models.PositiveSmallIntegerField(default=1, help_text="Number of employees")

    ### 🔹 Enterprise Franchise Code ###
    # Using a positive small integer to capture franchise code.
    franchise_code = models.PositiveSmallIntegerField(default=0, help_text="Enterprise Franchise Code")

    ### 🔹 Enterprise State ###
    class StateType(models.TextChoices):
        AL = 'AL', 'Alabama'
        AK = 'AK', 'Alaska'
        AZ = 'AZ', 'Arizona'
        AR = 'AR', 'Arkansas'
        CA = 'CA', 'California'
        CO = 'CO', 'Colorado'
        CT = 'CT', 'Connecticut'
        DE = 'DE', 'Delaware'
        DC = 'DC', 'District of Columbia'
        FL = 'FL', 'Florida'
        GA = 'GA', 'Georgia'
        HI = 'HI', 'Hawaii'
        ID = 'ID', 'Idaho'
        IL = 'IL', 'Illinois'
        IN = 'IN', 'Indiana'
        IA = 'IA', 'Iowa'
        KS = 'KS', 'Kansas'
        KY = 'KY', 'Kentucky'
        LA = 'LA', 'Louisiana'
        ME = 'ME', 'Maine'
        MD = 'MD', 'Maryland'
        MA = 'MA', 'Massachusetts'
        MI = 'MI', 'Michigan'
        MN = 'MN', 'Minnesota'
        MS = 'MS', 'Mississippi'
        MO = 'MO', 'Missouri'
        MT = 'MT', 'Montana'
        NE = 'NE', 'Nebraska'
        NV = 'NV', 'Nevada'
        NH = 'NH', 'New Hampshire'
        NJ = 'NJ', 'New Jersey'
        NM = 'NM', 'New Mexico'
        NY = 'NY', 'New York'
        NC = 'NC', 'North Carolina'
        ND = 'ND', 'North Dakota'
        OH = 'OH', 'Ohio'
        OK = 'OK', 'Oklahoma'
        OR = 'OR', 'Oregon'
        PA = 'PA', 'Pennsylvania'
        RI = 'RI', 'Rhode Island'
        SC = 'SC', 'South Carolina'
        SD = 'SD', 'South Dakota'
        TN = 'TN', 'Tennessee'
        TX = 'TX', 'Texas'
        UT = 'UT', 'Utah'
        VT = 'VT', 'Vermont'
        VA = 'VA', 'Virginia'
        WA = 'WA', 'Washington'
        WV = 'WV', 'West Virginia'
        WI = 'WI', 'Wisconsin'
        WY = 'WY', 'Wyoming'
    state = models.CharField(max_length=2, choices=StateType.choices)

    ### 🔹 City Zip Code ###
    zip = models.CharField(max_length=5, blank=True, null=True) 

    ### 🔹 Enterprise Bank ###
    bank = models.CharField(max_length=255, default="UB")

    ### 🔹 Bank State ###
    class BankStateType(models.TextChoices):
        AL = 'AL', 'Alabama'
        AK = 'AK', 'Alaska'
        AZ = 'AZ', 'Arizona'
        AR = 'AR', 'Arkansas'
        CA = 'CA', 'California'
        CO = 'CO', 'Colorado'
        CT = 'CT', 'Connecticut'
        DE = 'DE', 'Delaware'
        DC = 'DC', 'District of Columbia'
        FL = 'FL', 'Florida'
        GA = 'GA', 'Georgia'
        HI = 'HI', 'Hawaii'
        ID = 'ID', 'Idaho'
        IL = 'IL', 'Illinois'
        IN = 'IN', 'Indiana'
        IA = 'IA', 'Iowa'
        KS = 'KS', 'Kansas'
        KY = 'KY', 'Kentucky'
        LA = 'LA', 'Louisiana'
        ME = 'ME', 'Maine'
        MD = 'MD', 'Maryland'
        MA = 'MA', 'Massachusetts'
        MI = 'MI', 'Michigan'
        MN = 'MN', 'Minnesota'
        MS = 'MS', 'Mississippi'
        MO = 'MO', 'Missouri'
        MT = 'MT', 'Montana'
        NE = 'NE', 'Nebraska'
        NV = 'NV', 'Nevada'
        NH = 'NH', 'New Hampshire'
        NJ = 'NJ', 'New Jersey'
        NM = 'NM', 'New Mexico'
        NY = 'NY', 'New York'
        NC = 'NC', 'North Carolina'
        ND = 'ND', 'North Dakota'
        OH = 'OH', 'Ohio'
        OK = 'OK', 'Oklahoma'
        OR = 'OR', 'Oregon'
        PA = 'PA', 'Pennsylvania'
        RI = 'RI', 'Rhode Island'
        SC = 'SC', 'South Carolina'
        SD = 'SD', 'South Dakota'
        TN = 'TN', 'Tennessee'
        TX = 'TX', 'Texas'
        UT = 'UT', 'Utah'
        VT = 'VT', 'Vermont'
        VA = 'VA', 'Virginia'
        WA = 'WA', 'Washington'
        WV = 'WV', 'West Virginia'
        WI = 'WI', 'Wisconsin'
        WY = 'WY', 'Wyoming'
        PR = 'PR', 'Puerto Rico'
        GU = 'GU', 'Guam'
        AN = 'AN', 'AN'
        EN = 'EN', 'EN'
        VI = 'VI', 'Virgin Islands'
    bank_state = models.CharField(max_length=2, choices=BankStateType.choices, blank=True, default="UB")

    ### 🔹 Type of Business (New vs Existing) ###
    # Improved with more intuitive codes.
    class BusinessType(models.TextChoices):
        EXISTING_BUSINESS = '1.0', 'Existing Business'
        NEW_BUSINESS = '2.0', 'New Business'
    new_exist = models.CharField(max_length=3, choices=BusinessType.choices, blank=True, default='0.0')

    ### 🔹 Loan Term (Months) ###
    term = models.PositiveSmallIntegerField(default=1, help_text="Loan term in months")

    ### 🔹 Enterprise's NAICS Code ###
    naics = models.CharField(max_length=6, blank=True, default="0", help_text="North American Industry Classification System Code")

    ### 🔹 Loan Approval Date (stored as DateField) ###
    approval_date = models.DateField(null=True, blank=True, help_text="Date SBA commitment issued")
    
    def get_approval_date_formatted(self):
        """Return ApprovalDate formatted as DD-MMM-YY (e.g., '28-Feb-89')"""
        return self.approval_date.strftime("%d-%b-%y") if self.approval_date else None

    ### 🔹 Loan Approval Fiscal Year ###
    @staticmethod
    def get_year_choices():
        """Generate a list of years from 1980 to the current year + 1."""
        return [(str(year), str(year)) for year in range(1980, datetime.now().year + 2)]
    
    approval_fy = models.CharField(
        max_length=4,
        choices=get_year_choices(),
        null=True,
        blank=True,
        help_text="Fiscal Year of commitment"
    )

    ### 🔹 Jobs Created / Retained ###
    create_job = models.PositiveIntegerField(default=0, help_text="Number of jobs created")
    retained_job = models.PositiveIntegerField(default=0, help_text="Number of jobs retained")

    ### 🔹 Enterprise Class Type (Urban/Rural) ###
    class UrbanRuralType(models.TextChoices):
        URBAN = '1', 'Urban'
        RURAL = '2', 'Rural'
    urban_rural = models.CharField(max_length=1, choices=UrbanRuralType.choices, blank=True, default='0')

    ### 🔹 Loan Class (Revolving Line of Credit vs. Not) ###
    class RevLineCrType(models.TextChoices):
        YES = 'Y', 'Yes'
        NO = 'N', 'No'
    rev_line_cr = models.CharField(max_length=1, choices=RevLineCrType.choices, blank=True, null=True, help_text="Revolving line of credit")

    ### 🔹 Documentation Type (LowDoc vs. Heavy Doc) ###
    class LowDocType(models.TextChoices):
        YES = 'Y', 'Yes'
        NO = 'N', 'No'
    low_doc = models.CharField(max_length=1, choices=LowDocType.choices, blank=True, null=True, help_text="LowDoc Loan Program")

    ### 🔹 Default Date (e.g., charged off date) ###
    chg_off_date = models.DateField(null=True, blank=True, help_text="Date when loan is declared in default")

    ### 🔹 Disbursement Date (stored as DateField) ###
    disbursement_date = models.DateField(null=True, blank=True, help_text="Disbursement date")
    
    def get_disbursement_date_formatted(self):
        """Return DisbursementDate formatted as DD-MMM-YY"""
        return self.disbursement_date.strftime("%d-%b-%y") if self.disbursement_date else None 

    ### 🔹 Currency Fields ###
    # Using DecimalFields to store monetary values accurately.
    disbursement_gross = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text="Amount disbursed")
    balance_gross = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text="Gross amount outstanding")
    chg_off_prin_gr = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text="Charged-off amount")
    gr_appv = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text="Gross amount of loan approved by bank")
    sba_appv = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text="SBA’s guaranteed amount of approved loan")
   

    # Derived Field: Recession status
    @property
    def recession(self):
        """Determines if the loan was active during the recession period."""
        recession_start = date(2007, 12, 1)
        recession_end = date(2009, 6, 30)
        if self.approval_date and recession_start <= self.approval_date <= recession_end:
            return 1
        return 0
    
    # Derived Field: Franchise status
    @property
    def has_franchise(self):
        """Determines if an enterprise is a franchise or not."""
        try:
            code = int(self.franchise_code)
        except (ValueError, TypeError):
            return 0
        return 1 if code > 1 else 0

    def format_currency(self, value):
        """Convert a numeric value to a formatted currency string."""
        if value is None or value == "":
            return None
        try:
            return f"${float(value):,.2f}"
        except Exception:
            return value

    def clean_numeric(self, value):
        """Convert a currency string back to a float (removes '$' and ',')."""
        if value is None or value == "":
            return None
        return float(value.replace("$", "").replace(",", ""))

    # Consolidated save() method
    def save(self, *args, **kwargs):
        # Auto-generate LoanNr_ChkDgt if not provided.
        if not self.loan_nr_chk_dgt:
            loan_suffix = str(random.randint(100000, 999999))
            self.loan_nr_chk_dgt = f"{self.PREFIX}{loan_suffix}"

        # Convert text fields to uppercase.
        if self.name and isinstance(self.name, str):
            self.name = self.name.upper()
        if self.city and isinstance(self.city, str):
            self.city = self.city.upper()
        if self.bank and isinstance(self.bank, str):
            self.bank = self.bank.upper()

        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.loan_nr_chk_dgt



#     # # ### 🔹 Enterprise's NAICS Code ###
#     # naics = models.CharField(default="0", blank=True, max_length=6, help_text="North American Industry Classification System Code")

#     ### 🔹 Loan Approval Date (stored as DateField; display in dd-MMM-yy format) ###
#     # approval_date = models.DateField(null=True, blank=True, help_text="Date SBA commitment issued")
    
#     # def get_approval_date_formatted(self):
#     #     """Return ApprovalDate formatted as DD-MMM-YY (e.g., '28-Feb-89')"""
#     #     return self.approval_date.strftime("%d-%b-%y") if self.approval_date else None

#     ### 🔹 Loan Approval Fiscal Year ###
#     # @staticmethod
#     # def get_year_choices():
#     #     """Generate a list of years from 1980 to the current year + 1."""
#     #     return [(str(year), str(year)) for year in range(1980, datetime.now().year + 2)]
    
#     # approval_fy = models.CharField(
#     #     choices=get_year_choices(),
#     #     null=True,
#     #     blank=True,
#     #     max_length=4,
#     #     help_text="Fiscal Year of commitment"
#     # )



    


#     # ### 🔹 Jobs Created / Retained ###
#     # create_job = models.PositiveIntegerField(default=0, help_text="Number of jobs created")
#     # retained_job = models.PositiveIntegerField(default=0, help_text="Number of jobs retained")
    


#     ### 🔹 Enterprise Class Type (Urban/Rural) ###
#     # class UrbanRuralType(models.TextChoices):
#     #     URBAN = '1', 'Urban'
#     #     RURAL = '2', 'Rural'
#     # urban_rural = models.CharField(blank=True, max_length=1, choices=UrbanRuralType.choices, default='0', )

#     ### 🔹 Loan Class (Revolving Line of Credit vs. Not) ###
#     # class RevLineCrType(models.TextChoices):
#     #     YES = 'Y', 'Yes'
#     #     NO = 'N', 'No'
#     # rev_line_cr = models.CharField(blank=True, null=True, choices=RevLineCrType.choices, max_length=1, help_text="Revolving line of credit")

#     # ### 🔹 Documentation Type (LowDoc vs. Heavy Doc) ###
#     # class LowDocType(models.TextChoices):
#     #     YES = 'Y', 'Yes'
#     #     NO = 'N', 'No'
#     # low_doc = models.CharField(blank=True, null=True, choices=LowDocType.choices, max_length=1, help_text="LowDoc Loan Program")

#     ### 🔹 Default Date (e.g., charged off date) ###
#     # chg_off_date = models.DateField(null=True, blank=True, help_text="Date when loan is declared in default")

#     ### 🔹 Disbursement Date (stored as DateField; display in dd-MMM-yy format) ###
#     # disbursement_date = models.DateField(null=True, blank=True, help_text="Disbursement date")
    
#     # def get_disbursement_date_formatted(self):
#     #     """Return DisbursementDate formatted as DD-MMM-YY"""
#     #     return self.disbursement_date.strftime("%d-%b-%y") if self.disbursement_date else None 

#     ### 🔹 Currency Fields ###
#     # currency_regex = RegexValidator(
#     #     regex=r'^\$?\d{1,3}(,\d{3})*(\.\d{2})?$',
#     #     message="Enter a valid currency amount (e.g., 1,000.00 or 100.50)."
#     # )
#     # disbursement_gross = models.CharField(null=True, blank=True, max_length=10, validators=[currency_regex], help_text="Amount disbursed")
#     # balance_gross = models.CharField(null=True, blank=True, max_length=20, validators=[currency_regex], help_text="Gross amount outstanding")
#     # chg_off_prin_gr = models.CharField(null=True, blank=True, max_length=20, validators=[currency_regex], help_text="Charged-off amount")
#     # gr_appv = models.CharField(null=True, blank=True, max_length=20, validators=[currency_regex], help_text="Gross amount of loan approved by bank")
#     # sba_appv = models.CharField(null=True, blank=True, max_length=20, validators=[currency_regex], help_text="SBA’s guaranteed amount of approved loan")
#     # loan_status = models.CharField(max_length=15, default='Pending')

#     # Derived Field
#     # @property
#     # def recession(self):
#     #     """Determines if the loan was active during the recession period."""
#     #     recession_start = date(2007, 12, 1)
#     #     recession_end = date(2009, 6, 30)
#     #     if self.approval_date and recession_start <= self.approval_date <= recession_end:
#     #         return 1
#     #     return 0
    
#     # Derived Field
#     # @property
#     # def has_franchise(self):
#     #     """Determines if an enterprise is a franchise or not."""
#     #     try:
#     #         code = int(self.franchise_code)
#     #     except (ValueError, TypeError):
#     #         # If conversion fails, consider it not a franchise.
#     #         return 0

#     #     # If the code is greater than 1, it's considered a franchise.
#     #     return 1 if code > 1 else 0

#     # def format_currency(self, value):
#     #     """Convert a numeric value (int/float) to a formatted currency string."""
#     #     if value is None or value == "":
#     #         return None
#     #     try:
#     #         return f"${float(value):,.2f}"
#     #     except Exception:
#     #         return value  # Return as-is if conversion fails

#     # def clean_numeric(self, value):
#     #     """Convert a currency string back to a float (removes '$' and ',')."""
#     #     if value is None or value == "":
#     #         return None
#     #     return float(value.replace("$", "").replace(",", ""))
    

#     # --- Consolidated save() method ---
#     def save(self, *args, **kwargs):
#         # 1. Auto-generate LoanNr_ChkDgt if not provided.
#         if not self.loan_nr_chk_dgt:
#             loan_suffix = str(random.randint(100000, 999999))
#             self.loan_nr_chk_dgt = f"{self.PREFIX}{loan_suffix}"

#         # 2. Convert text fields to uppercase.
#         if self.name and isinstance(self.name, str):
#             self.name = self.name.upper()
#         if self.city and isinstance(self.city, str):
#             self.city = self.city.upper()
#         if self.bank and isinstance(self.bank, str):
#             self.bank = self.bank.upper()

#         # 3. Convert date fields if provided as strings.
#         # if self.ApprovalDate and isinstance(self.approval_date, str):
#         #     with contextlib.suppress(Exception):
#         #         self.ApprovalDate = datetime.strptime(self.approval_date, "%d-%b-%y").date()
#         # if self.disbursement_date and isinstance(self.disbursement_date, str):
#         #     with contextlib.suppress(Exception):
#         #         self.disbursement_date = datetime.strptime(self.disbursement_date, "%d-%b-%y").date()
#         # # 4. Format currency fields.
#         # self.disbursement_gross = self.format_currency(self.clean_numeric(self.disbursement_gross))
#         # self.balance_gross = self.format_currency(self.clean_numeric(self.balance_gross))
#         # self.chg_off_prin_gr = self.format_currency(self.clean_numeric(self.chg_off_prin_gr))
#         # self.gr_appv = self.format_currency(self.clean_numeric(self.gr_appv))
#         # self.sba_appv = self.format_currency(self.clean_numeric(self.sba_appv))

#         super().save(*args, **kwargs)
    
#     def __str__(self):
#         return self.username
    
# class Messages(models.Model):

#     name = models.CharField(max_length=255)
#     email = models.EmailField()
#     message = models.TextField()
#     submitted_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name
    

# class News(models.Model):

#     author = models.CharField(max_length=50)
#     headline = models.CharField(max_length=255)
#     body_text = models.TextField()
#     pub_date = models.DateField()
#     mod_date = models.DateField(default=date.today)
#     related_program = models.CharField(max_length=100)

#     def __str__(self):
#         return self.headline
    

# class Appointment(models.Model):

#     REASON_CHOICES = [
#     ("Loan Application Assistance", "Loan Application Assistance"),
#     ("Business Plan Review", "Business Plan Review"),
#     ("Financial Advisory", "Financial Advisory"),
#     ("Loan Repayment Support", "Loan Repayment Support"),
#     ("Grant and Funding Opportunities", "Grant and Funding Opportunities"),
# ]

#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     reason = models.CharField(max_length=50, choices=REASON_CHOICES)
#     date = models.DateField(default=date(2025, 2, 3))  # Correct default date
#     time = models.CharField(max_length=10)

#     def __str__(self):
#         return f"{self.reason} on {self.date} at {self.time}"