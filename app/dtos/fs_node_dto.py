from pydantic import BaseModel

class CreateNodeCmd(BaseModel):
    name: str
    owner_id: int
    parent_id: int
    path:str|None
    is_directory:bool

class NodeBaseCmd(BaseModel):
    id: int
    parent_id: int
    owner_id: int
class DeleteNodeCmd(NodeBaseCmd):
    is_directory: bool

class MoveNodeCmd(NodeBaseCmd):
    pass