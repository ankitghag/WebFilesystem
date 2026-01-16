from typing import List, Optional, Union
#from app.core.security import get_password_hash
from app.models.app_model import User, FSNode
from app.repositories.fs_node_query import FSNodeRepository
from app.schemas.sch_user import UserCreate, UserUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import get_password_hash
from app.dtos.fs_node_dto import CreateNodeCmd, DeleteNodeCmd
from app.utils.fs_utilis import fsutilis
from app.exceptions.http_exceptions import DirHasChild, NodeNotExsits, PermissionDenied
from app.exceptions.http_exceptions import NotaDirectory, NotaOwner

class FSNodeService:    
    def __init__(self, db: AsyncSession, node_repo: FSNodeRepository):
        """Initialize with user repository"""
        self.db = db
        self.node_repo = node_repo
    def has_permission(self, nodeobj, userid, grpid, uaction):
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
    
    async def create_node(self, dirparam: CreateNodeCmd) -> Optional[FSNode]:
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

            if not self.has_permission(parent, repoparam["owner_id"], user_grp_id, "create"):
                raise PermissionDenied("Permission to create is not allowed.", "PERMISSION_DENIED")
            return await self.node_repo.insert_data(repoparam, False)

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
                raise PermissionDenied("Permission to create is not allowed.", "PERMISSION_DENIED")
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
            user_grp_id= await self.node_repo.get_user_grp_id(repoparam["owner_id"]) 
            if not self.has_permission(parent, repoparam["owner_id"], user_grp_id, "delete"):
                raise PermissionDenied("Permission to create is not allowed.", "PERMISSION_DENIED")
            res= await self.node_repo.delete_node(repoparam, False)
            if res.rowcount == 0:
                raise NodeNotExsits()
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
        isown= await self.node_repo.chk_owner(param)
        if isown is None:
            raise NotaOwner("User is not a owner , cant changed permission", "NOT_OWNER")
        res= await self.node_repo.chg_node_perm(param)
        return res



    