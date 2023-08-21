# Bank credit card churn prediction

## Introduction

In a highly competitive market, customers have a plethora of options to chose from when it comes to availaing credit card services. In order
to boost sales and increase market share banks tend to woo their customers with credit cards that offer a multitude of benefits. Some customers
take advantage of such schemes by applying for a card and using up the benefits before cancelling the card; this is called credit card churning.
The churn rate is the percentage of the bank's customer's who have attrited. By building a Machine learning model, a bank can quickly estimate the
number of customers who are likely to churn; this could result in huge cost savings for the bank

## Dataset

The dataset is obtained from [Kaggle](https://www.kaggle.com/datasets/whenamancodes/credit-card-customers-prediction?resource=download); the attributes
that make up the dataset are as follows:<br>
- `CLIENTNUM`  - Unique identifier for the customer holding the account<br/>
- `Attrition_Flag`   - Internal event (customer activity) variable - if the account is closed then 1 else 0<br/>
- `Customer_Age`  - Demographic variable - Customer's Age in Years<br/>
- `Gender`  - Demographic variable - M=Male, F=Female<br/>
- `Dependent_count`  - Demographic variable - Number of dependents<br/>
- `Education_Level`  - Demographic variable - Educational Qualification of the account holder (example: high school, college graduate, etc.)<br/>
- `Marital_Status`   - Demographic variable - Married, Single, Divorced, Unknown<br/>
- `Income_Category`  - Demographic variable - Annual Income Category of the account holder (< $40K, $40K - 60K, $60K - $80K, $80K-$120K, ><br/>
- `Card_Category` - Product Variable - Type of Card (Blue, Silver, Gold, Platinum)<br/>
- `Monthsonbook`  - Period of relationship with bank<br/>
- `TotalRelationshipcount` - Total no. of products held by the customer<br/>
- `MonthsInactive12_mon`   - No. of months inactive in the last 12 months<br/>
- `ContactsCount12_mon` - No. of Contacts in the last 12 months<br/>
- `Credit_Limit`  - Credit Limit on the Credit Card<br/>
- `TotalRevolvingBal`   - Total Revolving Balance on the Credit Card<br/>
- `AvgOpenTo_Buy` - Open to Buy Credit Line (Average of last 12 months)<br/>
- `TotalAmtChngQ4Q1` - Change in Transaction Amount (Q4 over Q1)<br/>
- `TotalTransAmt` - Total Transaction Amount (Last 12 months)<br/>
- `TotalTransCt`  - Total Transaction Count (Last 12 months)<br/>
- `TotalCtChngQ4Q1`  - Change in Transaction Count (Q4 over Q1)<br/>
- `AvgUtilizationRatio` - Average Card Utilization Ratio<br/>

The response variable is: `Attrition flag`

Only a subset of these were used for training; these are listed in the `settings.py` file.

The best trained model that is available locally was trained on the entire dataset, but for the purposes of the demo, only a subset of the dataset
was uploaded to Github due to size limitations.

## Objective

The goal of this project was not so much to build a high performing prediction model than it was to build an end to end machine learning ops pipeline;
the emphasis was less on feature engineering and hyperparameter tuning and more on model deployment, experimentation and tracking, monitoring and serving. Additionally, the other aspects of software engineering were also explored, such as: adding test cases, integration tests, quality checks and precommit hooks and github action.

## MLOps pipeline

### Architecture

<img src="artifacts/architecture.png" width="100%"/>

### Deployment

The MLOps pipeline is fully dockerised and can be easily deployed via the following steps:

1. Clone the `capstone` repository locally:

```
git clone https://github.com/sl2902/mlops-zoomcamp.git
```

    1a. If you would like to only clone the `capstone` subdirectory, then run the following commands. Note: this requires git version >= 2.30.0

```
git clone --depth 1 --filter=blob:none --sparse https://github.com/sl2902/mlops-zoomcamp.git;
cd mlops-zoomcamp;
git sparse-checkout set capstone
```

2. Prepare your environment to run the pipeline:

    ```bash
    $ cd capstone
    $ make setup
    ```

3. Build and launch the MLOps pipeline:

    ```
    $ make build
    ```
    Once ready, the following containers will be available:

|Names  			          |     Port|Description       						 |
|-----------------------------|---------|---------------------------------------:|
|app   						  |     9696|Web service api						 |
|prefect					  |     4200|Training workflow orchestration		 |
|capstone_evidently_service_1 |     8085|ML observability platform			     |
|capstone_grafana_1			  |     3000|Dashboard							     |
|mlflow_server				  |	    5000|Tracking server					     |
|create_bucket       		  |        -|Command to create bucket				 |
|minio						  |9000/9001|AWS S3 equivalent services				 |
|capstone_prometheus_1		  |     9090|Database used with Evidently and Grafana|
|mlflow_db  				  |     5432|Postgres database						 |
|capstone_mongo_1             |    27018|Mongo database							 |

