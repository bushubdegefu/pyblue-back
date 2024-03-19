import uuid
from datetime import datetime
from typing import List, Optional, Literal
from pydantic import BaseModel, EmailStr, validator
from pydantic.types import SecretStr




class EndPointsModel(BaseModel):
    id: int 
    name: str
    route_paths: str 
    description: str
    method: str 
    feature_id: Optional[int] = None

    class Config:
        from_attributes = True

class EndPointsPostModel(BaseModel):
    name: str
    route_paths: str 
    description: str
    method: str 
    feature_id: Optional[int] = None

    class Config:
        from_attributes = True

class EndPointsDropModel(BaseModel):
    id: int 
    name: str
    route_paths: str 
   
    class Config:
        from_attributes = True


class AppModel(BaseModel):
    id: int
    name: str
    
    class Config:
        from_attributes = True
        #extra = "allow"


class RoleModelMatrix(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        from_attributes = True
        #extra = "allow"

class UserModelPost(BaseModel):
    email: EmailStr
    password: str
    disabled: Optional[bool]
    
    # class Config:
        #extra = "allow"

class UserModel(BaseModel):
    email: EmailStr
    password: SecretStr
    disabled: Optional[bool]

    class Config:
        from_attributes = True
        #extra = "allow"      

class UserModelAll(BaseModel):
    id: Optional[int]
    email: Optional[EmailStr]
    password: Optional[str]
    disabled: Optional[bool]
    date_registered: Optional[datetime]
    roles: Optional[List[RoleModelMatrix]] = []

    class Config:
        from_attributes = True
        #extra = "allow"

class UserModelUpdate(BaseModel):
    email: Optional[EmailStr]
    date_registered: Optional[datetime]

    # class Config:
        #extra = "allow"
 
class LoginUserModel(BaseModel):
    grant_type: Literal['authorization_code', 'refresh_token', 'token_decode'] = "authorization_code"
    email: EmailStr
    password: str
    token: Optional[str] = 'none'

    # class Config:
        #extra = "allow"       

class RoleModel(BaseModel):
    name: str
    description: Optional[str]
    app_id: Optional[int]

    class Config:
        from_attributes = True

class PageModel(BaseModel):
    id: int
    name: str 
    active: bool
    description: str 
    roles: Optional[List[RoleModel]]
    
    class Config:
        from_attributes = True

class PagePostModel(BaseModel):
    name: str 
    active: bool
    description: str 
    
    class Config:
        from_attributes = True
    
class PageDropModel(BaseModel):
    id: int
    name: str 
    active: bool
    
    class Config:
        from_attributes = True
    
class AppModel(BaseModel):
    id: int
    name: str 
    active: bool
    uuid: uuid.UUID 
    description: str
    roles: Optional[List[RoleModel]]
    
    class Config:
        from_attributes = True

class AppPostModel(BaseModel):
    name: str 
    active: bool
    description: str
    
    class Config:
        from_attributes = True

class AppDropModel(BaseModel):
    id: int
    name: str
     
   
    class Config:
        from_attributes = True  
       
class RoleModelAll(BaseModel):
    id: Optional[int]
    name: Optional[str]
    description: Optional[str]
    users: Optional[List[UserModel]] = []
    app: Optional[AppPostModel]    
    
    class Config:
        from_attributes = True
        
class RoleUserModelAll(BaseModel):
    id: Optional[int]
    roles: Optional[List[RoleModelMatrix]] = []

    class Config:
        from_attributes = True
        
class AddRole(BaseModel):
    role_id: int

    # class Config:
        #extra = "allow"
        
class RoleUserModel(BaseModel):
    id: Optional[int]
    email: Optional[EmailStr]
    roles: Optional[List[RoleModelMatrix]] = []

    class Config:
        from_attributes = True
        #extra = "allow"        


# #########################################################################

class EndPointsModel(BaseModel):
    name: str
    route_paths: str
    description: str 
    method: str 
    feature_id : Optional[int]
    
    class Config:
        from_attributes = True
        #extra = "allow"


class FeatureModel(BaseModel):
    name: str
    description: Optional[str]
    active: bool
    description: str
    role_id: int
    
    class Config:
        from_attributes = True
        #extra = "allow"

class FeatureModelAll(BaseModel):
    id: Optional[int]
    name: Optional[str]
    description: Optional[str]
    active: bool
    role_id: int
    end_points: Optional[List[EndPointsModel]] = []

    class Config:
        from_attributes = True
        #extra = "allow"
        
class AddFeature(BaseModel):
    feature_id: int

    # class Config:
        #extra = "allow"
        
# #########################################################################


class UserNameModel(BaseModel):
    name: str

    class Config:
        from_attributes = True
        #extra = "allow"

class UserLoader(BaseModel):
    name: List[UserNameModel]
    email: Optional[EmailStr]
    disabled: Optional[bool]
    roles: Optional[List[RoleModel]] = []
    is_active: bool
    is_authenticated: bool = False

    class Config:
        from_attributes = True
        #extra = "allow"

class UserModelLogin(BaseModel):
    id: Optional[int]
    uid: Optional[uuid.UUID]
    email: Optional[EmailStr]
    is_active: Optional[bool]
    roles: Optional[List[RoleModel]] = []

    # class Config:
        #extra = "allow"

class RolesUsersModel(BaseModel):
    user_id: int
    role_id: int
    
    # class Config:
        #extra = "allow"

class RouteResponseModel(BaseModel):
    id: int
    name: str
    route_path: str
    description: str
    roles:  Optional[List[RoleModel]] = []

    class Config:
        from_attributes = True
        #extra = "allow"


class RouteResponseDropDownModel(BaseModel):
    id: int
    name: Optional[str]
    route_path: Optional[str]
    description: Optional[str]

    class Config:
        from_attributes = True
        #extra = "allow"

        

class App(BaseModel):
    id : int
    name: str
    active: bool
    uuid: Optional[uuid.uuid4]
    roles: Optional[List[RoleModelMatrix]]
      
    @validator('uuid', pre=True, always=True)
    def set_id(cls, v):
        return v or uuid.uuid4()

    class Config:
        from_attributes = True
        #extra = "allow"
        