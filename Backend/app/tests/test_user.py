# tests/test_user.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.User_Table import User
from app.core.security import get_password_hash
from app.db.test_session import TestingSessionLocal
from app.api.deps import role_required, get_db

client = TestClient(app)

# -------------------------
# 1️⃣ Fake logged-in user
# -------------------------
# app/tests/conftest.py or at the top of your test file
from app.main import app

def fake_admin_user(roles_required=None):
    return {"user_id": 1, "role": 1}

# Fake regular user (role 2)
def fake_regular_user(roles_required=None):
    return {"user_id": 2, "role": 2}


# 2️⃣ Fixture to create test user
# -------------------------
@pytest.fixture(scope="module", autouse=True)

def create_test_users():
    db = TestingSessionLocal()

    if not db.query(User).filter_by(Username="keerthikk").first():

        password_plain = "1234"
        user = User(
            Username="keerthikk",
            First_Name="keerthi",
            Last_Name="krishna",
            Email="keerthi@gmail.com",
            Phone="999999999",
            Password=get_password_hash(password_plain),  # hashed
            User_Role_id=2,
            Is_Active=True
        )
        db.add(user)
        db.commit()
    db.close()

# LOGIN SUCCESS

def test_login_success():
    response = client.post(
        "/user/Login",
        json={"username_or_email": "keerthikk", "password": "1234"}  # plain password
    )
    assert response.status_code == 200

# LOGIN FAIL

def test_login_invalid():
    response = client.post(
        "/user/Login",
        json={"username_or_email": "wrong", "password": "wrong"}
    )
    assert response.status_code == 401

# FOROGT PASSWORD

def test_forgot_password():
    response = client.post(
        "/user/forgot_password",
        json={"email": "keerthi@gmail.com"}
    )
    assert response.status_code == 200


# RESET PASSWORD

def test_reset_password_invalid_key():
    response = client.post(
        "/user/reset_password",
        json={
            "resetkey": "wrongkey",
            "new_password": "1234"
        }
    )
    assert response.status_code in [400, 404]

def test_change_password():

    response = client.post(
        "/user/change_password",
        json={
            "Current_Password": "1234",
            "new_password": "123456",
            "confirm_password":"123456"

        }
    )
    assert response.status_code in [200]


def test_change_password_invalid():

    response = client.post(
        "/user/change_password",
        json={
            "Current_Password": "wrongpass",
            "new_password": "1234",
            "confirm_password":"1234"

        }
    )
    assert response.status_code in [400, 404]



# # -------------------------
# # ✅ 3. UPDATE USER (FormData)
# # -------------------------
# def test_update_user():
#     response = client.put(
#         "/user/UpdateUser",
#         data={
#             "first_name": "New",
#             "last_name": "Name",
#             "email": "new@gmail.com",
#             "phone": "9999999999"
#         },
#         headers={"Authorization": "Bearer faketoken"}  # mock
#     )

#     # may fail if auth not mocked
#     assert response.status_code in [200, 401, 403]
