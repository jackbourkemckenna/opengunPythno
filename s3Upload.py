import boto3
import os
import glob
# Create an S3 client
s3 = boto3.client('s3')
bucket_name = 'open-gun-recordings'
path = "bin/"
userID = ""
def uploadDirectory(path,bucketname,userID):
    directory_name = "users/screenshots"

    for root,dirs,files in os.walk(path):
        for file in files:
            #s3C.upload_file(os.path.join(root,file),bucketname,file)
            #ExtraArgs={'ACL':'public-read'}

            s3.upload_file(os.path.join(root,file),bucket_name, Key=(directory_name+'/'+userID+'/'+file),ExtraArgs = {"ContentType": "image/jpeg",'ACL':'public-read'})


uploadDirectory("bin/", "open-gun-recordings",userID)
