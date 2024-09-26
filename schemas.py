from pydantic import BaseModel
#-----------V1----------------
class Task(BaseModel):
    title: str
    description: str
    status: str
    
class TaskWithID(Task):
    id: int
#------------------------------



#-----------V2----------------
#ADDED IN ORDER TO UPGRADE THE API VERSION TO VERSION 2

class Taskv2(BaseModel):
    title: str
    description: str
    status: str
    priority: str | None = "lower"

class taskv2WithID(Taskv2):
    id: int
    
#-----------------------------



#-------------USERS----------------

class User(BaseModel):
    username: str

class UserInDB(User):
    hashed_password: str

#----------------------------------