import concurrent.futures
import logging
import time

import certifi
import pymongo
import requests
from bson import ObjectId
from google.cloud import storage
from settings import Settings

settings = Settings()


logger = logging.getLogger()

# STORAGE
storage_client = storage.Client()
bucket = storage_client.bucket(settings.FITS_BUCKET)

def process_sess(sess):
    fit = get_fit(f"{sess['firestore_user_id']}_{sess['session_id']}.fit")
    if fit is None:
        return 
    id_mongo = sess["_id"]
    sport_id = sess.get("sport_id", None)
    privacy = sess.get("privacy", None)
    print(f"Processing session: {id_mongo} from user: {sess['firestore_user_id']}")
    params_dic = {
        "user_id": sess["user_id"],
        "firestore_user_id": sess["firestore_user_id"],
        "device_user_id": sess["device_user_id"],
        "device": sess["device"].upper(),
        "session_id": sess["session_id"],
        "id_mongo": id_mongo,
        "sport_id": sport_id,
        "privacy": privacy

    }
    #Llamada a la siguiente function
    time.sleep(1)
    res = requests.post(url=settings.NORMALIZATION_URL, data=fit, params=params_dic, headers={'Content-Type': 'application/octet-stream'})
    logger.info(res.status_code)
    print(res.status_code)
    if res.status_code != 200:
        logger.error(f"Error with session: {id_mongo} on normalization/clean")
        logger.error(res.content)
        return

    params_back = {
        "userId": sess["firestore_user_id"],
        "sessionId": id_mongo,
        "sportId": "" if sport_id is None else sport_id,
        "privacy": "public" if privacy is None else privacy
    }

    res = requests.post(url=settings.SET_SPORT_URL, params=params_back)
    time.sleep(1)


def get_fit(fit_name):
    file = bucket.blob(fit_name)
    try:
        return file.download_as_bytes()
    except Exception:
        return None


threads = []
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    for skip in range(0, settings.NUM_SESSIONS, 5):
        client = pymongo.MongoClient(settings.MONGO_CONNECTION, tlsCAFile=certifi.where()) #PROD
        db_mongo = client.Kanara
        print(f"Number of elements: {skip}")
        sess = db_mongo.Sessions.find({}).skip(skip).limit(5).sort("_id", pymongo.DESCENDING)
        for session in sess:
            print(session["_id"])
            future = executor.submit(process_sess, session)
        client.close()
        del client
        del db_mongo
        time.sleep(3)
            

