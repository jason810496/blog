---
title: "k8s: Extract ConfigMap or Secret to .env file"
subtitle: "Kubernetes cheat sheet: ConfigMap/Secret to .env format"
date:   2024-05-06 16:00:00 +0800

tag: [notes]

thumbnail-img: "https://raw.githubusercontent.com/jason810496/blog/main/_images/2024-05-06-k8s-extract-configmap-or-secret-to-env-file-thumbnail.jpeg" #1:1 (450:450)

cover-img: "https://raw.githubusercontent.com/jason810496/blog/main/_images/2024-05-06-k8s-extract-configmap-or-secret-to-env-file-banner.jpeg"

comments: true

# ======= Other parameters ========
layout: post
readtime: true

# test local : bundle exec jekyll serve
---

# k8s: Extract configmap/secret to .env file

* [test local : bundle exec jekyll serve](#test-local--bundle-exec-jekyll-serve)
* [FastAPI Testing: Mock boto3 S3 with moto](#fastapi-testing-mock-boto3-s3-with-moto)
    * [Intro](#intro)
    * [Application Example](#application-example)
    * [setup moto](#setup-moto)
        * [Moto: Server Mode](#moto-server-mode)
        * [Recommended Usage &amp; Example(from official docs)](#recommended-usage--examplefrom-official-docs)
    * [override s3_client using dependency_overrides](#override-s3_client-using-dependency_overrides)

## Intro 

{: .box-warning}
Mock `boto3` with `moto` in `FastAPI` framework.


- `boto3` : AWS python SDK
- `moto` : Mock package for AWS python SDK
    - **server mode** for Mocking AWS services
    - `mock_aws` decorator for AWS mocked out
- `FastAPI` 
    - provide `TestClient` : [ref](https://fastapi.tiangolo.com/tutorial/testing/)
        - for clean testing with `pytest`

## Application Example

In FastAPI , the common pattern is using `Depends` for dependcies-injection 
> By the way , `Depends` can be recursive 
> Which means , `A Depends` can depends on `B Depends` and `C Depends`

Eg:
`endpoint.py`
```python 
from fastapi import Depends

@FileV1Router.post(
    path="/files",
    response_model=v1_schemas.FilePresignedUrlResponse,
)
async def create_file_endpoint(
    file: v1_schemas.FileCreate,
    file_service: FileService = Depends(get_file_service),
    user_id: str = Depends(get_current_user),
):
    file_response = file_service.generate_presigned_upload_url(file, user_id)
    return file_response
```
`deps.py`
```python 
def get_file_service(
        # sqlalchemy `Session` instance
        db: Session = Depends(get_db),
        # `boto3.client('s3')` instance
        s3_client=Depends(get_s3_client),
):
    # inject dependencies to `FileService` class
    return FileService(
        db,
        s3_client,
)
```

## `dependency_overrides` with Database example

However, when it comes to testing .
We might want to overrider `get_db` dependcies with our Testing Database such as `sqlite` in memeory.


Luckly, `FastAPI` provide `[FastAPI
Testing Dependencies with Overrides](https://fastapi.tiangolo.com/advanced/testing-dependencies/)` utilites for our use cases!

Continue from previous application.
```python
def override_get_db():
    try:
        # sqlalchemy `sessionmaker` with mock DB
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# app : original FastAPI instance from main application
app.dependency_overrides[get_db] = override_get_db
testClient = TestClient(app)
```

## setup `moto`

`moto` : A library that allows you to easily mock out tests based on AWS infrastructure.



### Moto: Server Mode

[Moto: Server Mode](https://docs.getmoto.org/en/latest/docs/server_mode.html#run-using-docker)

`Moto` also provide stand-alone server mode. ( for mocking AWS services )
I recommend using `Docker` to setup `moto-server`

```bash 
docker run --rm -p 5000:5000 --name moto motoserver/moto:latest
```

Or using `Docker-compose` If having other infra dependencies.

```yaml 
version: '3.7'

services:
 moto:
    image: motoserver/moto:4.1.13
    ports:
      - "5000:5000"
    environment:
      - MOTO_PORT=5000
```
```bash 
docker compose up moto -d
```

**Dashboard**
Moto server provide a dashboard for monitoring current state of service.
```
http://localhost:5000/moto-api/
```

### Recommended Usage & Example(from official docs)

[Recommended Usage](https://docs.getmoto.org/en/latest/docs/getting_started.html#recommended-usage)

Ensure dummy env setup in your test scope.
```python 
os.environ["AWS_ACCESS_KEY_ID"] = "testing"
os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
os.environ["AWS_SECURITY_TOKEN"] = "testing"
os.environ["AWS_SESSION_TOKEN"] = "testing"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
os.environ["MOTO_S3_CUSTOM_ENDPOINTS"] = "http://127.0.0.1:3000"
```

Example useage with `Pytest`

```python 
@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

@pytest.fixture(scope="function")
def aws(aws_credentials):
    with mock_aws():
        yield boto3.client("s3", region_name="us-east-1")

@pytest.fixture
def create_bucket1(aws):
    boto3.client("s3").create_bucket(Bucket="b1")

@pytest.fixture
def create_bucket2(aws):
    boto3.client("s3").create_bucket(Bucket="b2")

def test_s3_directly(aws):
    s3.create_bucket(Bucket="somebucket")

    result = s3.list_buckets()
    assert len(result["Buckets"]) == 1

def test_bucket_creation(create_bucket1, create_bucket2):
    buckets = boto3.client("s3").list_buckets()["Buckets"]
    assert len(result["Buckets"]) == 2
```

## override `s3_client` using `dependency_overrides`

With base usage of `moto` and `dependency_overrides`
We could override `get_s3_client` dependency with `moto` mock client ~

```python 

def override_get_s3_client():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
    os.environ["MOTO_S3_CUSTOM_ENDPOINTS"] = "http://127.0.0.1:3000"

    try:
        with mock_aws():
            conn = boto3.resource("s3")
            conn.create_bucket(Bucket=file_settings.USER_BUCKET_NAME)
            s3_client = boto3.client(
                "s3", region_name="us-east-1", endpoint_url="http://127.0.0.1:3000"
            )
            yield s3_client
    finally:
        pass
    
# app : original FastAPI instance from main application
app.dependency_overrides[get_s3_client] = override_get_s3_client
testClient = TestClient(app)
```

BTW, **don't forget to add `mock_aws`** for pytest function.

```python 
from moto import mock_aws
from test.client import testClient

@mock_aws
def test_create_file(test_user_setup_teardown):
    valid_user_data, response = test_user_setup_teardown
    response = testClient.post(
        "/files",
        headers={
            "Authorization": "{token_type} {token}".format(
                token_type=response.json()["token_type"],
                token=response.json()["access_token"],
            )
        },
        json={"filename": "test-file", "description": "This is a test file"},
    )
    # ...
```