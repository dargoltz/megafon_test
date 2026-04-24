import pytest


@pytest.mark.parametrize(
    "resolution, excepted",
    [
        (0, 100),
        (1, 100),
        (2, 200),
        (3, 200),
        (4, 300),
        (5, 400),
        (6, 1000),
        (12, 532933)
    ]
)
def test_avg(client, resolution, excepted):
    response = client.get("/avg", params={'resolution': resolution})
    assert response.status_code == 200
    assert len(response.json()) == excepted
