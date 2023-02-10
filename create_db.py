from db.models import create_db
from load_data import load_data

if __name__ == '__main__':
    create_db()
    load_data()
