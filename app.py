import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from werkzeug.utils import secure_filename
from src.storage import create_request, get_request, get_all_requests, update_request_response, update_request_files
from src.validation import validate_input

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev_key_only')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

EXPERT_PASSWORD = "password123"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_request():
    make = request.form.get('make')
    model = request.form.get('model')
    try:
        year = int(request.form.get('year'))
    except (ValueError, TypeError):
        year = 0
    try:
        mileage = int(request.form.get('mileage'))
    except (ValueError, TypeError):
        mileage = -1

    vin = request.form.get('vin')
    engine_type = request.form.get('engine_type')
    symptoms = request.form.get('symptoms')
    obd_codes = request.form.get('obd_codes')

    # Handle files
    uploaded_files = request.files.getlist('files')
    filenames = []

    # Validation
    errors = validate_input(make, model, year, mileage, vin, engine_type, symptoms, obd_codes)

    if errors:
        for error in errors:
            flash(error, 'danger')
        return redirect(url_for('index'))

    # Create request data
    request_data = {
        "make": make,
        "model": model,
        "year": year,
        "mileage": mileage,
        "vin": vin,
        "engine_type": engine_type,
        "symptoms": symptoms,
        "obd_codes": obd_codes,
        "has_files": False,
        "files": []
    }

    req_id = create_request(request_data)

    # Handle File Uploads
    if uploaded_files and uploaded_files[0].filename != '':
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], req_id)
        os.makedirs(upload_path, exist_ok=True)

        for file in uploaded_files:
            if file.filename:
                filename = secure_filename(file.filename)
                file.save(os.path.join(upload_path, filename))
                filenames.append(filename)

        # Update the request with file info
        update_request_files(req_id, filenames)

    return render_template('success.html', request_id=req_id)

@app.route('/expert')
def expert_index():
    if session.get('expert_logged_in'):
        return redirect(url_for('expert_dashboard'))
    return redirect(url_for('expert_login'))

@app.route('/expert/login', methods=['GET', 'POST'])
def expert_login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == EXPERT_PASSWORD:
            session['expert_logged_in'] = True
            return redirect(url_for('expert_dashboard'))
        else:
            flash('Incorrect password.', 'danger')
    return render_template('expert_login.html')

@app.route('/expert/logout')
def expert_logout():
    session.pop('expert_logged_in', None)
    return redirect(url_for('expert_login'))

@app.route('/expert/dashboard')
def expert_dashboard():
    if not session.get('expert_logged_in'):
        return redirect(url_for('expert_login'))

    all_requests = get_all_requests()
    pending_requests = {k: v for k, v in all_requests.items() if v.get('status') == 'pending'}

    return render_template('expert_dashboard.html', pending_requests=pending_requests)

@app.route('/expert/reply/<req_id>', methods=['POST'])
def expert_reply(req_id):
    if not session.get('expert_logged_in'):
        return redirect(url_for('expert_login'))

    diagnosis = request.form.get('diagnosis')
    if diagnosis:
        success = update_request_response(req_id, diagnosis)
        if success:
            flash(f'Diagnosis sent for request {req_id}!', 'success')
        else:
            flash('Failed to update request.', 'danger')
    else:
        flash('Please enter a diagnosis.', 'warning')

    return redirect(url_for('expert_dashboard'))

@app.route('/status', methods=['GET', 'POST'])
def check_status():
    req_data = None
    check_id = None
    not_found = False

    if request.method == 'POST':
        check_id = request.form.get('check_id', '').strip()
        if check_id:
            req_data = get_request(check_id)
            if not req_data:
                not_found = True

    return render_template('status.html', req_data=req_data, check_id=check_id, not_found=not_found)

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'False') == 'True'
    app.run(debug=debug_mode, port=5000)
