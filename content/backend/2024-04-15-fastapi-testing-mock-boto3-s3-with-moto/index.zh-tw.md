---
title: "FastAPI: 使用 Moto 模擬 S3"
summary: "FastAPI 測試: 使用 Moto 模擬 AWS S3 Boto3"
description: "FastAPI: 在整合測試中使用 Moto 模擬 AWS S3 和 Boto3 SDK"
date: 2024-05-28T15:47:01+08:00
slug: "k8s-fastapi-mock-boto3-s3-with-moto"
tags: ["blog","zh-tw","AWS","backend","testing","FastAPI"]
# series: ["Documentation"]
# series_order: 9
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
draft: false
---

## 介紹

{{< alert "circle-info" >}}
在 `FastAPI` 框架中使用 `moto` 模擬 `boto3`。
{{< /alert >}}

- `boto3` : AWS 的 Python SDK
- `moto` : 用於模擬 AWS 的 Python SDK 的 Package
    - **server mode** 用於模擬 AWS 服務
    - `mock_aws` decorator 用於模擬 AWS 操作
- `FastAPI` 
    - 提供 `TestClient` : [參考](https://fastapi.tiangolo.com/tutorial/testing/)
        - 與 `pytest` 一起進行測試

## 應用範例

在 FastAPI 中，常見模式是使用 `Depends` 進行依賴注入 
> 順便說一下，`Depends` 可以是遞迴的
> 這表示，`A Depends` 可以依賴於 `B Depends` 和 `C Depends`

範例:
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
        # sqlalchemy `Session` 實例
        db: Session = Depends(get_db),
        # `boto3.client('s3')` 實例
        s3_client=Depends(get_s3_client),
):
    # 使用 依賴注入 `FileService` 實例
    return FileService(
        db,
        s3_client,
)
```

## 使用 Database 範例的 `dependency_overrides`

在測試時，我們可能想要覆蓋 `get_db` 依賴 
使用我們的測試資料庫，如內存中的 `sqlite`。

幸運的是，`FastAPI` 提供了 [FastAPI: Override Testing Dependencies ](https://fastapi.tiangolo.com/advanced/testing-dependencies/) 的工具！

繼續前面的程式。
```python
def override_get_db():
    try:
        # 使用 mock DB 的 sqlalchemy `sessionmaker`
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# app : 來自主應用程式的原始 FastAPI 實例
app.dependency_overrides[get_db] = override_get_db
testClient = TestClient(app)
```

## 設置 `moto`

`moto` : 一個模擬基於 AWS 基礎設施測試的 package 。

### Moto: Server Mode

[Moto: Server Mode](https://docs.getmoto.org/en/latest/docs/server_mode.html#run-using-docker)

`Moto` 也提供獨立的 Server Mode。（用於模擬 AWS 服務）
我建議使用 `Docker` 設置 `moto-server`

```bash 
docker run --rm -p 5000:5000 --name moto motoserver/moto:latest
```

或使用 `Docker-Compose` 如果有其他基礎設施依賴。

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

**儀表板**
Moto 伺服器提供一個儀表板，用於監控當前服務狀態。
```
http://localhost:5000/moto-api/
```

### 推薦用法與範例（來自官方文檔）

[推薦用法](https://docs.getmoto.org/en/latest/docs/getting_started.html#recommended-usage)

確保在測試範圍內設置虛擬環境。
```python 
os.environ["AWS_ACCESS_KEY_ID"] = "testing"
os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
os.environ["AWS_SECURITY_TOKEN"] = "testing"
os.environ["AWS_SESSION_TOKEN"] = "testing"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
os.environ["MOTO_S3_CUSTOM_ENDPOINTS"] = "http://127.0.0.1:3000"
```

使用 `Pytest` 的範例

```python 
@pytest.fixture(scope="function")
def aws_credentials():
    """Moto 的模擬 AWS 憑證。"""
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

## 使用 `dependency_overrides` 覆蓋 `s3_client` 依賴

使用 `moto` 和 `dependency_overrides` 的基本用法
我們可以用 `moto` 模擬 S3 客戶端 override `get_s3_client` 依賴~

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
    
# app : 來自主應用程式的原始 FastAPI 實例
app.dependency_overrides[get_s3_client] = override_get_s3_client
testClient = TestClient(app)
```

並且，**不要忘記為 pytest 函數添加 `mock_aws`**

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