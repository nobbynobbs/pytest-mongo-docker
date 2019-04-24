import time

import pymongo
import pytest


@pytest.yield_fixture
def mongo_client(mongo_server):
    port = mongo_server["mongo_port"]
    client = pymongo.MongoClient("127.0.0.1:{}".format(port))
    yield client
    client.close()

@pytest.yield_fixture(scope="session")
def mongo_server(unused_port, session_id, docker):
    docker.pull("jamesridgway/mongo-tmpfs:4.0")
    port = unused_port()
    container = docker.create_container(
        image="jamesridgway/mongo-tmpfs:4.0",
        name="test-mongo-{}".format(session_id),
        ports=[27017], detach=True,
        host_config=docker.create_host_config(
            port_bindings={27017: port},
            privileged=True,
        )
    )
    docker.start(container=container["Id"])
    wait_mongo(port)
    container["mongo_port"] = port
    yield container
    docker.kill(container=container["Id"])
    docker.remove_container(container["Id"])

def wait_mongo(port):
    timeout = 0.001
    for _ in range(20):
        try:
            client = pymongo.MongoClient("127.0.0.1:{}".format(port))
            client.irkkt.command("ping")
        except pymongo.errors.ServerSelectionTimeoutError:
            time.sleep(timeout)
            timeout *= 2
        else:
            client.close()
            return
    else:
        raise RuntimeError("Unable to connect to mongodb at port %s", port)


