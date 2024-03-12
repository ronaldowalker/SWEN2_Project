from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from App.controllers.csv import *
import os

csv_views = Blueprint('csv_views', __name__, template_folder='../templates')

@csv_views.route('/upload_csv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and file.filename.endswith('.csv'):
        filename = secure_filename(file.filename)
        file_path = os.path.join('App', 'Csv', filename)  # Assuming 'App/Csv' is the path to save CSV files
        file.save(file_path)
        try:
            populate_db_from_csv(file_path)
            return jsonify({'message': 'CSV file uploaded successfully'})
        except Exception as e:
            return jsonify({'error': 'Invalid file'})

if __name__ == '__main__':
    app.run(debug=True)
