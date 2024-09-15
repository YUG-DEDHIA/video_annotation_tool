from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'  # Set folder for video uploads

# Store annotations globally for simplicity
annotations = []

# Route for the homepage
@app.route('/')
def index():
    video = request.args.get('video')  # Get the video filename if it exists
    search_results = request.args.get('search_results')  # Get search results if they exist
    return render_template('index.html', video=video, annotations=annotations, search_results=search_results)

# Route to handle video uploads
@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return 'No file part'
    file = request.files['video']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = secure_filename(file.filename)  # Secure the filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  # Save the video
        return redirect(url_for('index', video=filename))  # Pass video name via url_for

# Route to handle annotations
@app.route('/annotate', methods=['POST'])
def annotate():
    timestamp = request.form['timestamp']
    label = request.form['label']
    video = request.form['video']
    
    # Save the annotation along with the video name for future reference
    annotations.append({'timestamp': timestamp, 'label': label, 'video': video})
    print(f"Added annotation: {label} at {timestamp} seconds for video {video}")
    
    return redirect(url_for('index', video=video))  # Redirect back to the homepage with the same video

# Route to handle search functionality
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('search')  # Get the search query
    search_results = []

    # Filter annotations based on the search query
    for annotation in annotations:
        if query.lower() in annotation['label'].lower():
            search_results.append(annotation)

    return render_template('index.html', search_results=search_results)  # Render the results

if __name__ == "__main__":
    # Ensure the uploads folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    app.run(debug=True)
