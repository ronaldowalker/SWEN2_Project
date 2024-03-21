from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename
from App.controllers.csv import populate_db_from_csv
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
        # Update the file_path to store in the desired directory
        file_path = os.path.join('/workspaces/Info3604_Project/App/Csv', filename)
        file.save(file_path)
        try:
            populate_db_from_csv(file_path)
            return jsonify({'message': 'CSV file uploaded successfully'})
        except Exception as e:
            return jsonify({'error': 'Invalid file'})

if __name__ == '__main__':
    app.run(debug=True)
