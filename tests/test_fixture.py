

def test_mongo(mongo_client):
    response = mongo_client.irkkt.command("ping")
    assert response == {"ok": 1.0}
