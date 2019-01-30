from flask import render_template, request, redirect, url_for, flash, Response, jsonify
from app import app, db
from datetime import datetime
from config import S3_BUCKET, S3_KEY, S3_SECRET
from flask_bootstrap import Bootstrap
import boto3
from models import Files
from filters import datetimeformat, file_type
from helpers import Wrapper




@app.route('/')
def index():
    return render_template("index.html")


@app.route('/files', methods=["GET", "POST"])
def files():
    bucket = Wrapper.my_bucket
    files = Wrapper.summaries
    comments = Wrapper.comments
    Wrapper.makeUrl()
    
    return render_template('files.html', my_bucket=bucket, files=files, comments=comments)



@app.route('/upload', methods=['POST'])
def upload():
    if request.form:
        Wrapper.uploadFile()
    
    flash('rigi uploaded file successfully')
    return redirect(url_for('files'))
  





@app.route('/delete', methods=['POST'])
def delete():
    Wrapper.deleteFile()
    flash('rigi deleted file successfully')
    return redirect(url_for('files'))
    #ne brise iz baze, samo s bucketa, ne znam kako da izvucem id iz key-a!!!



@app.route('/download', methods=['POST'])
def download():
    key = request.form['key']
    Wrapper.downloadFile()
    return Response(
        Wrapper.downloadFile()['Body'].read(),
        mimetype='text/plain',
        headers={"Content-Disposition": "attachment;filename={}".format(key)}
    )   


