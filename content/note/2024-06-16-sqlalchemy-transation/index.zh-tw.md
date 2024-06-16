---
title: "在 SqlAlchemy 使用 Transaction"
summary: "如何在 SqlAlchemy 中使用 Transaction"
description: "如何在 SqlAlchemy 中使用 Transaction？ 提供在 FastAPI 框架中使用 SqlAlchemy 的 Transaction 範例。"
date: 2024-06-16T22:12:18+08:00
slug: "sqlalchemy-transaction"
tags: ["blog","zh-tw","SqlAlchemy","backend","python"]
# series: ["Documentation"]
# series_order: 9
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
draft: false
---

# 在 `SqlAlchemy` 使用 Transaction

Transaction 是資料庫操作中非常重要的一環，透過 Transaction 可以確保資料庫的一致性
而 SqlAlchemy 是 Python 中最常見的 ORM 框架
那要如何在 SqlAlchemy 中使用 Transaction 呢？

## Transaction 的特性

在 Transaction 中
- 所有的操作要麼**全部成功**，要麼**全部失敗**
  - 也就是說 Transaction 中的操作是 Atomic 的 (原子性的)


Transaction 通常包含以下幾個步驟
- 開始 Transaction
- 執行操作
  - 可能會在這個 transaction 中執行多個操作，如：
    - 新增多一個 object instance 又修改另一個 object instance ...
- 結束 Transaction
  - 如果操作成功，則 `Commit` Transaction
  - 如果操作失敗，則 `Rollback` Transaction


## 在 SqlAlchemy 中使用 Transaction

在 SqlAlchemy 中，Transaction 是透過 `Session` 來實現的
以下是一個簡單的 Transaction 範例

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# 創建 engine
engine = create_engine("sqlite:///example.db")
# 創建 session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Get SQLAlchemy database session
    """
    database:Session = SessionLocal()
    try:
        yield database
    finally:
        database.close()

# service 層
def create_user(db, user):
    """
    Create user
    """

    # 其他商業邏輯
    # user.name = user.name.capitalize() ...
    # user.age = random.randint(0, 100) ...

    try:  
      db.add(user)
      db.commit()
      db.refresh(user)
      return user
    except Exception as e:
      db.rollback()
      raise e

# controller 層
def create_user_controller(user):
    """
    Create user controller
    """
    db = next(get_db())
    return create_user(db, user)
```

使用 `sessionmaker` 創建的是 `Session` 的 module-level factory 
並在 `get_db` 中使用 `SessionLocal()` 來取得 `Session` instance 並在 `finally` 中關閉 `Session`

在 controller 層
只要負責將 `Session` instance 注入 service 層的 `create_user` 

這樣在 service 層
所有的操作就已經在 Transaction 中了
如果在 `create_user` 中的任何一個操作失敗，則整個 Transaction 會 `Rollback`，並且不會對資料庫做任何更動


## 在 FastAPI 中使用 SqlAlchemy Transaction

在 FastAPI 中使用 SqlAlchemy Transaction 也是非常簡單的
同時提供了 `Depends` 來實現 `Dependency Injection`
可以將 Generator Function 作為 `Depends` 的參數，並在 `Depends` 中取得在 `get_db` 中 `yield` 的 `Session` instance

```python
from typing import List
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

...

def get_db():
    """
    Get SQLAlchemy database session
    """
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()

@router.post("/users", response_model=List[schemas.User])
def create_users(user_1: schemas.UserCreate, user_2: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create two users
    """
    try:
        user_1 = crud.create_user(db=db, user=user_1)
        user_2 = crud.create_user(db=db, user=user_2)
        db.commit()
        return [user_1, user_2]
    except:
        db.rollback()
        raise HTTPException(status_code=400, detail="Duplicated user")
```