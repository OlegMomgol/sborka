import pytest
from psycopg2 import IntegrityError
from src.models import User, Order


class TestUserRepository:
    def test_get_by_id_success(self, user_repo, sample_user):
        user = user_repo.get_by_id(sample_user["id"])
        assert user is not None
        assert user.id == sample_user["id"]
        assert user.name == sample_user["name"]
        assert user.email == sample_user["email"]
        assert user.status == sample_user["status"]

    def test_get_by_id_not_found(self, user_repo):

        user = user_repo.get_by_id(99999)
        assert user is None

    def test_create_user_success(self, user_repo):

        new_user = User(id=None, name="New User", email="new@example.com", status="active")

        created = user_repo.create(new_user)

        assert created.id is not None
        assert created.name == new_user.name
        assert created.email == new_user.email
        assert created.status == new_user.status

        fetched = user_repo.get_by_id(created.id)
        assert fetched is not None
        assert fetched.email == new_user.email

    def test_create_user_duplicate_email(self, user_repo, sample_user):

        duplicate_user = User(
            id=None,
            name="Another User",
            email=sample_user["email"],
            status="active"
        )

        with pytest.raises(IntegrityError) as exc_info:
            user_repo.create(duplicate_user)

        assert "duplicate key" in str(exc_info.value).lower()

    def test_create_user_invalid_status(self, user_repo):

        invalid_user = User(
            id=None,
            name="Invalid User",
            email="invalid@example.com",
            status="invalid_status"
        )

        with pytest.raises(IntegrityError) as exc_info:
            user_repo.create(invalid_user)

        assert "check constraint" in str(exc_info.value).lower() or "invalid" in str(exc_info.value).lower()

    def test_delete_user(self, user_repo, sample_user):

        result = user_repo.delete(sample_user["id"])

        assert result is True
        assert user_repo.get_by_id(sample_user["id"]) is None


class TestOrderRepository:
    def test_create_order_success(self, db_connection, order_repo, sample_user):

        new_order = Order(
            id=None,
            user_id=sample_user["id"],
            product_name="Test Product",
            quantity=5
        )

        created = order_repo.create(new_order)

        assert created.id is not None
        assert created.user_id == sample_user["id"]
        assert created.product_name == "Test Product"
        assert created.quantity == 5

    def test_create_order_invalid_foreign_key(self, db_connection, order_repo):

        invalid_order = Order(
            id=None,
            user_id=99999,
            product_name="Test Product",
            quantity=5
        )

        with pytest.raises(IntegrityError) as exc_info:
            order_repo.create(invalid_order)

        assert "foreign key" in str(exc_info.value).lower() or "violates foreign key" in str(exc_info.value).lower()

    def test_create_order_invalid_quantity(self, db_connection, order_repo, sample_user):

        invalid_order = Order(
            id=None,
            user_id=sample_user["id"],
            product_name="Test Product",
            quantity=-5  
        )

        with pytest.raises(IntegrityError) as exc_info:
            order_repo.create(invalid_order)

        assert "check constraint" in str(exc_info.value).lower()


def test_transaction_rollback(db_connection, user_repo, sample_user):

    initial_count = len(user_repo.get_all())

    new_user = User(id=None, name="Temp User", email="temp@example.com", status="active")
    user_repo.create(new_user)

    assert len(user_repo.get_all()) == initial_count + 1

    db_connection.rollback()

    assert len(user_repo.get_all()) == initial_count