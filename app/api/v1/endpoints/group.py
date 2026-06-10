from fastapi import APIRouter, Depends, status, Body, File, UploadFile
from app.dtos.custom_response import CustomResponse
from app.dtos.fs_node_dto import CreateNodeCmd, DeleteNodeCmd, MoveNodeCmd
from app.schemas.sch_user import UserCreate, CreateNode, NodeContext, ChgPermission, CreateGrp
from app.dependencies.dp_services import get_node_service
from app.dependencies.dp_common import verify_jwt, get_create_node_form
from app.utils.response import create_response
from app.exceptions.http_exceptions import InvalidNodeName

router= APIRouter()


@router.post("/node/{node_id}/creategroup",  summary= "Change permission", description= "Change permission")
async def create_group(node_id:int, nodeparam: CreateGrp, payload= Depends(verify_jwt), dbcon= Depends(get_node_service)):
    param= {
        "grpname": nodeparam.grpname,
        "grpuserids": nodeparam.grpuserids,
        "grpdesc": nodeparam.grpdesc,
        "userid": payload["userid"]
    }
    res= await dbcon.create_grp(param)
    return create_response(data= {}, message="Create Group", status_code=status.HTTP_200_OK)