import os
from typing import TypeVar, Generator

import botocore
import pytest
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer

from redbox.models import File, Settings

T = TypeVar("T")

YieldFixture = Generator[T, None, None]

env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env.test")


env = Settings(
    _env_file=env_path,
    object_store="minio",
    minio_host="localhost",
    elastic_host="localhost",
    embedding_model="paraphrase-albert-small-v2",
)


@pytest.fixture
def s3_client():
    yield env.s3_client()


@pytest.fixture
def es_client() -> YieldFixture[Elasticsearch]:
    yield env.elasticsearch_client()


@pytest.fixture
def embedding_model() -> YieldFixture[SentenceTransformer]:
    yield SentenceTransformer(env.embedding_model)


@pytest.fixture
def file_pdf_path() -> YieldFixture[str]:
    path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..",
        "..",
        "tests",
        "data",
        "pdf",
        "Cabinet Office - Wikipedia.pdf",
    )
    yield path


@pytest.fixture
def file(s3_client, file_pdf_path):
    """
    TODO: this is a cut and paste of core_api:create_upload_file
    When we come to test core_api we should think about
    the relationship between core_api and the ingest app
    """
    file_name = os.path.basename(file_pdf_path)
    file_type = file_name.split(".")[-1]
    body = open(file_pdf_path, "rb").read()

    try:
        s3_client.put_object(
            Bucket=env.bucket_name,
            Body=body,
            Key=file_name,
            Tagging=f"file_type={file_type}",
        )
    except Exception as e:
        raise Exception(f"bucket: {env.bucket_name}, original exception {e}")


    authenticated_s3_url = s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": env.bucket_name, "Key": file_name},
        ExpiresIn=3600,
    )

    # Strip off the query string (we don't need the keys)
    simple_s3_url = authenticated_s3_url.split("?")[0]
    file_record = File(
        name=file_name,
        path=simple_s3_url,
        type=file_type,
        creator_user_uuid="dev",
        storage_kind=env.object_store,
    )

    yield file_record
