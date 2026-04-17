from pydantic_settings import BaseSettings

class AppConfig(BaseSettings):
    BASE_RESOLUTION: int = 12

    CENTER_LAT: int = 56
    CENTER_LON: int = 38

    BASE_RADIUS_KM: int = 7

app_config = AppConfig()