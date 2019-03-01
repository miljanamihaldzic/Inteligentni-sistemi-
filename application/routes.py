from flask import Flask, render_template,redirect,flash,url_for,session,logging, request,jsonify
from application import app
from application.forms.form import MainForm
import cv2 , os, json
import numpy as np
from werkzeug.utils import secure_filename
from flask_cors import cross_origin
import secrets



@app.route('/', methods = ['GET','POST'])
def index():
    form= MainForm(request.form)
    return render_template('index.html',form = form,image_name = "")

@app.route('/upload', methods=[ 'POST'])
@cross_origin()
def upload():
    form= MainForm(request.form)
    
    target_folder = os.path.join(app.root_path,'static/pictures')
    for upload in request.files.getlist("file"):
        filename = 'original.jpg'
        destination = "/".join([target_folder, filename])
        upload.save(destination)
    return render_template("index.html", image_name=filename,form = form)

@app.route('/geometry', methods = ['POST'])
def geometry():
    #extraction info from json
    json_obj = request.get_json(force = True)
    shape_sides = json_obj['shape']
    surface = json_obj['surface']
    color = json_obj['color']
    
    #getting original image
    big_img = cv2.imread(app.root_path + '/static/pictures/original.jpg', 1)
    
    #convert from RGB to HSV
    org_img_hsv = cv2.cvtColor(big_img, cv2.COLOR_BGR2HSV)

    #defining color boundaries in HSV
    if color == "G":
        lower_color = np.array([35,30,0])
        upper_color = np.array([104,255,255])
    if color == "R":
        lower_color = np.array([0,30,0])
        upper_color = np.array([30,255,255])
        lower_color1 = np.array([150,30,0])
        upper_color1 = np.array([180,255,255])
    if color == "B":
        lower_color = np.array([109,30,0])
        upper_color = np.array([169,255,255])

    #creating mask according to specific color boundaries
    mask = cv2.inRange(org_img_hsv, lower_color,upper_color)
    #
    contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #spacial case if color is red because of red's non-continues nature
    if color == "R":
        mask1 = cv2.inRange(org_img_hsv, lower_color1,upper_color1)
        contours1, hierarchy = cv2.findContours(mask1.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours1:
            if cv2.isContourConvex(cnt):
                area=cv2.contourArea(cnt)
        
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt,0.04*peri,True)
        
                if (area>float(surface) and len(approx)==int(shape_sides)):
                    cv2.drawContours(big_img,[cnt],-1,(0,0,0),4)        

    for cnt in contours:
        if cv2.isContourConvex(cnt):
            area=cv2.contourArea(cnt)

            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt,0.04*peri,True)

            if (area>float(surface) and len(approx)==int(shape_sides)):
                cv2.drawContours(big_img,[cnt],-1,(0,0,0),2)

    randon_hex = secrets.token_hex(8)
    f_ext = '.jpg'
    picture_fn = randon_hex + f_ext
    
    path = os.path.join(app.root_path,'static/pictures',picture_fn)
    cv2.imwrite(path,big_img)
    rel_path = '/static/pictures/' + picture_fn
    return jsonify({'result' : 'success', 'image_path' : rel_path })
   


#@app.route('/brightness_and_contrast', methods = ['POST'])
#def brightness_and_contrast():
#    a = request.get_json(force = True)
#    brightness = a['brightness'] #beta
#    contrast = a['contrast'] #alfa
#    brightness = (float(brightness)-100.0)*2
#    contrast = float(contrast) / 33.3
#    
#    img = cv2.imread(app.root_path + '/static/pictures/original.jpg', 1)
#    new_image = np.zeros(big_img.shape, big_img.dtype)
#    
#    new_image = cv2.convertScaleAbs(big_img, alpha=float(contrast), beta=float(brightness))
#
#    randon_hex = secrets.token_hex(8)
#    f_ext = '.jpg'
#    picture_fn = randon_hex + f_ext
#   
#    path = os.path.join(app.root_path,'static/pictures',picture_fn)
#    cv2.imwrite(path,new_image)
#    rel_path = '/static/pictures/' + picture_fn
#    return jsonify({'result' : 'success', 'image_path' : rel_path })


@app.route('/brightness_and_contrast', methods = ['POST'])
def brightness_and_contrast():
    a = request.get_json(force = True)
    brightness = a['brightness'] 
    contrast = a['contrast'] 
    brightness = (float(brightness)*127/50)-127
    contrast = (float(contrast)*64/50)-64

    big_img = cv2.imread(app.root_path + '/static/pictures/original.jpg', 1)
    
    if brightness > 0:
        shadow = brightness
        highlight = 255
    else:
        shadow = 0
        highlight = 255 + brightness
    alpha_b = (highlight - shadow)/255
    gamma_b = shadow

    new_image = cv2.addWeighted(big_img, alpha_b, big_img, 0, gamma_b)
    
    f = 131*(contrast + 127)/(127*(131-contrast))
    alpha_c = f
    gamma_c = 127*(1-f)

    new_image = cv2.addWeighted(new_image, alpha_c, new_image, 0, gamma_c)

    randon_hex = secrets.token_hex(8)
    f_ext = '.jpg'
    picture_fn = randon_hex + f_ext
    
    path = os.path.join(app.root_path,'static/pictures',picture_fn)
    cv2.imwrite(path,new_image)
    rel_path = '/static/pictures/' + picture_fn
    return jsonify({'result' : 'success', 'image_path' : rel_path })



@app.route('/edge', methods = ['POST'])
def edge():
    img = cv2.imread(app.root_path + '/static/pictures/original.jpg', 1)
    
    edges = cv2.Canny(img,100,200)

    randon_hex = secrets.token_hex(8)
    f_ext = '.jpg'
    picture_fn = randon_hex + f_ext
    
    picture_path = os.path.join(app.root_path,'static/pictures',picture_fn)

    cv2.imwrite(picture_path,edges)
    
    rel_path = '/static/pictures/' + picture_fn
    return jsonify({'result' : 'success', 'image_path' : rel_path })
  