SHELL:=/bin/bash

deployment: ## Deploy the scheduled training workflow
	@docker exec -t prefect python s3_remote_storage.py
	@docker exec -t prefect prefect deployment build ./train.py:main --name "Credit Churn Deployment" --tag credit-churn-experiment --cron "0 0 * * *" --storage-block remote-file-system/minio
	@docker exec -t prefect prefect deployment apply main-deployment.yaml
	@docker exec -td prefect prefect agent start --tag credit-churn-experiment

run: ## Execute the training workflow
	@docker exec -ti prefect prefect deployment run "main/Credit Churn Deployment"

post_request:
	@docker exec -ti app python send_requests.py --file-path data/BankChurnersSample.csv

help: ## Help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'