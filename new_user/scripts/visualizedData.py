from new_user.scripts.preProcess import pre_process
from new_user.models import test_users, pre_processed_data, age_gender_bkts
import pandas as pd

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import seaborn as sns
import os

def visualize(originalFileName):
    pre_process();
    # users = pd.read_csv(fileName);
    users = pd.DataFrame(list(pre_processed_data.objects.all().values()))

    users['gender'] = users['gender'].map({"1": '-unknown-', "2": 'MALE', "3": 'FEMALE', "4": 'OTHER'});
    users.gender.value_counts(dropna=False).plot(kind='bar', color='#FD5C64', rot=0)
    plt.xlabel('Gender')
    sns.despine()

    plt.savefig(os.path.join('airbnbNewUserPredictions/static/img/gender_count.png'))
    plt.close()

    sns.distplot(users[users.age != -1].age, color='#FD5C64')
    plt.xlabel('Age')
    sns.despine()

    plt.savefig(os.path.join('airbnbNewUserPredictions/static/img/age.png'))
    plt.close()

    # if originalFileName == '':
    #     originalFileName = "test_users.csv";
    #
    # # fileName = "test_users.csv";
    # print(originalFileName)
    #
    # fileName = os.path.join('media', originalFileName);

    users = pd.DataFrame(list(test_users.objects.all().values()))
    # users = pd.read_csv(fileName);

    users['date_account_created'] = pd.to_datetime(users['date_account_created'])

    sns.set_style("whitegrid", {'axes.edgecolor': '0'})
    sns.set_context("poster", font_scale=1.1)
    users.date_account_created.value_counts().plot(kind='line', linewidth=1.2, color='#FD5C64')

    plt.savefig(os.path.join('airbnbNewUserPredictions/static/img/date_account_created.png'))
    plt.close()

    # users.timestamp_first_active = [x[0:8] for x in users.timestamp_first_active]
    # users['date_first_active'] = pd.to_datetime((users.timestamp_first_active), format='%Y%m%d')

    # users.date_first_active.value_counts().plot(kind='line', linewidth=1.2, color='#FD5C64')
    # plt.savefig(os.path.join('airbnbNewUserPredictions/static/img/date_first_active.png'))
    # plt.close()

    weekdays = []
    for date in users.date_account_created:
        weekdays.append(date.weekday())
    weekdays = pd.Series(weekdays)

    sns.barplot(x=weekdays.value_counts().index, y=weekdays.value_counts().values, order=range(0, 7))
    plt.xlabel('Week Day')
    sns.despine()

    plt.savefig(os.path.join('airbnbNewUserPredictions/static/img/weekday.png'))
    plt.close()

    # bkts = pd.DataFrame(list(age_gender_bkts.objects.all().values()))
    # sns.factorplot(x="age_bucket", y="population_in_thousands", hue="gender", col="country_destination_id", data=bkts,
    #                kind="bar", size=6)
    # plt.savefig(os.path.join('airbnbNewUserPredictions/static/img/age_gender_bkts.png'))
    # plt.close()