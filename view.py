from app import app
from flask import render_template
from flask import send_file


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/author', methods=['POST', 'GET'])
def author():
    return render_template('author.html')

@app.route('/resume', methods=['GET', 'POST'])
def download():
    return send_file("static/CV_Vlad_Timofeev.docx", as_attachment=True)
