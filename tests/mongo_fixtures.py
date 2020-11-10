import time

import pymongo
import pytest


MONGO_IMAGE = "mongo:3.4"


@pytest.fixture
def mongo_client(mongo_server):
    port = mongo_server.mongo_port
    client = pymongo.MongoClient(f"127.0.0.1:{port}")
    yield client
    client.close()

@pytest.fixture(scope="session")
def mongo_server(unused_port, session_id, docker):
    port = unused_port()
    docker.images.pull(MONGO_IMAGE)
    container = docker.containers.run(
        image=MONGO_IMAGE,
        command=["mongod", "--storageEngine", "ephemeralForTest"],
        detach=True,
        ports={'27017/tcp': port},
        name=f"test-mongo-{session_id}",
        # auto-remove=True,
        # remove=True,
    )
    wait_mongo(port)
    container.mongo_port = port
    yield container
    container.stop(timeout=5)
    container.remove(v=True)

def wait_mongo(port):
    timeout = 0.001
    for _ in range(20):
        try:
            client = pymongo.MongoClient(f"127.0.0.1:{port}")
            client.test.command("ping")
        except pymongo.errors.ServerSelectionTimeoutError:
            time.sleep(timeout)
            timeout *= 2
        else:
            client.close()
            return
    else:
        raise RuntimeError(f"Unable to connect to mongodb at port {port}")
