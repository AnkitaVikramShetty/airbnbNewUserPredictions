import sys, os
import csv

import numpy as np
import pandas as pd

# csv.field_size_limit(sys.maxsize)
csv.field_size_limit(2147483647)

# Full path and name to your csv file
# csv_filepathname = "test_users_10.csv"
# Full path to your django project directory
your_djangoproject_home = "../"

sys.path.append(your_djangoproject_home)
os.environ['DJANGO_SETTINGS_MODULE'] = 'airbnbNewUserPredictions.settings'

from new_user.models import test_users
# from new_user.models import train_users_2, countries
# from trial_predictions.models import train_users_2, countries
# from new_user.models import train_users_2, countries

def load_users(users):
    # dataframe = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"')
    test_users.objects.all().delete()
    count = 0

    for user in users:
        user = str(user.decode("utf-8")).strip()
        if ",,,,,,,,,,,,,," in user:
            break
        print(user)

        # av = dataframe.age.values
        # dataframe['age'] = np.where(np.logical_or(av < 14, av > 100), -1, av)
        #
        # dataframe = dataframe.fillna(-1)
        # dataframe.to_csv(csv_filepathname, index=False)
        # dataframe = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"')


        row = user.split(',')
        count += 1

        print(count)
        if row[0] != 'id':  # Ignore the header row, import everything else
            test_user = test_users()
            test_user.id = row[0]
            test_user.date_account_created = row[1]
            test_user.timestamp_first_active = row[2]
            test_user.date_first_booking = row[3]
            test_user.gender = row[4]
            if row[5] != '': test_user.age = float(row[5])
            else: test_user.age = -1
            test_user.signup_method = row[6]
            test_user.signup_flow = row[7]
            test_user.language = row[8]
            test_user.affiliate_channel = row[9]
            test_user.affiliate_provider = row[10]
            test_user.first_affiliate_tracked = row[11]
            test_user.signup_app = row[12]
            test_user.first_device_type = row[13]
            test_user.first_browser = row[14]
            test_user.save()
