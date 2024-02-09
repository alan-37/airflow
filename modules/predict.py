import json
import dill
import pandas as pd
import os
from datetime import datetime



path = os.environ.get('PROJECT_PATH', '..')


def predict():
    model_file = [pos_pkl for pos_pkl in os.listdir(f'{path}/data/models') if pos_pkl.endswith('.pkl')]
    model_filename = f'{path}/data/models/{model_file[0]}'
    with open(model_filename, 'rb') as file:
        model = dill.load(file)
    json_files = [pos_json for pos_json in os.listdir(f'{path}/data/test') if pos_json.endswith('.json')]
    df_predict = pd.DataFrame(columns=['car_id', 'predict'])
    for file_name in json_files:
        with open(f'{path}/data/test/' + file_name) as json_file:
            data = json.load(json_file)
            df1 = pd.DataFrame.from_dict([data])
            y = model.predict(df1)
            x = {'car_id': df1.id, 'predict': y}
            df2 = pd.DataFrame(x)
            df_predict = pd.concat([df_predict,df2], join="inner")
    df_predict.to_csv(f'{path}/data/predictions/pred_{datetime.now().strftime("%Y%m%d%H%M")}.csv')
    print(df_predict)


if __name__ == '__main__':
    predict()

