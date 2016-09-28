import os
from redis import Redis
from pymongo import MongoClient
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class BaseConfiguration(object):
    APP_ENV = os.environ.get("APP_ENV")
    WTF_CSRF_ENABLED = False
    DEBUG = os.environ.get("DEBUG_MODE") == "True"
    MONGODB_SETTINGS = {
        'db': os.environ.get("MONGO_DB_NAME"),
        'host': os.environ.get("MONGO_URL")
    }

    SECRET_KEY = os.environ.get("SECRET_KEY")

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
    redis_host, redis_port = r.split('/')[2].split(':')
    redis_connection = Redis(host=redis_host, port=redis_port)

    return redis_connection


def get_multivac_db():
    # Connect to the mongodb db
    username = os.environ.get("MONGO_USERNAME")
    password = os.environ.get("MONGO_PASSWORD")
    server = os.environ.get("MONGO_SERVER")

    # To account for local, protection-less dbs
    if password == "":
        mongourl = "mongodb://%s" % server
    else:
        mongourl = "mongodb://%s:%s@%s/%s" % (username, password, server, "multivac")

    log.debug("Connecting to the %s mongo database." % mongourl)
    client = MongoClient(mongourl, 27017)
    db = client.get_database("multivac")

    return db
