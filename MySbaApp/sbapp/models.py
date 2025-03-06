import contextlib
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import RegexValidator
from datetime import datetime, date
from django.conf import settings
import random
from phonenumber_field.modelfields import PhoneNumberField

class UserProfile(AbstractUser):

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



class LoanRequest(models.Model):
    """Model representing a loan application"""

    # Link to the user (formerly 'username')
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='loan_requests')

    ### 🔹 Loan Identifier ###
    PREFIX = 1000  # Prefix for LoanNr_ChkDgt
    loan_nr_chk_dgt = models.CharField(primary_key=True, max_length=10, unique=True, db_index=True)

    ### Enterprise Name
    name = models.CharField(max_length=255, blank=True, help_text="Full Name of the Enterprise")
    
    ### 🔹 City where enterprise is located ###
    city = models.CharField(max_length=255, blank=True, help_text="City where enterprise is located")
    
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
    disbursement_gross = models.CharField(
        max_length=20, null=True, blank=True, help_text="Amount disbursed"
    )
    balance_gross = models.CharField(
        max_length=20, null=True, blank=True, help_text="Gross amount outstanding"
    )
    chg_off_prin_gr = models.CharField(
        max_length=20, null=True, blank=True, help_text="Charged-off amount"
    )
    gr_appv = models.CharField(
        max_length=20, null=True, blank=True, help_text="Gross amount of loan approved by bank"
    )
    sba_appv = models.CharField(
        max_length=20, null=True, blank=True, help_text="SBA’s guaranteed amount of approved loan"
    )
    loan_status = models.CharField(max_length=15, default='Pending')

    ### Derived Fields ###
    @property
    def recession(self):
        """Determines if the loan was active during the recession period."""
        recession_start = date(2007, 12, 1)
        recession_end = date(2009, 6, 30)
        if self.approval_date and recession_start <= self.approval_date <= recession_end:
            return 1
        return 0

    @property
    def has_franchise(self):
        """Determines if an enterprise is a franchise or not."""
        try:
            code = int(self.franchise_code)
        except (ValueError, TypeError):
            return 0
        return 1 if code > 1 else 0

    ### Helper Methods ###
    def format_currency(self, value):
        """
        Convert a numeric value (int/float) into a formatted currency string.
        e.g., 12345.67 -> "$12,345.67"
        Returns None if invalid.
        """
        if value is None:
            return None
        try:
            return f"${float(value):,.2f}"
        except Exception:
            return None
        
    def clean_numeric(self, value):
        """
        Convert a formatted currency string back to a float.
        e.g., "$12,345.67" -> 12345.67
        Returns None if invalid.
        """
        if not value:
            return None
        try:
            return float(value.replace("$", "").replace(",", ""))
        except Exception:
            return None


    def export_as_integer(self, value):
        """
        Convert a numeric value into an integer without decimals.
        e.g., 12345.67 -> 1234567
        Returns None if invalid.
        """
        if value is None:
            return None
        try:
            return int(float(value))
        except Exception:
            return None

    ### Overridden Save Method ###
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

        # Convert date fields if provided as strings.
        if self.approval_date and isinstance(self.approval_date, str):
            with contextlib.suppress(Exception):
                self.approval_date = datetime.strptime(self.approval_date, "%d-%b-%y").date()
        if self.disbursement_date and isinstance(self.disbursement_date, str):
            with contextlib.suppress(Exception):
                self.disbursement_date = datetime.strptime(self.disbursement_date, "%d-%b-%y").date()

        # Process currency fields.
        for field_name in [
            "disbursement_gross",
            "balance_gross",
            "chg_off_prin_gr",
            "gr_appv",
            "sba_appv",
        ]:
            value = getattr(self, field_name)
            numeric_value = self.clean_numeric(value)  # Clean input to numeric
            if numeric_value is not None:
                setattr(self, field_name, self.format_currency(numeric_value))  # Format as currency string

        super().save(*args, **kwargs)

    ### API Export Method ###
    def to_api_data(self):
        """
        Export the model data for API validation.
        Converts currency fields to integers and ensures all fields are properly formatted.
        """
        # Helper function to convert RevLineCr and LowDoc to integer (1 for 'Y', 0 for 'N' or None)
        def convert_yes_no_to_int(value):
            if value == "Y":
                return 1
            elif value == "N" or value is None:
                return 0
            return None

        # Helper function to convert UrbanRural to integer (1 for Urban, 2 for Rural, 0 for default/invalid)
        def convert_urban_rural_to_int(value):
            if value == "1":
                return 1
            elif value == "2":
                return 2
            return 0

        def convert_naics_to_int(value):
            if value.isdigit():
                return int(str(value)[:2])  # Convert to string, slice, then back to int
            raise ValueError("Invalid NAICS code: must be a numeric string")  # Handle invalid input

        def new_exists_to_int(value):
            return int(float(value)) if value and str(value).replace('.','',1).isdigit() else 0

        # Construct the API data dictionary
        api_data = {
            "state": self.state.upper() if self.state else None,  # Ensure state is uppercase
            "bank": self.bank.upper() if self.bank else None,  # Ensure bank name is uppercase
            "naics": convert_naics_to_int(self.naics),  # Safely convert NAICS to integer
            "term": self.term or 0,  # Default to 0 if term is missing
            "no_emp": self.no_emp or 0,  # Default to 0 if no_emp is missing
            "new_exist": new_exists_to_int(self.new_exist),  # Default to 0 if no_emp is missing
            "create_job": self.create_job or 0,  # Default to 0 if create_job is missing
            "retained_job": self.retained_job or 0,  # Default to 0 if retained_job is missing
            "urban_rural": convert_urban_rural_to_int(self.urban_rural),  # Convert UrbanRural to integer
            "rev_line_cr": convert_yes_no_to_int(self.rev_line_cr),  # Convert RevLineCr to integer
            "low_doc": convert_yes_no_to_int(self.low_doc),  # Convert LowDoc to integer
            "gr_appv": self.export_as_integer(self.clean_numeric(self.gr_appv)),  # Convert GrAppv to integer
            "recession": self.recession or random.randint(0,1),  # Use the derived property for recession status
            "has_franchise": self.has_franchise,  # Use the derived property for franchise status
        }

        return api_data
        

    def __str__(self):
        return self.loan_nr_chk_dgt
    

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