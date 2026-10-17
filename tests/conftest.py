import pytest

from database.db import db


@pytest.fixture(autouse=True)
def clean_db():
    db.reset()
    yield
    db.reset()
