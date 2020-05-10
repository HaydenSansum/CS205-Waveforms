scp -i ~/.ssh/CS205-key.pem elephas_requirements.txt $1:~
scp -i ~/.ssh/CS205-key.pem elephas_setup.sh $1:~
scp -i ~/.ssh/CS205-key.pem get_song_sample.sh $1:~
scp -i ~/.ssh/CS205-key.pem spark_build_model.py $1:~
scp -i ~/.ssh/CS205-key.pem spark_build_model_latesttest.py $1:~
scp -i ~/.ssh/CS205-key.pem spark_model_building_functions.py $1:~
scp -i ~/.ssh/CS205-key.pem spark_preprocessing_functions.py $1:~
scp -i ~/.ssh/CS205-key.pem spark_preprocessing.py $1:~
scp -i ~/.ssh/CS205-key.pem wavenet.py $1:~
scp -i ~/.ssh/CS205-key.pem test_hdfs.sh
