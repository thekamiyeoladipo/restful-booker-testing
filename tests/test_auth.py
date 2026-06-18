from utils.api_helpers import get_auth_token

class TestAuth:

    def test_generate_auth_token(self):
        token = get_auth_token()
        assert token is not None, "Token should not be None"
        assert isinstance(token, str), "Token should be a string"
        assert len(token) > 0, "Token should not be empty"

    def test_invalid_credentials_return_bad_credentials(self):
        import requests
        response = requests.post(
            "https://restful-booker.herokuapp.com/auth",
            json={
                "username": "wronguser",
                "password": "wrongpassword"
            }
        )
        data = response.json()
        assert response.status_code == 200
        assert data.get("reason") == "Bad credentials", "Invalid credentials should return bad credentials message"