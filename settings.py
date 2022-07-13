from pydantic import BaseSettings

class Settings(BaseSettings):
    NORMALIZATION_URL: str
    MONGO_CONNECTION: str
    FITS_BUCKET: str
    SET_SPORT_URL: str
    NUM_SESSIONS: int