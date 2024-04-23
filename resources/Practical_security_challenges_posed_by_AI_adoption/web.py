from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///uploads.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
db = SQLAlchemy(app)

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100))

with app.app_context(): #https://stackoverflow.com/a/74000056/12534623
    db.create_all()

@app.route('/')
def index():
    documents = Document.query.all()
    return render_template('index.html') # https://stackoverflow.com/a/60256471/12534623

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        document = Document(filename=filename)
        db.session.add(document)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return render_template('uploaded_file.html', filename=filename)

if __name__ == '__main__':
    app.run(debug=True)
