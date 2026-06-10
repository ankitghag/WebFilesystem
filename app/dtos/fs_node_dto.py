from pydantic import BaseModel
from typing import List

class CreateNodeCmd(BaseModel):
    name: str
    owner_id: int
    parent_id: int
    path:str|None
    is_directory:bool
    status: str

class NodeBaseCmd(BaseModel):
    id: int
    parent_id: int
    owner_id: int
class DeleteNodeCmd(NodeBaseCmd):
    pass

class MoveNodeCmd(NodeBaseCmd):
    pass

class CreateGrpCmd(BaseModel):
    grpname: str
    grpuserids: List[int]
    grpdesc: str
    userid: int