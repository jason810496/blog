---
title: "How to use Transaction in SqlAlchemy"
summary: "How to transaction in SqlAlchemy"
description: "How to transaction in SqlAlchemy? Provide transaction example in SqlAlchemy with FastAPI Framework."
date: 2024-06-16T22:12:17+08:00
slug: "sqlalchemy-transaction"
tags: ["blog","en","SqlAlchemy","backend","python"]
# series: ["Documentation"]
# series_order: 9
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
draft: false
---

# How to use Transaction in `SqlAlchemy`

Transaction is an essential part of database operations, and it ensures the consistency of the database. SqlAlchemy is the most common ORM framework in Python. So how to use Transaction in SqlAlchemy?

## Features of Transaction

In Transaction
- All operations are either **all successful** or **all failed**
  - That is, the operations in the Transaction are Atomic

Transaction usually includes the following steps
- Start Transaction
- Perform operations
  - Multiple operations may be performed in this transaction, such as:
    - Add one more object instance and modify another object instance ...
- End Transaction
  - If the operation is successful, `Commit` Transaction
  - If the operation fails, `Rollback` Transaction


## Use Transaction in `SqlAlchemy`

In SqlAlchemy, Transaction is implemented through `Session`. Here is a simple Transaction example

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Create engine
engine = create_engine("sqlite:///example.db")

# Create session
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

# service layer
def create_user(db: Session, user):
  """
  Create user
  """

  # other business logic
  # user.name = user.name.capitalize()
  # user.age = user.age + 1

  try:
    db.add(user)
    db.commit()
    return user
  except Exception as e:
    db.rollback()
    raise e


# controller layer
def create_user_controller(user):
    """
    Create user controller
    """
    db = next(get_db())
    return create_user(db, user)
```

The `sessionmaker` creates a module-level factory for `Session`. In `get_db`, a `Session` instance is obtained using `SessionLocal()`, and the `Session` is closed in the `finally` block.

In the controller layer, it is only responsible for injecting the `Session` instance into the service layer's `create_user`.

In this way, all operations in the service layer are already within a Transaction. If any operation in `create_user` fails, the entire Transaction will `Rollback`, and no changes will be made to the database.

## Using `SqlAlchemy` Transactions in `FastAPI`

Using SqlAlchemy Transactions in FastAPI is also very simple. FastAPI provides `Depends` to implement `Dependency Injection`. You can use a Generator Function as a parameter for `Depends` and obtain the `Session` instance yielded in `get_db` within `Depends`.

> Unlike the example above, there is no need to use `next` to get the `Session` instance.



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
        user_1 = service.create_user(db=db, user=user_1)
        user_2 = service.create_user(db=db, user=user_2)
        db.commit()
        return [user_1, user_2]
    except:
        db.rollback()
        raise HTTPException(status_code=500, detail="SqlAlchemy Transaction Error")
```


## Reference
- https://stackoverflow.com/questions/65699977/fastapi-sqlalchemy-how-to-manage-transaction-session-and-multiple-commits
- https://docs.sqlalchemy.org/en/20/orm/session_basics.html#using-a-sessionmaker