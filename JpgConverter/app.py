from flask import Flask, request, send_file
from flask import url_for;

import os;
from os import system;

import  uuid;

app = Flask(__name__)

def convert_to_jpg(input_file):
    
    _pdf = os.path.splitext(input_file)[0]+'.pdf';
    _jpg = os.path.splitext(input_file)[0]+'.jpg';

    system(f"libreoffice --headless --convert-to pdf {input_file} --outdir ./tmp/");
    system(f"convert -density 300 {_pdf} {_jpg}");
    
    system(f"rm {input_file}");
    return _pdf,_jpg;

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    file.save(file.filename);
    
    _pdf,_jpg = convert_to_jpg(file.filename);
    
    return send_file(_jpg, mimetype='image/jpg');

@app.route('/upload_certificate',methods=['POST'])
def upload_certificate():
    file = request.files['file'];
    saved_file_name = os.path.join('.',
                                   'static',
                                   str(uuid.uuid4())+'.jpg');
    file.save(saved_file_name);

    return url_for('show_certificate',
                   user=os.path.splitext(
                       os.path.basename(saved_file_name))[0],_external=True);

@app.route('/download_certificate/<user>',methods=['GET'])
def download_certificate(user):
    file_name = user+'.jpg';
    abs_path = os.path.join('.','static',file_name);
    return send_file(abs_path,mimetype="image/jpg")

@app.route('/get_certificate/<user>',methods=['GET'])
def get_certificate(user):
    rel_path = os.path.join('.','static',f'{user}.jpg');
    return send_file(rel_path,mimetype="image/jpg");


@app.route('/show_certificate/<user>',methods=['GET'])
def show_certificate(user):
    file_name = user+'.jpg';
    abs_path = url_for('get_certificate',user=user,_external=True);

    return f"""

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
            background-color: #f4f4f4;
        }}

        .rounded-image-container {{
            overflow: hidden;
            border-radius: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }}

        .rounded-image {{
            display: block;
            width: 100%;
            height: auto;
            border-radius: 20px;
        }}
    </style>
    <title>Rounded Image</title>
</head>
<body>
    <div class="rounded-image-container">
        <img class="rounded-image" src="{abs_path}" alt="Aesthetic Image">
    </div>
</body>
</html>
""";


if __name__ == '__main__':
    app.run(debug=True);
