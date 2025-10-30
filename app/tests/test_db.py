import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Base, User, Item
from app.db.repository import create_user, create_item
from app.schemas.user import UserCreate
from app.schemas.item import ItemCreate

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

@pytest.fixture()
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

def test_create_user(db_session):
    user_in = UserCreate(email="test@example.com", password="password")
    user = create_user(db_session, user_in)
    assert user.email == "test@example.com"
    assert user.id is not None

def test_create_item(db_session):
    item_in = ItemCreate(id="test_item", title="Test Item", description="This is a test item")
    item = create_item(db_session, item_in)
    assert item.id == "test_item"
    assert item.title == "Test Item"
