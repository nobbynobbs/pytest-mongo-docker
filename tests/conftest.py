import socket
import uuid

import docker as libdocker
import pytest

pytest_plugins = ['mongo_fixtures']

@pytest.fixture(scope="session")
def session_id():
    return str(uuid.uuid4())

@pytest.fixture(scope="session")
def unused_port():
    def f():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(('127.0.0.1', 0))
            return sock.getsockname()[1]
    return f

@pytest.fixture(scope="session")
def docker():
    return libdocker.APIClient(version="auto")
