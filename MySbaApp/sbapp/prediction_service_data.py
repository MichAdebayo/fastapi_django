from pydantic import BaseModel, Field
from typing import Optional

#______________________________________________________________________________
#
# region AuthData données utilisées pour le login 
#______________________________________________________________________________
class AuthData(BaseModel):
    email:str
    password:str

#______________________________________________________________________________
#
# region JWT Web Token
#______________________________________________________________________________
class Token(BaseModel):
    access_token: str  # Le token d'accès généré
    token_type: str    # Le type du token, généralement "bearer"

#______________________________________________________________________________
#
# region User activation Data
#______________________________________________________________________________
class UserActivationData(BaseModel):
    """
    User activation Data
    """
    new_password : str

#______________________________________________________________________________
#
# region User information data
#______________________________________________________________________________
class UserInfoData(BaseModel):
    """
    User information data 
    """
    email: str
    username : Optional [str] = None
    is_active : bool
    role: str = "user"

#______________________________________________________________________________
#
# region Creation data needed for a User 
#______________________________________________________________________________
class UserCreationData(BaseModel):
    """
    All data excluded 'is_active' field
    """
    email: str
    username : Optional [str] = None
    role: str = "user"
    password : str


#______________________________________________________________________________
#
# region Loan request Data
#______________________________________________________________________________
class LoanRequestData(BaseModel):
    """
    data used for loan prediction
    """
    state : str = Field(description = "State, encoded on 2 characters")
    """State, encoded on 2 characters"""

    bank : str = Field(description = "Bank name")
    """Bank name"""

    naics : int = Field(description = "North American industry classiﬁcation system code, \n first two characters")
    """North American industry classiﬁcation system code, \n first two characters"""

    term : int = Field(description = "Loan term in months")
    """Loan term in months"""

    no_emp : int = Field(description = "Number of business employees")
    """Number of business employees"""

    new_exist : int = Field(description = "1 = Existing business, 2 = New business") # bool 
    """1 = Existing business, 2 = New business"""

    create_job : int = Field(description = "number of jobs created")
    """number of jobs created"""

    retained_job: int = Field(description = "number of jobs saved")
    """number of jobs saved"""

    urban_rural: int = Field(description = "1 = Urban, 2 = rural, 0 = undeﬁned") 
    """1 = Urban, 2 = rural, 0 = undeﬁned"""
    rev_line_cr: int = Field(description = "Revolving line of credit: 1 = Yes, 0 = No")
    """Revolving line of credit: 1 = Yes, 0 = No"""

    low_doc : int = Field(description = "LowDoc Loan Program: 1 = Yes, 0 = No")
    """LowDoc Loan Program: 1 = Yes, 0 = No"""

    gr_appv: int = Field(description = "Gross amount of loan approved by bank")
    """Gross amount of loan approved by bank"""

    recession: int = Field(description = "From December 2007 to June 2009")
    """From December 2007 to June 2009"""

    has_franchise: int = Field(description = "has a franchise code or not")
    """has a franchise code or not"""

#______________________________________________________________________________
#
# region Loan response Data
#______________________________________________________________________________
class LoanResponseData(BaseModel):
    approval_status : str
    approval_proba_0 : float
    approval_proba_1 : float
    feat_imp_state : float
    feat_imp_bank : float  
    feat_imp_naics : float  
    feat_imp_term : float  
    feat_imp_no_emp : float  
    feat_imp_new_exist : float  
    feat_imp_create_job : float  
    feat_imp_retained_job : float  
    feat_imp_urban_rural : float  
    feat_imp_rev_line_cr : float  
    feat_imp_low_doc : float  
    feat_imp_gr_appv : float  
    feat_imp_recession : float  
    feat_imp_has_franchise : float

#______________________________________________________________________________
#
# region Loan info Data
#______________________________________________________________________________
class LoanInfoData(LoanRequestData):
    approval_status : Optional[str]


