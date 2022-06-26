from flask import Flask
from flask import jsonify,request, send_file

app = Flask(__name__)
# from models.experimental import attempt_load
# import cv2
# import torch
# import torch.backends.cudnn as cudnn
from numpy import random
import os

UPLOAD_FOLDER = "E:\\Bob\\deploy\\uploaded_img"
occ=0
emp=0
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/process/', methods=['GET', 'POST'])
def welcome():
    if request.method == 'POST':
        file = request.files['file']
    filename=file.filename    
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    filepath=os.path.join(app.config['UPLOAD_FOLDER'], filename)
    print(filepath)
    os.system("python inference.py --weights best.pt --conf 0.4 --line-thickness 2 --hide-conf --source "+filepath)
    return(send_file("./runs/detect/exp/"+filename))

@app.route('/number/', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        file = request.files['file']
    filename=file.filename    
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    filepath=os.path.join(app.config['UPLOAD_FOLDER'], filename)
    print(filepath)
    os.system("python inference.py --save-txt --weights best.pt --conf 0.4 --line-thickness 2 --hide-conf --source "+filepath )
    new_filename=filename[:-3]+'txt'
    occ=0
    emp=0
    with open("./runs/detect/exp/labels/"+new_filename, 'r') as fp:
        x = fp.readlines()
        n = len(x)
        for line in x: 
            if line[0] == '1':
                occ+=1
            elif line[0] =='0':
                emp+=1 
        print('Total parking spaces:', n)
        print('Occupied parking spaces:', occ)
        print('Empty parking spaces:', emp) 
    result={
        'Total Parking Spaces: ':n,
        'Occupied Parking Spaces: ':occ,
        'Empty Parking Spaces: ':emp
    }
    return(jsonify(result))

@app.route('/', methods=['GET'])
def test():
    return('hi')
    
if __name__ == '__main__':
    occ=0
    emp=0
    app.run(host='0.0.0.0')