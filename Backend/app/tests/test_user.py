# tests/test_user.py
from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.User_Table import User
from app.core.security import get_password_hash
from app.db.test_session import TestingSessionLocal
from app.api.deps import role_required, get_db

client = TestClient(app)

from app.main import app

# def fake_admin_user(roles_required=None):
#     return {"user_id": 1, "role": 1}

# # Fake regular user (role 2)
# def fake_regular_user(roles_required=None):
#     return {"user_id": 2, "role": 2}

def test_signup_creates_user():
    db = TestingSessionLocal()

    db.query(User).filter(User.Username == "test_keerthi").delete()
    db.commit()

    response = client.post(
        "/user/Signup",
        json={
            "username": "test_keerthi",
            "first_name": "Test",
            "last_name": "User",
            "email": "testkeerthi@gmail.com",
            "phone": "9999999999",
            "password": "1234",
            "role_id": 1,
            "is_active": True
        }
    )
    assert response.status_code == 200

# LOGIN SUCCESS

def test_login_success():
    response = client.post(
        "/user/Login",
        json={"username_or_email": "test_keerthi", "password": "1234"}  # plain password
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
        json={"email": "testkeerthi@gmail.com"}
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

# def test_otp():


#     # Call the endpoint
#     response = client.post(
#         "/user/Otpverify",
#         json={
#             "otp": 793014,
#             "resetkey": "bkyNZChgJScycduqVWIqG3xf8s0JSW"
#         }
#     )

#     # Assert status code
#     assert response.status_code == 200

# def test_change_password():


#     response = client.post(
#         "/user/change_password",
#         json={
#             "Current_Password": "1234",
#             "new_password": "123456",
#             "confirm_password":"123456"

#         }
#     )
#     assert response.status_code in [200]


# def test_change_password_invalid():

#     response = client.post(
#         "/user/change_password",
#         json={
#             "Current_Password": "wrongpass",
#             "new_password": "1234",
#             "confirm_password":"1234"

#         }
#     )
#     assert response.status_code in [400, 404]



# # -------------------------
# #  UPDATE USER (FormData)
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
