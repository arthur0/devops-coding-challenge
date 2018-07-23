import os
import redis
from pymongo import MongoClient
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class BaseConfiguration(object):
    APP_ENV = os.environ.get("APP_ENV")
    WTF_CSRF_ENABLED = False
    DEBUG = os.environ.get("DEBUG_MODE") == "True"
    MONGODB_URL = os.environ.get("MONGO_URL")

    SECRET_KEY = os.environ.get("SECRET_KEY")

    REDIS_URL = os.environ.get("REDIS_URL", "localhost")
    RQ_DEFAULT_URL = REDIS_URL

    FORCE_ENGINE = os.environ.get("FORCE_ENGINE", None)


class TestConfiguration(BaseConfiguration):
    TESTING = True
    DEBUG = False
    MONGODB_SETTINGS = {
        'db': 'multivac_test',
    }


def get_env_var(varname):
    import os
    from dotenv import load_dotenv

    load_dotenv('.env')

    return os.environ.get(varname)


def get_redis_connection():
    # Redis connection
    r = get_env_var("REDIS_URL")
    redis_connection = redis.from_url(r)

    return redis_connection


def get_multivac_db():
    # Connect to the mongodb db
    mongourl = os.environ.get("MONGO_URL")

    log.debug("Connecting to the %s mongo database." % mongourl)
    client = MongoClient(mongourl)
    db = client.get_database("multivac")

    return db
