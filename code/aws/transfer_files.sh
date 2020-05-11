scp -i ~/.ssh/$2.pem elephas_requirements.txt $1:~
scp -i ~/.ssh/$2.pem elephas_setup.sh $1:~
scp -i ~/.ssh/$2.pem process_mp3.sh $1:~
scp -i ~/.ssh/$2.pem spark_build_model.py $1:~
scp -i ~/.ssh/$2.pem spark_model_building_functions.py $1:~
scp -i ~/.ssh/$2.pem spark_preprocessing_functions.py $1:~
scp -i ~/.ssh/$2.pem spark_preprocessing.py $1:~
scp -i ~/.ssh/$2.pem wavenet.py $1:~
