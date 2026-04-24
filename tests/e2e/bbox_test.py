import pytest


@pytest.mark.parametrize(
    "borders, excepted",
    [
        ("55.99558/38.04223,55.99528/38.04742,55.99880/38.04781,55.99611/38.05324,55.98915/38.05099,55.99272/38.05063",
         627),
        ("56.035953/37.911440,56.280315/37.589786,56.0/37.182514", 63),
        ("90/38,0/38,0/38.0007,90/38", 0),
    ]
)
def test_borders(client, borders, excepted):
    response = client.get("/bbox", params={"borders": borders})
    assert response.status_code == 200
    assert len(response.json()) == excepted
