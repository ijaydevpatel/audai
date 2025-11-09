from typing import Protocol

import boto3
from pydantic import BaseModel

from ..core.config import settings


class SignedUpload(BaseModel):
    url: str
    objectKey: str


class StorageClient(Protocol):
    def sign_upload_url(self, filename: str, content_type: str) -> SignedUpload: ...


class S3StorageClient:
    def __init__(self) -> None:
        self._client = boto3.client("s3", region_name=settings.s3_region)

    def sign_upload_url(self, filename: str, content_type: str) -> SignedUpload:
        object_key = f"uploads/{filename}"
        url = self._client.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": settings.s3_bucket,
                "Key": object_key,
                "ContentType": content_type,
            },
            ExpiresIn=900,
        )
        return SignedUpload(url=url, objectKey=object_key)


storage_client: StorageClient = S3StorageClient()
