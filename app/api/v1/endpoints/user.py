from fastapi import APIRouter, Depends, status, Body, File, UploadFile
from app.dtos.custom_response import CustomResponse
from app.dtos.fs_node_dto import CreateNodeCmd, DeleteNodeCmd, MoveNodeCmd, CreateGrpCmd
from app.schemas.sch_user import UserCreate, CreateNode, NodeContext, ChgPermission, CreateGrp,  CompleteUpload
from app.dependencies.dp_services import get_node_service, get_group_service
from app.dependencies.dp_common import verify_jwt, get_create_node_form
from app.utils.response import create_response
from app.exceptions.http_exceptions import InvalidNodeName

router= APIRouter()
@router.get("/testuser")
def testuser():
    print("WORKING USER")
    return {}

async def create_node(file, nodeparam, payload, dbcon, is_dir):
    if not nodeparam and not nodeparam.nodename.strip():
        raise InvalidNodeName(detail= "", error_code= "")
    print(payload)
    nodepath= f"/{nodeparam.ppath}" if nodeparam.ppath is None else f"{nodeparam.ppath}/{nodeparam.nodename}"
    nodestatus= "PROCESSED" if is_dir else "UPLOADING"
    print(nodeparam)
    param= CreateNodeCmd(
        name= nodeparam.nodename,
        owner_id= payload['userid'],
        parent_id= nodeparam.pid,
        path= nodepath,
        is_directory= is_dir,
        status= nodestatus
        )
    print("BEFORE SERIVCE")
    res= await dbcon.create_node(param, file)
    print(res)
    if not is_dir:
        resdata= res
    else : resdata= {}
    return create_response(resdata, message="FOLDER CREATED", status_code=status.HTTP_200_OK)

async def delete_node(nodeparam, payload, dbcon, is_recursive):
    param= DeleteNodeCmd(
        id= nodeparam.id,
        owner_id= payload['userid'],
        parent_id= nodeparam.pid,
        )
    res= None
    print("BEFORE SERIVCE")
    if is_recursive:
        res= await dbcon.delete_node_forcefully(param)
    else:
        res= await dbcon.delete_empty_node(param)
    print(res)
    return create_response(data= {}, message="NODE DELETE", status_code=status.HTTP_200_OK)

# @router.post("/mkdir", response_model=CustomResponse[UserCreate], summary= "Create Folder", description= "Create Folder") 
@router.post("/mkdir",  summary= "Create Folder", description= "Create Folder") 
async def create_folder(nodeparam: CreateNode, payload= Depends(verify_jwt), dbcon= Depends(get_node_service)):
    return await create_node(None, nodeparam, payload, dbcon, True)

@router.post("/mkfile",  summary= "Create File", description= "Create File") 
async def create_file(file:UploadFile= File(...), nodeparam: CreateNode= Depends(get_create_node_form), payload= Depends(verify_jwt), dbcon= Depends(get_node_service)):
    print("MKFILE")
    return await create_node(file, nodeparam, payload, dbcon, False)

@router.post("/rmdir/r",  summary= "Delete Folder recursively", description= "Delete Folder") 
async def delete_file(nodeparam: NodeContext, payload= Depends(verify_jwt), dbcon= Depends(get_node_service)):
    print("Del Folder recursively")
    return await delete_node(nodeparam, payload, dbcon, True)

@router.post("/rmdir",  summary= "Delete Folder", description= "Delete Folder") 
async def delete_file(nodeparam: NodeContext, payload= Depends(verify_jwt), dbcon= Depends(get_node_service)):
    print("Del Folder")
    return await delete_node(nodeparam, payload, dbcon, False)

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

@router.post("/creategroup",  summary= "Create Group", description= "Create Group")
async def create_group(nodeparam: CreateGrp, payload= Depends(verify_jwt), dbcon= Depends(get_group_service)):
    param= {
        "grpname": nodeparam.grpname,
        "grpuserids": nodeparam.grpuserids,
        "grpdesc": nodeparam.grpdesc,
        "userid": payload["userid"]
    }
    gdto= CreateGrpCmd(**param)
    res= await dbcon.create_grp(gdto)
    return create_response(data= {}, message="Create Group", status_code=status.HTTP_200_OK)

@router.get("/getfile/{node_id}",  summary= "Get file content", description= "Get file contnet")
async def get_file(node_id:int, payload= Depends(verify_jwt), dbcon= Depends(get_node_service)):
    param= {"id": node_id, "user_id": payload["userid"]}
    res= await dbcon.get_file(param)
    return create_response(data= res, message="Create Group", status_code=status.HTTP_200_OK)


@router.post("/complete",  summary= "Get file content", description= "Get file contnet")
async def file_upload_complete(nodeparam: CompleteUpload ,payload= Depends(verify_jwt), dbcon= Depends(get_node_service)):
    param= { 
        "nid": nodeparam.file_id,
        "content_type": nodeparam.content_type,
        "user_id": payload["userid"]
        }
    res= await dbcon.upload_file_complete(param)
    return create_response(data= res, message="File uploaded", status_code=status.HTTP_200_OK)