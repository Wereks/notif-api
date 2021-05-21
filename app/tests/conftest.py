from fastapi import Depends
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
import pytest

from ..api import app, get_db, get_db_authorized
from ..auth import oauth2_scheme, get_password_hash
from sqlalchemy.ext.declarative import declarative_base  # type: ignore
from ..models import User, Base


SQLALCHEMY_TEST_DATABASE_URI = "postgresql://postgres:admin@localhost:5432/"

"""Setups the database, adds admin,admin user for authorization"""
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URI)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

with TestingSessionLocal() as db:
        user = User(username="admin", hashed_password=get_password_hash('admin'))
        db.query(User).delete()
        db.commit()
        db.add(user)
        db.commit()
        db.refresh(user)


@pytest.fixture()
def session():
    """Connects with the database, but every commit is rolled back"""
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    session.begin_nested()
    
    yield session

    @event.listens_for(session, "after_transaction_end")
    def restart_savepoint(session, transaction):
        if transaction.nested and not transaction._parent.nested:
            session.expire_all()
            session.begin_nested()


@pytest.fixture()
def client(session):
    """Client which uses the database connection with rollbacks"""
    def override_get_db():
        yield session

    def override_get_db_authorized(user = Depends(oauth2_scheme)):
        yield session

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_db_authorized] = override_get_db_authorized
    yield TestClient(app)
    del app.dependency_overrides[get_db]
    del app.dependency_overrides[get_db_authorized]

@pytest.fixture()
def token(client):
    response = client.post('/token', data = {
        'username': 'admin',
        'password': 'admin',
    })
    return {'Authorization' :'Bearer '+ response.json().get("access_token")}