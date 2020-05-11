scp -i ~/.ssh/$2.pem emr_requirements.txt $1:~
scp -i ~/.ssh/$2.pem scraper_setup.py $1:~
scp -i ~/.ssh/$2.pem scraper_aws.py $1:~