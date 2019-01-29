from flask import render_template, request, redirect, url_for, flash, Response, jsonify
from app import app, db
from datetime import datetime
from config import S3_BUCKET, S3_KEY, S3_SECRET
from flask_bootstrap import Bootstrap
import boto3
from models import Files
from filters import datetimeformat







s3_resource = boto3.resource(
   "s3",
   aws_access_key_id= "AKIAI4P7ASHAQT2C7AVA",
   aws_secret_access_key="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",
   
)


s3_client = boto3.client(
    "s3",
    aws_access_key_id="AKIAI4P7ASHAQT2C7AVA",
    aws_secret_access_key="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",
)





@app.route('/')
def index():
    return render_template("index.html")


@app.route('/files', methods=["GET", "POST"])
def files():
    my_bucket = s3_resource.Bucket(S3_BUCKET)
    summaries = my_bucket.objects.all()
    comments = Files.query.all()
    for c in comments:
        params = {'Bucket': "bucket-flask-us", 'Key': c.name }
        c.urlocator = s3_client.generate_presigned_url('get_object', params)
    
    return render_template('files.html', my_bucket=my_bucket, files=summaries, comments=comments)



@app.route('/upload', methods=['POST'])
def upload():
    
    file = request.files['file']
    my_bucket = s3_resource.Bucket(S3_BUCKET)


    if request.form:
        now = datetime.now()
        fname = file.filename + "_" + str(now)
        my_bucket.Object(fname).put(Body=file)
        newFile= Files(title=request.form.get("title"), name=fname)
        db.session.add(newFile)
        db.session.commit()
    
    flash('rigi uploaded file successfully')
    return redirect(url_for('files'))





@app.route('/delete', methods=['POST'])
def delete():
    key = request.form['key']
    my_bucket = s3_resource.Bucket(S3_BUCKET)
    my_bucket.Object(key).delete()

    flash('rigi deleted file successfully')
    return redirect(url_for('files'))



@app.route('/download', methods=['POST'])
def download():
    key = request.form['key']
    my_bucket = s3_resource.Bucket(S3_BUCKET)
    file_obj = my_bucket.Object(key).get()
    
    return Response(
        file_obj['Body'].read(),
        mimetype='text/plain',
        headers={"Content-Disposition": "attachment;filename={}".format(key)}
    )   

################ API
