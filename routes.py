from app import app
from flask import render_template, request, redirect, url_for, flash, Response, jsonify
import boto3
from models import Files
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

@app.route('/download', methods=['POST'])
def download():
    key = request.form['key']
    Wrapper.downloadFile()
    return Response(
        Wrapper.downloadFile()['Body'].read(),
        headers={"Content-Disposition": "attachment;filename={}".format(key)}
    )   

    


