from fastapi import APIRouter, Depends

from app.db.sql import write_and_commit
from app.models import ScrapRequest
from app.schemas.scrap_request import ScrapRequestCreate, ScrapRequestData
from app.utils.auth import authenticate_user

router = APIRouter()


@router.post("/scrap_requests/", dependencies=[Depends(authenticate_user)], response_model=ScrapRequestData)
def create_scrap_request(scrap_request: ScrapRequestCreate):
    db_request = ScrapRequest(**scrap_request.dict())
    return write_and_commit(db_request)


@router.get('/scrap_requests/get')
def get_scrap_request():
    from app.services.scrapping_app import ScrappingApp
    ScrappingApp().process(request_id=1)
    return "S"