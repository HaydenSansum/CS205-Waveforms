wget https://harvard-iacs.github.io/2020-CS205/lab/I10/src/wordcount.py
wget https://harvard-iacs.github.io/2020-CS205/lab/I10/src/input.txt

hadoop fs -put input.txt
mv input.txt input_local.txt

spark-submit wordcount.py

hadoop fs -ls

