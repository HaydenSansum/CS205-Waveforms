import pandas as pd
from io import StringIO
import boto3

s3 = boto3.resource('s3')

# Print out bucket names
for bucket in s3.buckets.all():
    print(bucket.name)


# Create a test datafile and try to put it into the S3 bucket in a random folder:
# NOTE Bucket must exist on S3 for it to work

a = [1,2,3,4,5,6]
b = [7,8,9,8,7,6]
c = ["a","b","c","d","e","f"]

data = pd.DataFrame(data={'a':a, 'b':b, 'c':c})
csv_buffer = StringIO()
data.to_csv(csv_buffer)

# Upload a new file
s3.Bucket('waveform-storage').put_object(Key='test_dump/test.csv', Body=csv_buffer.getvalue())