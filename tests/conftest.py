import os

import boto3
from fastapi.testclient import TestClient
from moto import mock_aws
from pytest import fixture

from main import app
from routes import TRANSCRIPTION_BUCKET


@fixture(scope="function", autouse=True)
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-central-1"


@fixture(scope="function")
def s3(aws_credentials):
    with mock_aws():
        yield boto3.client("s3")


@fixture(scope="function")
def create_bucket(s3):
    s3.create_bucket(Bucket=TRANSCRIPTION_BUCKET, CreateBucketConfiguration={
        'LocationConstraint': 'eu-central-1'
    },)


@fixture
def client():
    with TestClient(app) as client:
        yield client
