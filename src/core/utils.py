from fastapi import HTTPException


def parse_borders(borders: str) -> list[tuple[float, float]]:
    result = []

    try:
        for border in borders.split(','):
            parts = border.split('/')
            if len(parts) != 2:
                raise ValueError

            lat, lon = map(float, parts)
            result.append((lat, lon))

    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid border format. Use lat/lon,lat/lon"
        )

    return result
