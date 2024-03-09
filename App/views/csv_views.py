
from flask import Blueprint, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from App.controllers.csv import populate_db_from_csv

csv_blueprint = Blueprint('csv_blueprint', __name__)

@csv_blueprint.route('/upload', methods=['GET', 'POST'])
def upload_csv():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and file.filename.endswith('.csv'):
            filename = secure_filename(file.filename)
            file_path = os.path.join('uploads', filename)  # Assuming 'uploads' is within the root directory
            file.save(file_path)
            populate_db_from_csv(file_path)
            os.remove(file_path)  # Remove the file after processing
            return 'CSV Uploaded and Database Populated'
    return render_template('upload.html')
