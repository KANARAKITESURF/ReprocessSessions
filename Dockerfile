FROM python:3.9-slim

WORKDIR /app

COPY  . ./

ENV NORMALIZATION_URL="https://europe-west1-kanaraflutterdev.cloudfunctions.net/normalizationAPI-REPROCESS"
ENV MONGO_CONNECTION="mongodb+srv://VectorizationAPI:yF6gfh2n6VALktyk@dev.inl0u.mongodb.net/Kanara?retryWrites=true&w=majority"
ENV FITS_BUCKET="kanara-fit-files"
ENV SET_SPORT_URL="https://develpkanarasports.herokuapp.com/setSportAndPrivacyAsyncReprocess"
ENV NUM_SESSIONS=100
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/kanara-firestore-DEV.json"

RUN python3 -m pip install -r requirements.txt

CMD ["python3", "-m", "http.server", "8000"]
