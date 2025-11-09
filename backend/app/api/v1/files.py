from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ..deps import get_current_user
from ...services.storage import SignedUpload, storage_client

router = APIRouter()


class SignUploadRequest(BaseModel):
    filename: str
    contentType: str


@router.post("/sign-upload", response_model=SignedUpload)
def sign_upload(payload: SignUploadRequest, user=Depends(get_current_user)) -> SignedUpload:  # noqa: B008
    return storage_client.sign_upload_url(payload.filename, payload.contentType)
