from typing import List, Optional, Union
#from app.core.security import get_password_hash
from app.models.app_model import User, FSNode
from app.repositories.fs_node_query import FSNodeRepository
from app.schemas.sch_user import UserCreate, UserUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import get_password_hash
from app.dtos.fs_node_dto import CreateNodeCmd, DeleteNodeCmd, CreateGrpCmd
from app.utils.fs_utilis import fsutilis
from app.exceptions.http_exceptions import DirHasChild, NodeNotExsits, PermissionDenied, PresignedUrlfail
from app.exceptions.http_exceptions import NotaDirectory, NotaOwner
from app.services.storage_service import StorageService
from fastapi import UploadFile
from fastapi.concurrency import run_in_threadpool
from enum import IntEnum
from pathlib import Path
from app.redis_code.queue.file_queue import file_queue

class FileStatus(IntEnum):
    UPLOADING= 0
    READY= 1
    FAILED= 2
class Perm(IntEnum):
    PERM_READ   = 4
    PERM_WRITE  = 2
    PERM_EXEC   = 1




class FSNodeService:    
    ACTION_PERM = {
        "read":   Perm.PERM_READ,
        "list":   Perm.PERM_READ  | Perm.PERM_EXEC, 
        "create": Perm.PERM_WRITE | Perm.PERM_EXEC,
        "delete": Perm.PERM_WRITE | Perm.PERM_EXEC,
        "move":   Perm.PERM_WRITE | Perm.PERM_EXEC,
        "enter":  Perm.PERM_EXEC,
    }
    def __init__(self, db: AsyncSession, node_repo: FSNodeRepository, storage):
        """Initialize with user repository"""
        self.db= db
        self.node_repo= node_repo
        self.storage= storage

    def chk_permission(self, node, userid, grp_id, req_perm):
        p= False
        if node.owner_id == userid:
            p= (node.owner_perm & req_perm) == req_perm
        elif node.group_id in grp_id:
            p= (node.group_perm & req_perm) == req_perm
        else:
            p= (node.other_perm & req_perm) == req_perm
        return p

    async def has_permission(self, nodeobj, userid, grpid, uaction):
        all_parent= await self.node_repo.get_all_parent(nodeobj.path)
        grp_id= await self.node_repo.get_all_grp_id(userid)
        print(f"ALL PARENT {all_parent}")

        p= False
        for pnode in all_parent:
            p= self.chk_permission(pnode, userid, grp_id, Perm.PERM_EXEC )
            if not p:
                break
        if p:
            req_perm= FSNodeService.ACTION_PERM[uaction]
            p= self.chk_permission(all_parent[-1], userid, grp_id, req_perm )
        return p



    
    def xhas_permission(self, nodeobj, userid, grpid, uaction):
        print(f"PERMISSION | {nodeobj.owner_id} | {userid} | {grpid}")
        # Permission	Meaning
        # r	List directory contents (ls)
        # x	Enter directory / access children
        # r + x	List + access files
        # w + x	Create / delete files
        # w only	❌ useless
        # r only	❌ can list names but can’t open files
        # x only	Can access known files but can’t list

        # if own:
        #     chk owner perm
        # if grpid :
        #     chk grp perm
        # else:
        #     chk other perm
        PERM_READ   = 4
        PERM_WRITE  = 2
        PERM_EXEC   = 1

        ACTION_PERM = {
            "read":   PERM_READ,
            "list":   PERM_READ | PERM_EXEC, 
            "create": PERM_WRITE | PERM_EXEC,
            "delete": PERM_WRITE | PERM_EXEC,
            "move":   PERM_WRITE | PERM_EXEC,
            "enter":  PERM_EXEC,
        }
        req_perm= ACTION_PERM[uaction]
        if nodeobj.owner_id == userid:
            p= (nodeobj.owner_perm & req_perm) == req_perm
        elif grpid:
            p= (nodeobj.group_perm & req_perm) == req_perm
        else:
            p= (nodeobj.other_perm & req_perm) == req_perm
        return p
    
    async def create_node(self, dirparam: CreateNodeCmd, file:UploadFile) -> Optional[FSNode]:
        # On parent node chk if there is write permission .
        # return self.node_repo.create_dir(dirparam)
        fid= fsutilis.generate_id() 
        print(f"FID : {fid}")
        repoparam= dict(dirparam)
        repoparam["id"]= fid
        print(repoparam)
        async with self.db.begin():
            parent= await self.node_repo.chk_parent(repoparam)
            user_grp_id= await self.node_repo.get_user_grp_id(repoparam["owner_id"])
            print(f"CHKPARENT {parent}")
            if parent is None or not parent.is_directory:
                raise NotaDirectory("Parent is not a directory", "NOT_DIRECTORY")

            if not await self.has_permission(parent, repoparam["owner_id"], user_grp_id, "create"):
                raise PermissionDenied("Permission to create is not allowed.", "PERMISSION_DENIED")
            res= await self.node_repo.insert_data(repoparam,  False)
            if not repoparam['is_directory']:
                try:
                    purl= self.storage.get_presigned_url(fid)
                except Exception as e:
                    print(f"EXCEPTION : {e}")
                    raise PresignedUrlfail()
            return {"purl":purl, "fid":str(fid)}

    async def xxcreate_node(self, dirparam: CreateNodeCmd, file:UploadFile) -> Optional[FSNode]:
        # On parent node chk if there is write permission .
        # return self.node_repo.create_dir(dirparam)
        fid= fsutilis.generate_id() 
        print(f"FID : {fid}")
        repoparam= dict(dirparam)
        repoparam["id"]= fid
        print(repoparam)
        async with self.db.begin():
            parent= await self.node_repo.chk_parent(repoparam)
            user_grp_id= await self.node_repo.get_user_grp_id(repoparam["owner_id"])
            print(f"CHKPARENT {parent}")
            if parent is None or not parent.is_directory:
                raise NotaDirectory("Parent is not a directory", "NOT_DIRECTORY")

            if not await self.has_permission(parent, repoparam["owner_id"], user_grp_id, "create"):
                raise PermissionDenied("Permission to create is not allowed.", "PERMISSION_DENIED")
            res= await self.node_repo.insert_data(repoparam,  False)
            if not repoparam['is_directory']:
                try:
                    print("R2 upload")
                    print(self.storage)
                    fres= await self.storage.put_object(fid, file)
                    print(fres)
                    res= await self.node_repo.chg_node_status(repoparam, 1)
                except Exception as e:
                    print(f"EXCEPTION : {e}")
                    res= await self.node_repo.chg_node_status(repoparam, 2)
            return res

    async def delete_node(self, dirparam: DeleteNodeCmd) -> Optional[FSNode]:
        repoparam= dict(dirparam)
        res=None
        async with self.db.begin():
            parent= await self.node_repo.chk_parent(repoparam)
            user_grp_id= await self.node_repo.get_user_grp_id(repoparam["owner_id"]) 
            if await self.node_repo.dir_has_child(repoparam):
                raise DirHasChild()
            elif not self.has_permission(parent, repoparam["owner_id"], user_grp_id, "delete"):
                raise PermissionDenied("Permission to create is not allowed.", "PERMISSION_DENIED")
            else:
                res= await self.node_repo.delete_node(repoparam)
                if res.rowcount == 0:
                    raise NodeNotExsits()
        return res
        
    async def delete_empty_node(self, dirparam: DeleteNodeCmd) -> Optional[FSNode]:
        repoparam= dict(dirparam)
        res= None
        async with self.db.begin():
            parent= await self.node_repo.chk_parent(repoparam)
            user_grp_id= await self.node_repo.get_user_grp_id(repoparam["owner_id"]) 
            if await self.node_repo.dir_has_child(repoparam):
                raise DirHasChild()
            elif not self.has_permission(parent, repoparam["owner_id"], user_grp_id, "delete"):
                raise PermissionDenied("Permission to delete is not allowed.", "PERMISSION_DENIED")
            else:
                res= await self.node_repo.delete_empty_node(repoparam, False)
                print(f"RES SERV : {res}")
                if res.rowcount == 0:
                    raise NodeNotExsits()
        return res

    async def delete_node_forcefully(self, dirparam: DeleteNodeCmd)-> Optional[FSNode]:
        repoparam= dict(dirparam)
        async with self.db.begin():
            parent= await self.node_repo.chk_parent(repoparam)
            nodeobj= await self.node_repo.get_node(repoparam)
            user_grp_id= await self.node_repo.get_user_grp_id(repoparam["owner_id"]) 
            if not self.has_permission(parent, repoparam["owner_id"], user_grp_id, "delete"):
                raise PermissionDenied("Permission to delete is not allowed.", "PERMISSION_DENIED")
            elif nodeobj is None:
                raise  NodeNotExsits("Node does not exists", "NODE_NOT_EXISTS")
            print(nodeobj)
            repoparam["parent_path"]= nodeobj.FSNode.path
            res= await self.node_repo.delete_node(repoparam, False)
            # if res.rowcount == 0:
            #     raise NodeNotExsits()
        return res
    
    async def move_node(self, nodeparam: DeleteNodeCmd)-> Optional[FSNode]:
        repoparam= dict(nodeparam)
        async with self.db.begin():
            parent= await self.node_repo.chk_parent(repoparam)
            user_grp_id= await self.node_repo.get_user_grp_id(repoparam["owner_id"])
            print(f"CHKPARENT {parent}")
            if parent is None or not parent.is_directory:
                raise NotaDirectory("Parent is not a directory", "NOT_DIRECTORY")
            elif not self.has_permission(parent, repoparam["owner_id"], user_grp_id, "move"):
                raise PermissionDenied("Permission to move is not allowed.", "PERMISSION_DENIED")
            res= await self.node_repo.move_node(repoparam, False)
            if res.rowcount == 0:
                raise NodeNotExsits()
        return res

    async def chg_node_perm(self, param):
        tperm= (param["perm"] // 100 , (param["perm"] // 10) % 10, param["perm"] % 10 )
        param["perm"]= tperm
        isown= await self.node_repo.chk_owner(param["nid"], param["owner_id"])
        if isown is None:
            raise NotaOwner("User is not a owner , cant changed permission", "NOT_OWNER")
        res= await self.node_repo.chg_node_perm(param)
        return res
        


    async def get_file(self, param) -> dict:
        res=None
        async with self.db.begin():
            nodeobj= await self.node_repo.get_node(param)
            if not self.has_permission(nodeobj[0], param["user_id"], nodeobj[0].group_id, "read"):
                raise PermissionDenied("No  Permission to read file ", "PERMISSION_DENIED")
            else:
                res= await self.storage.get_object(param["id"])
        return res


    async def upload_file_complete(self, param)->dict:
        res= None
        print(param)
        res= await self.node_repo.chg_node_status(param["nid"], "UPLOADED")
        await file_queue.publish_file_uploaded(
            file_id=str(param["nid"]),
            bucket_name="webfsbucket",
            user_id=param["user_id"],
            mime_type=param["content_type"]
        )

        print(f"PARAM : {param}")
        return {"message": "File queued"}




    