import sys
import os
import pytest

from app import app


# set dir enviroment
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)


@pytest.fixture
def client():
    app.config["TESTING"] = True
    client = app.test_client()

    yield client


def test_main(client) -> None:
    response = client.get("/")

    assert response.status_code == 302
