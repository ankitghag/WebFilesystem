from fastapi import APIRouter, Depends, status, Body
from app.dtos.custom_response import CustomResponse
from app.dtos.fs_node_dto import CreateNodeCmd, DeleteNodeCmd, MoveNodeCmd
from app.schemas.sch_user import UserCreate, CreateNode, NodeContext, ChgPermission
from app.dependencies.dp_services import get_node_service
from app.dependencies.dp_common import verify_jwt
from app.utils.response import create_response
from app.exceptions.http_exceptions import InvalidNodeName

router= APIRouter()
@router.get("/testuser")
def testuser():
    print("WORKING USER")
    return {}

async def create_node(nodeparam, payload, dbcon, is_dir):
    if not nodeparam and not nodeparam.nodename.strip():
        raise InvalidNodeName(detail= "", error_code= "")
    print(payload)
    nodepath= f"/{nodeparam.ppath}" if nodeparam.ppath is None else f"{nodeparam.ppath}/{nodeparam.nodename}"
    param= CreateNodeCmd(
        name= nodeparam.nodename,
        owner_id= payload['userid'],
        parent_id= nodeparam.pid,
        path= nodepath,
        is_directory= is_dir
        )
    print("BEFORE SERIVCE")
    res= await dbcon.create_node(param)
    print(res)
    return create_response(data= {}, message="FOLDER CREATED", status_code=status.HTTP_200_OK)

async def delete_node(nodeparam, payload, dbcon, is_dir):
    param= DeleteNodeCmd(
        id= nodeparam.id,
        owner_id= payload['userid'],
        parent_id= nodeparam.pid,
        is_directory= is_dir
        )
    res= None
    print("BEFORE SERIVCE")
    if is_dir:
        res= await dbcon.delete_empty_node(param)
    else:
        res= await dbcon.delete_node_forcefully(param)
    print(res)
    return create_response(data= {}, message="NODE DELETE", status_code=status.HTTP_200_OK)

# @router.post("/mkdir", response_model=CustomResponse[UserCreate], summary= "Create Folder", description= "Create Folder") 
@router.post("/mkdir",  summary= "Create Folder", description= "Create Folder") 
async def create_folder(nodeparam: CreateNode, payload= Depends(verify_jwt), dbcon= Depends(get_node_service)):
    return await create_node(nodeparam, payload, dbcon, True)

@router.post("/mkfile",  summary= "Create File", description= "Create File") 
async def create_file(nodeparam: CreateNode, payload= Depends(verify_jwt), dbcon= Depends(get_node_service)):
    print("MKFILE")
    return await create_node(nodeparam, payload, dbcon, False)

@router.post("/rmdir",  summary= "Delete Folder", description= "Delete Folder") 
async def delete_file(nodeparam: NodeContext, payload= Depends(verify_jwt), dbcon= Depends(get_node_service)):
    print("Del Folder")
    return await delete_node(nodeparam, payload, dbcon, True)

@router.post("/rmfile",  summary= "Delete File", description= "Delete File") 
async def delete_file(nodeparam: NodeContext, payload= Depends(verify_jwt), dbcon= Depends(get_node_service)):
    print("Del File")
    return await delete_node(nodeparam, payload, dbcon, False)
 

@router.post("/movenode",  summary= "Move Node", description= "Move Node") 
async def move_node(nodeparam: NodeContext, payload= Depends(verify_jwt), dbcon= Depends(get_node_service)):
    print("Move Node")
    param= MoveNodeCmd(
        id= nodeparam.id,
        owner_id= payload['userid'],
        parent_id= nodeparam.pid
        )
    res= await dbcon.move_node(param) 
    return create_response(data= {}, message="NODE DELETE", status_code=status.HTTP_200_OK)



@router.post("/node/{node_id}/chmod",  summary= "Change permission", description= "Change permission") 
async def change_node_permission(nodeparam: ChgPermission, payload= Depends(verify_jwt), dbcon= Depends(get_node_service)):
    param= {
        "nid": nodeparam.nid,
        "perm": nodeparam.perm,
        "owner_id": payload["userid"]
        
    }
    res= await dbcon.chg_node_perm(param)
    return create_response(data= {}, message="Permission changed", status_code=status.HTTP_200_OK)