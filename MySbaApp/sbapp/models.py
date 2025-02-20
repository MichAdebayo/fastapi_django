from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import RegexValidator
from datetime import datetime, date
import random

class LoanRequestUserProfile(AbstractUser):
    """Model representing a loan application"""

    # --- Override default relations with custom related_names ---
    groups = models.ManyToManyField(
        Group,
        related_name="loanrequestuserprofile_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="loanrequestuserprofile_permissions",
        blank=True
    )

    ### 🔹 Loan Identifier ###
    PREFIX = 1000  # Prefix for LoanNr_ChkDgt
    LoanNr_ChkDgt = models.CharField(primary_key=True, max_length=10, unique=True, db_index=True)

    ### Enterprise Name
    Name = models.CharField(null=True, blank=True, max_length=255, help_text="Full Name of the Enterprise")
    
    ### 🔹 City where enterprise is located ###
    City = models.CharField(max_length=255)
    
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
    State = models.CharField(choices=StateType.choices, max_length=2)

    ### 🔹 City Zip Code ###
    Zip = models.CharField(max_length=5, blank=True, null=True) 

    ### 🔹 Enterprise Bank ###
    Bank = models.CharField(max_length=255, default="UB")

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
        EN = 'EN', 'EN ' 
        VI = 'VI', 'Virgin Islands'
    BankState = models.CharField(default="UB", max_length=2, choices=BankStateType.choices)

    ### 🔹 Enterprise's NAICS Code ###
    NAICS = models.CharField(null=True, blank=True, max_length=6, help_text="North American Industry Classification System Code")

    ### 🔹 Loan Approval Date (stored as DateField; display in dd-MMM-yy format) ###
    ApprovalDate = models.DateField(null=True, blank=True, help_text="Date SBA commitment issued")
    
    def get_approval_date_formatted(self):
        """Return ApprovalDate formatted as DD-MMM-YY (e.g., '28-Feb-89')"""
        return self.ApprovalDate.strftime("%d-%b-%y") if self.ApprovalDate else None

    ### 🔹 Loan Approval Fiscal Year ###
    @staticmethod
    def get_year_choices():
        """Generate a list of years from 1980 to the current year + 1."""
        return [(str(year), str(year)) for year in range(1980, datetime.now().year + 2)]
    
    ApprovalFY = models.CharField(
        choices=get_year_choices(),
        null=True,
        blank=True,
        max_length=4,
        help_text="Fiscal Year of commitment"
    )

    ### 🔹 Loan Term (Months) ###
    Term = models.PositiveIntegerField(default=1, help_text="Loan term in months")

    ### 🔹 Number of Employees ###
    NoEmp = models.PositiveIntegerField(default=0, help_text="Number of employees")
    
    ### 🔹 Type of Business (New vs Existing) ###
    class NewExistType(models.TextChoices):
        EXISTING_BUSINESS = '1.0', 'Existing Business'
        NEW_BUSINESS = '2.0', 'New Business'
    NewExist = models.CharField(default='0.0', blank=True, choices=NewExistType.choices, max_length=3)

    ### 🔹 Jobs Created / Retained ###
    CreateJob = models.PositiveIntegerField(default=0, help_text="Number of jobs created")
    RetainedJob = models.PositiveIntegerField(default=0, help_text="Number of jobs retained")
    
    ### 🔹 Enterprise Franchise Code ###
    FranchiseCode = models.CharField(max_length=5, blank=True, default='00000')

    ### 🔹 Enterprise Class Type (Urban/Rural) ###
    class UrbanRuralType(models.TextChoices):
        URBAN = '1', 'Urban'
        RURAL = '2', 'Rural'
    UrbanRural = models.CharField(blank=True, max_length=1, choices=UrbanRuralType.choices, default='0', )

    ### 🔹 Loan Class (Revolving Line of Credit vs. Not) ###
    class RevLineCrType(models.TextChoices):
        YES = 'Y', 'Yes'
        NO = 'N', 'No'
    RevLineCr = models.CharField(blank=True, null=True, choices=RevLineCrType.choices, max_length=1, help_text="Revolving line of credit")

    ### 🔹 Documentation Type (LowDoc vs. Heavy Doc) ###
    class LowDocType(models.TextChoices):
        YES = 'Y', 'Yes'
        NO = 'N', 'No'
    LowDoc = models.CharField(blank=True, null=True, choices=LowDocType.choices, max_length=1, help_text="LowDoc Loan Program")

    ### 🔹 Default Date (e.g., charged off date) ###
    ChgOffDate = models.DateField(null=True, blank=True, help_text="Date when loan is declared in default")

    ### 🔹 Disbursement Date (stored as DateField; display in dd-MMM-yy format) ###
    DisbursementDate = models.DateField(null=True, blank=True, help_text="Disbursement date")
    
    def get_disbursement_date_formatted(self):
        """Return DisbursementDate formatted as DD-MMM-YY"""
        return self.DisbursementDate.strftime("%d-%b-%y") if self.DisbursementDate else None 

    ### 🔹 Currency Fields ###
    currency_regex = RegexValidator(
        regex=r'^\$?\d{1,3}(,\d{3})*(\.\d{2})?$',
        message="Enter a valid currency amount (e.g., 1,000.00 or 100.50)."
    )
    DisbursementGross = models.CharField(null=True, blank=True, max_length=10, validators=[currency_regex], help_text="Amount disbursed")
    BalanceGross = models.CharField(null=True, blank=True, max_length=20, validators=[currency_regex], help_text="Gross amount outstanding")
    ChgOffPrinGr = models.CharField(null=True, blank=True, max_length=20, validators=[currency_regex], help_text="Charged-off amount")
    GrAppv = models.CharField(null=True, blank=True, max_length=20, validators=[currency_regex], help_text="Gross amount of loan approved by bank")
    SBA_Appv = models.CharField(null=True, blank=True, max_length=20, validators=[currency_regex], help_text="SBA’s guaranteed amount of approved loan")
    
    def format_currency(self, value):
        """Convert a numeric value (int/float) to a formatted currency string."""
        if value is None or value == "":
            return None
        try:
            return f"${float(value):,.2f}"
        except Exception:
            return value  # Return as-is if conversion fails

    def clean_numeric(self, value):
        """Convert a currency string back to a float (removes '$' and ',')."""
        if value is None or value == "":
            return None
        return float(value.replace("$", "").replace(",", ""))
    

    # --- Consolidated save() method ---
    def save(self, *args, **kwargs):
        # 1. Auto-generate LoanNr_ChkDgt if not provided.
        if not self.LoanNr_ChkDgt:
            loan_suffix = str(random.randint(100000, 999999))
            self.LoanNr_ChkDgt = f"{self.PREFIX}{loan_suffix}"
        
        # 2. Convert text fields to uppercase.
        if self.Name and isinstance(self.Name, str):
            self.Name = self.Name.upper()
        if self.City and isinstance(self.City, str):
            self.City = self.City.upper()
        if self.Bank and isinstance(self.Bank, str):
            self.Bank = self.Bank.upper()
        
        # 3. Convert date fields if provided as strings.
        if self.ApprovalDate and isinstance(self.ApprovalDate, str):
            try:
                self.ApprovalDate = datetime.strptime(self.ApprovalDate, "%d-%b-%y").date()
            except Exception:
                pass
        if self.DisbursementDate and isinstance(self.DisbursementDate, str):
            try:
                self.DisbursementDate = datetime.strptime(self.DisbursementDate, "%d-%b-%y").date()
            except Exception:
                pass
        
        # 4. Format currency fields.
        self.DisbursementGross = self.format_currency(self.clean_numeric(self.DisbursementGross))
        self.BalanceGross = self.format_currency(self.clean_numeric(self.BalanceGross))
        self.ChgOffPrinGr = self.format_currency(self.clean_numeric(self.ChgOffPrinGr))
        self.GrAppv = self.format_currency(self.clean_numeric(self.GrAppv))
        self.SBA_Appv = self.format_currency(self.clean_numeric(self.SBA_Appv))
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.username