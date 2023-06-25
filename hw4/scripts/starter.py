import pickle
import pandas as pd
import argparse


with open('model.bin', 'rb') as f_in:
    dv, model = pickle.load(f_in)

categorical = ['PULocationID', 'DOLocationID']

def read_data(filename):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', type=int, help="Enter a four digit year - yyyy", default=2022)
    parser.add_argument('--month', help="Enter month", type=int)
    args = parser.parse_args()

    if args.month is None:
        raise ValueError("Invalid month. Valid values range between [1-12] inclusive")

    if args.year:
        if len(str(args.year)) != 4:
            raise ValueError("Invalid year entered. Thee format is yyyy")
    if args.month:
        if args.month < 1 or args.month > 12:
            raise ValueError("Invalid month. Valid values range between [1-12] inclusive")
        
    df = read_data(f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{args.year:04}-{args.month:02}.parquet')
    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = model.predict(X_val)
    print(f'Mean predicted duration {y_pred.mean()}')

if __name__ == "__main__":
    main()



