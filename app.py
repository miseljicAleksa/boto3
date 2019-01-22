from flask import Flask, render_template, request, redirect, url_for, flash, Response
from flask_bootstrap import Bootstrap
import boto3
from config import S3_BUCKET, S3_KEY, S3_SECRET
from filters import datetimeformat
from filters import datetimeformat, file_type
from flask_sqlalchemy import SQLAlchemy
import os

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))

urll='https://s3.eu-central-1.amazonaws.com/bucket-flask/slika4.jpg'



s3_resource = boto3.resource(
   "s3",
   aws_access_key_id= "AKIAI4P7ASHAQT2C7AVA",
   aws_secret_access_key="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"
)


app = Flask(__name__)
Bootstrap(app)

app.secret_key = 'secret'

app.jinja_env.filters['datetimeformat'] = datetimeformat
app.jinja_env.filters['file_type'] = file_type

app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/files', methods=["GET", "POST"])
def files():
    s3_resource = boto3.resource('s3')
    my_bucket = s3_resource.Bucket(S3_BUCKET)
    summaries = my_bucket.objects.all()

    comments = Comment.query.all()

    return render_template('files.html', my_bucket=my_bucket, files=summaries, comments=comments)


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']

    s3_resource = boto3.resource('s3')
    my_bucket = s3_resource.Bucket(S3_BUCKET)
    my_bucket.Object(file.filename).put(Body=file)

    if request.form:
        comm = Comment(title=request.form.get("title"))
        db.session.add(comm)
        db.session.commit()
    


    flash('rigi uploaded file successfully')
    return redirect(url_for('files'))



@app.route('/delete', methods=['POST'])
def delete():
    key = request.form['key']

    s3_resource = boto3.resource('s3')
    my_bucket = s3_resource.Bucket(S3_BUCKET)
    my_bucket.Object(key).delete()

    flash('rigi deleted file successfully')
    return redirect(url_for('files'))



@app.route('/download', methods=['POST'])
def download():
    key = request.form['key']

    s3_resource = boto3.resource('s3')
    my_bucket = s3_resource.Bucket(S3_BUCKET)

    file_obj = my_bucket.Object(key).get()

    return Response(
        file_obj['Body'].read(),
        mimetype='text/plain',
        headers={"Content-Disposition": "attachment;filename={}".format(key)}
    )




class Comment(db.Model):
    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)

    def __repr__(self):
        return "<Title: {}>".format(self.title)


if __name__ == "__main__":
    app.run()


