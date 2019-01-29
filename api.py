from flask import request, Response, jsonify
from app import app, db
import boto3
from models import Files, FilesSchema, file_schema, files_schema



@app.route('/getfiles', methods=['GET'])
def get_all_files():
    all_files = Files.query.all()
    result = files_schema.dump(all_files)
    return jsonify(result.data)



@app.route('/getfiles/<id>', methods=['GET'])
def get_file(id):
    files = Files.query.get(id)
    return file_schema.jsonify(files)


@app.route('/createfile', methods=['POST'])
def add_files():
    name = request.json['name']
    title = request.json['title']

    new_file = Files(name, title)

    db.session.add(new_file)
    db.session.commit()

    return file_schema.jsonify(new_file)


@app.route('/getfiles/<id>', methods=['PUT'])
def update_file(id):
    files = Files.query.get(id)

    name = request.json['name']
    title = request.json['title']


    files.name = name
    files.title = title
    

    db.session.commit()

    return file_schema.jsonify(files)


@app.route('/getfiles/<id>', methods=['DELETE'])
def delete_file(id):
    files = Files.query.get(id)
    db.session.delete(files)
    db.session.commit()

    return file_schema.jsonify(files)