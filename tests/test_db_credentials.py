import json
import types
import app as target

class FakeSecretsClient:
    def get_secret_value(self, SecretId):
        assert SecretId == "customer-info-app-credentials"
        return {"SecretString": json.dumps({
            "username": "app_user",
            "password": "secret",
            "port": 3306
        })}

def test_load_db_credentials(monkeypatch):
    def fake_boto3_client(service_name, region_name=None):
        assert service_name == "secretsmanager"
        return FakeSecretsClient()

    monkeypatch.setenv("DB_SECRET_NAME", "customer-info-app-credentials")
    monkeypatch.setenv("AWS_REGION", "ap-northeast-2")
    monkeypatch.setattr(target, "boto3", types.SimpleNamespace(client=fake_boto3_client))

    creds = target.load_db_credentials()
    assert creds["username"] == "app_user"
    assert creds["password"] == "secret"
    assert creds["port"] == 3306
