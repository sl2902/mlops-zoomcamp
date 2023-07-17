import sys
import pickle
import pandas as pd
import argparse
import os
from typing import List



def prepare_data(df, categorical):
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    return df

def read_data(filename, categorical: List[str]):

    S3_ENDPOINT_URL = os.getenv('S3_ENDPOINT_URL')

    if S3_ENDPOINT_URL is not None and S3_ENDPOINT_URL != "": 
        options = {
        'client_kwargs': {
            'endpoint_url': S3_ENDPOINT_URL
        }
    }

        df = pd.read_parquet(filename, storage_options=options)
    else:
        df = pd.read_parquet(filename)
    
    return prepare_data(df, categorical)

def write_date(filename, df):
    S3_ENDPOINT_URL = os.getenv('S3_ENDPOINT_URL')

    if S3_ENDPOINT_URL is not None and S3_ENDPOINT_URL != "":
        options = {
            'client_kwargs': {
                'endpoint_url': S3_ENDPOINT_URL
            }
        }

        df.to_parquet(filename, engine='pyarrow', index=False, storage_options=options)
    else:
        df.to_parquet(filename, engine='pyarrow', index=False)

def get_input_path(year, month):
    default_input_pattern = 'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet'
    input_pattern = os.getenv('INPUT_FILE_PATTERN', default_input_pattern)
    return input_pattern.format(year=year, month=month)


def get_output_path(year, month):
    # default_output_pattern = f'output/yellow_tripdata_{year:04d}-{month:02d}.parquet'
    default_output_pattern = 's3://nyc-duration/taxi_type=yellow_tripdata/year={year:04d}/month={month:02d}/predictions.parquet'
    output_pattern = os.getenv('OUTPUT_FILE_PATTERN', default_output_pattern)
    return output_pattern.format(year=year, month=month)


def main(year, month):

    input_file = get_input_path(year, month)
    output_file = get_output_path(year, month)

    with open('model/model.bin', 'rb') as f_in:
        dv, lr = pickle.load(f_in)


    categorical = ['PULocationID', 'DOLocationID']

    df = read_data(input_file, categorical)
    df['ride_id'] = f'{args.year:04d}/{args.month:02d}_' + df.index.astype('str')


    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = lr.predict(X_val)


    print('predicted mean duration:', y_pred.mean())


    df_result = pd.DataFrame()
    df_result['ride_id'] = df['ride_id']
    df_result['predicted_duration'] = y_pred

    write_date(output_file, df_result)
    # df_result.to_parquet(output_file, engine='pyarrow', index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", help="Enter year for taxi trip data - yyyy", type=int, default=2023)
    parser.add_argument("--month", help="Enter month for taxi trip data", type=int, default=1)
    args = parser.parse_args()

    if len(str(args.year)) != 4 or args.year < 2000 or args.year > 2023:
        raise ValueError("Invalid year format or invalid year. Valid range is [2000-2023]")
    if args.month < 1 or args.month > 12:
        raise ValueError("Invalid month. Valid range is [1-12]")
    main(args.year, args.month)