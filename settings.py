from lib2to3.pytree import Base
from pydantic import BaseSettings


class Settings(BaseSettings):
    NORMALIZATION_URL: str
    MONGO_CONNECTION: str
    FITS_BUCKET: str
    SET_SPORT_URL: str

settings = Settings()