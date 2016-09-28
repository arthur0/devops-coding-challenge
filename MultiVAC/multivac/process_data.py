from config import get_multivac_db

db = get_multivac_db()


def process_data(value):
    # inserting data in db
    db.entropy.insert_one({'data': value})
