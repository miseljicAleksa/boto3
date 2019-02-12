from flask import request
from app import db
from datetime import datetime
from config import S3_BUCKET, S3_KEY, S3_SECRET
import boto3
from models import Files


class Wrapper:
    s3_resource = boto3.resource(
        "s3",
        aws_access_key_id = S3_KEY,
        aws_secret_access_key = S3_SECRET    
    )

    s3_client = boto3.client(
        "s3",
        aws_access_key_id = S3_KEY,
        aws_secret_access_key = S3_SECRET 
    )

    my_bucket = s3_resource.Bucket(S3_BUCKET)
    summaries = my_bucket.objects.all()
    comments = Files.query.all()



    @classmethod
    def get_files(cls):
        files = Files.query.all()
        for f in files:
            params = {'Bucket': "bucket-flask-us", 'Key': f.name }
            f.urlocator = cls.s3_client.generate_presigned_url('get_object', params)
        return files


    @classmethod
    def save_file(cls, file):
        """
        File name is created in this way:
        file.name + _ + utc.now()

        :param file: File that is going to be saved
        :return: Saved file
        """
        now = datetime.now()    
        fname = file.filename + "_" + str(now)

        cls.my_bucket.Object(fname).put(Body=file)

        newFile= Files(title=request.form.get("title"), name=fname)
        db.session.add(newFile)
        db.session.commit()

        return newFile
  
    @classmethod
    def delete_file(cls, filename):
        """
        :param filename: Name of the file to be deleted
        :return: None if succesfull
        """
        delete = cls.my_bucket.Object(filename).delete()
        dlt = Files.query.filter_by(name=filename).one()

        db.session.delete(dlt)
        db.session.commit()

        return delete

    @classmethod
    def get_file_data(cls, filename):
        """
        :param filename: Name of the file to be downloaded
        :return: file data
        """
        my_bucket = cls.s3_resource.Bucket(S3_BUCKET)
        downloaded_file = my_bucket.Object(filename).get()

        return downloaded_file