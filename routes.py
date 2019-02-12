from app import app
from flask import render_template, request, redirect, url_for, flash, Response, jsonify
from helpers import Wrapper


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/files', methods=["GET"])
def files():
    files = Wrapper.get_files()
    return render_template('files.html', comments=files)


@app.route('/upload', methods=['POST'])
def upload():
    if request.form:
        file = request.files['file']
        Wrapper.save_file(file)
    flash('rigi uploaded file successfully')
    return redirect(url_for('files'))


@app.route('/delete', methods=['POST'])
def delete():
    key = request.form['key']
    Wrapper.delete_file(key)
    flash('rigi deleted file successfully')
    return redirect(url_for('files'))


@app.route('/download', methods=['POST'])
def download():
    key = request.form['key']
    Wrapper.get_file_data(key)
    return Response(
        Wrapper.get_file_data(key)['Body'].read(),
        headers={"Content-Disposition": "attachment;filename={}".format(key)}
    )




