def test_home(client):
    resp = client.get("/")

    assert resp.status_code == 200


def test_add_todo(client):
    resp = client.get("/add")

    assert resp.status_code == 200


def test_update_todo(client):
    resp = client.get("/update/1")

    assert resp.status_code == 200
