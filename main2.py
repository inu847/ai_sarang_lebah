from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    f = request.files['file']

    if not f:
        return 'No file part'

    f.save(f.filename)

    data = {'filename': f.filename, 'status': 'success', 'message': 'File uploaded successfully'}
    return jsonify(data)

if __name__ == '__main__':
    app.run()``