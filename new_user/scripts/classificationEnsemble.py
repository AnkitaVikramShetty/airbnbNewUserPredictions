import future as future
import matlab.engine
import pandas as pd
import numpy as np
import os

from new_user.scripts.preProcess import pre_process
from new_user.models import pre_processed_data, test_users, results

from sqlalchemy import create_engine

def start_matlab():
    eng = matlab.engine.connect_matlab()
    # print(matlab.engine.find_matlab())

    return eng

def make_predictions(eng, x):
    print("Calling function")
    y = eng.predictUsingClassificationBaggedEnsembleByResampling("classificationBaggedEnsembleByResampling.mat",x);

    return y

def stop_matlab(eng):
    eng.quit()


def save_predictions(y, ids, filename):
    sub = pd.DataFrame(np.column_stack((ids, y)), columns=['results_id', 'country_destination'])
    sub['country_destination'] = sub['country_destination'].map(
        {1: 'NDF', 2: 'US', 3: 'other', 4: 'FR', 5: 'CA', 6: 'AU', 7: 'DE', 8: 'ES', 9: 'GB', 10: 'IT', 11: 'NL',
         12: 'PT'})

    results.objects.all().delete()
    disk_engine = create_engine('sqlite:///db.sqlite3')
    sub.to_sql('new_user_results', disk_engine, if_exists='append', index=False)

    sub.to_csv(os.path.join('media', filename), index=False)
    print('Results generated')

def user_prediction(fileName):
    eng = start_matlab()

    # ids, preProcessedFileName = pre_process()
    # print(preProcessedFileName)

    pre_process()
    dataframe = pd.DataFrame(list(pre_processed_data.objects.all().values()))
    dataframe = dataframe.drop(['id'], axis=1)

    preProcessedFileName = "pre_processed.csv";
    preProcessedFileName = os.path.join('media', preProcessedFileName);

    dataframe.to_csv(preProcessedFileName,
                     columns=["gender", "age", "signup_method", "signup_flow", "language", "affiliate_channel",
                              "affiliate_provider", "first_affiliate_tracked", "signup_app", "first_device_type",
                              "first_browser", "dac_year", "dac_month", "dac_day", "tfa_year", "tfa_month", "tfa_day"]);
    preProcessedFileName = os.path.abspath(preProcessedFileName);

    matFile = "classificationEnsembleByBayesianHyperparameterOptimization.mat";
    matFile = os.path.join('new_user', 'scripts', matFile);

    matFile = os.path.abspath(matFile);
    print(matFile)

    y = eng.predictUsingClassificationEnsemble(matFile, preProcessedFileName);
    print(y);

    os.remove(preProcessedFileName)
    print("File Removed!")
    # y = make_predictions(eng, vals)
    # print(y)

    # stop_matlab(eng)
    dataframe = pd.DataFrame(list(test_users.objects.all().values()))
    ids = dataframe.id.values

    save_predictions(y, ids, 'results.csv')
    eng.quit()