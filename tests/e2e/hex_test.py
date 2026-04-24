import pytest


@pytest.mark.parametrize(
    "h, excepted",
    [
        ("8d118c9108f617f", 0),  # resolution: 13 (in circle)
        ("8c1119251c6bdff", 0),  # resolution: 12 (not in circle)
        ("8c118c9320a33ff", 1),  # resolution: 12 (in circle)
        ("8b1119251c6bfff", 0),  # resolution: 11 (not in circle)
        ("8b11aa648361fff", 7),  # resolution: 11 (in circle)
        ("81757ffffffffff", 0),  # resolution:  1 (not in circle)
        ("8111bffffffffff", 532933),  # resolution:  1 (in circle)
    ],
)
def test_hex(client, h: str, excepted: int):
    response = client.get('/hex', params={'hex': h})
    assert response.status_code == 200
    assert len(response.json()) == excepted
