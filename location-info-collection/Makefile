deploy:
	sls deploy --stage production

offline_api:
	sls offline start

local_post:
	curl -X POST -H "Content-Type: application/json" -d @../sent_from_smartphone.json http://localhost:3000/production/post

local_output:
	sls invoke local -f output