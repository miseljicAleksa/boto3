from flask import render_template, request, redirect, url_for, flash, Response, jsonify
from app import app, db
from datetime import datetime
from config import S3_BUCKET, S3_KEY, S3_SECRET
from flask_bootstrap import Bootstrap
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
    
    @staticmethod
    def makeUrl():
        for c in Wrapper.comments:
            params = {'Bucket': "bucket-flask-us", 'Key': c.name }
            c.urlocator = Wrapper.s3_client.generate_presigned_url('get_object', params)
        return c.urlocator

    @staticmethod
    def uploadFile():
        file = request.files['file']
        now = datetime.now()    
        fname = file.filename + "_" + str(now)
        Wrapper.my_bucket.Object(fname).put(Body=file)
        newFile= Files(title=request.form.get("title"), name=fname)
        db.session.add(newFile)
        db.session.commit()
        return newFile
  
    @staticmethod
    def deleteFile():
        key = request.form['key']
        delete = Wrapper.my_bucket.Object(key).delete()
        dlt = Files.query.filter_by(name=key).one()
        db.session.delete(dlt)
        db.session.commit()
        return delete

    @staticmethod
    def downloadFile():
        key = request.form['key']
        my_bucket = Wrapper.s3_resource.Bucket(S3_BUCKET)
        file_obj = my_bucket.Object(key).get()
        return file_obj