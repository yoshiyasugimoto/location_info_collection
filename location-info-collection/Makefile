deploy:
	sls deploy --stage production

offline_api:
	sls offline start --httpPort 3003

local_post:
	curl -X POST -H "Content-Type: application/json" -d @../sent_from_smartphone.json http://localhost:3003/production/post

local_output:
	sls invoke local -f output

local_bucket_list:
	curl http://localhost:3003/production/bucket_list

local_downlocal_csv:
	curl http://localhost:3003/production/download_csv/2021-09-12-location-info-collection.csv