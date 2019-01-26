from app import db

class Comment(db.Model):
    name = db.Column(db.String(80), unique=True, nullable=False, index=True)
    title = db.Column(db.String(80),unique=False, nullable=True)
    urlocator = db.Column(db.String(256), unique=True, primary_key=True)

    def __repr__(self):
        return "<Title: {}>".format(self.urlocator)
