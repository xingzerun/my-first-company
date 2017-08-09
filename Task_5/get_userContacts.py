from pymongo import MongoClient
from datetime import date, time, datetime, timedelta

def get_userContacts(collection):
    try:
        # 遍历 chatLog -> usercontacts
        for usercontact in collection.find():
            # print(usercontact)

            userPhone = usercontact['userPhone']
            print('userPhone:%d' % userPhone)

            userContacts = usercontact['userContacts']
            print('userContacts:%d' % len(userContacts))
    except:
        print('Get Error')

def runTask(collection, day=0, hour=0, min=0, second=0):
    # Init time
    now = datetime.now()
    strnow = now.strftime('%Y-%m-%d %H:%M:%S')
    print("now:", strnow)
    # First next run time
    period = timedelta(days=day, hours=hour, minutes=min, seconds=second)
    next_time = now + period
    strnext_time = next_time.strftime('%Y-%m-%d %H:%M:%S')
    print("next run:", strnext_time)
    while True:
        # Get system current time
        iter_now = datetime.now()
        iter_now_time = iter_now.strftime('%Y-%m-%d %H:%M:%S')
        if str(iter_now_time) == str(strnext_time):
            # Get every start work time
            print("start work: %s" % iter_now_time)
            # Call task func
            get_userContacts(collection)
            print("task done.")
            # Get next iteration time
            iter_time = iter_now + period
            strnext_time = iter_time.strftime('%Y-%m-%d %H:%M:%S')
            print("next_iter: %s" % strnext_time)
            # Continue next iteration
            continue

def main():
    MONGO_URL = 'mongodb://0.0.0.0:27017/'
    MONGO_DB = 'db'
    MONGO_Collections = 'c'

    # Making a Connection with MongoClient
    client = MongoClient(MONGO_URL)

    # Getting a Database
    db = client[MONGO_DB]

    # Getting a Collection
    collection = db[MONGO_Collections]

    runTask(collection, day=0, hour=0, min=0, second=5)


if __name__ == '__main__':
    main()
