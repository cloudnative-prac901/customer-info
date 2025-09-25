# tests/test_health.py
import os, sys, types

# app/ を import パスに追加（CodeBuild でもローカルでも動くように保険）
sys.path.insert(0, os.path.abspath("app"))

# boto3 を Secrets Managerだけダミー化
class _FakeSecretsClient:
    def get_secret_value(self, SecretId):
        # テスト用のダミー資格情報を返す
        return {"SecretString": '{"username":"test_user","password":"test_pass","port":3306}'}

def _fake_boto3_client(service_name, region_name=None):
    assert service_name == "secretsmanager"
    return _FakeSecretsClient()

# boto3 モジュールを差し替え（最低限のAPIだけ持つ偽オブジェクト）
sys.modules['boto3'] = types.SimpleNamespace(client=_fake_boto3_client)

# アプリのimport
import app as target  # app/app.py が読み込まれる（PYTHONPATH=.../app 前提）
app = target.app

# テスト
def test_index_returns_ok():
    client = app.test_client()
    res = client.get("/")
    assert res.status_code == 200
    assert b"OK" in res.data
