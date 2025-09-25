# tests/test_db_credentials.py
import os, sys, types, importlib

# app/ を import パスに追加
sys.path.insert(0, os.path.abspath("app"))

# --- boto3 をダミー化（import 前に！） ---
class _FakeSecretsClient:
    def get_secret_value(self, SecretId):
        # テストで検証したい値を返す
        return {"SecretString": '{"username":"app_user","password":"secret","port":3306}'}

def _fake_boto3_client(service_name, region_name=None):
    assert service_name == "secretsmanager"
    return _FakeSecretsClient()

sys.modules['boto3'] = types.SimpleNamespace(client=_fake_boto3_client)

# --- ここから import。app/app.py のトップレベルが実行される前にモック済み ---
target = importlib.import_module("app")  # = app/app.py

def test_load_db_credentials_returns_mock():
    creds = target.load_db_credentials()
    assert creds["username"] == "app_user"
    assert creds["password"] == "secret"
    assert int(creds.get("port", 0)) == 3306
