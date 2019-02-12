from app import db, ma


class Files(db.Model):
    id = db.Column(db.Integer, unique = True, autoincrement=True, primary_key=True )
    name = db.Column(db.String(80), unique=True, nullable=False, index=True)
    title = db.Column(db.String(80),unique=False, nullable=True)

    def __init__(self, name, title):
        self.name = name
        self.title = title

    def __repr__(self):
        return '<User {}>'.format(self.username)


class FilesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'title')


file_schema = FilesSchema(strict=True)
files_schema = FilesSchema(many=True, strict=True)