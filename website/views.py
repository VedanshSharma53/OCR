from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
from paddleocr import PaddleOCR,draw_ocr
from IPython.display import display
import os
from datetime import datetime
from werkzeug.utils import secure_filename

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html",user = current_user)

@views.route('/redirect', methods=['post'])
def redirect_to_new_page():
    selected_option = request.form['options']
    if selected_option == 'option1':
        return render_template('aadhaar.html',user = current_user)
    elif selected_option == 'option2':
        return render_template('pan.html',user = current_user)
    elif selected_option == 'option3':
        return render_template('passsport.html',user = current_user)
    else:
        pass


@login_required
@views.route('/aadhar', methods=['post'])
def aadhaar_details():
    if request.method == 'POST': 
        file = request.files['filename']
        filename = datetime.now().strftime('%Y%m%d%H%M%S') + '_' + secure_filename(file.filename)
        filename = os.path.join(file.filename)
        file.save(filename)
       
        ocr = PaddleOCR(lang='en')
        result = ocr.ocr(filename, cls=False)
        for idx in range(len(result)):
            res = result[idx]
            for line in res:
                print(line)

        from PIL import Image
        result = result[0]
        image = Image.open(filename).convert('RGB')
        boxes = [line[0] for line in result]
        txts = [line[1][0] for line in result]
        scores = [line[1][1] for line in result]
        newtext = []
        newcoord = []

        for i in range(len(txts)):
            if(scores[i] >= 0.7):
                newtext.append(txts[i])
                newcoord.append(boxes[i][0])
                
        start_index = 0
        end_index = 0
        name_flag = False
        state_flag = False
        for i in range(len(newtext)):
            if("Enrol" in newtext[i]):
                start_index = i+1
                name_flag = True
            if(newtext[i].isdigit() and len(newtext[i])>=10):
                j = i-1
                while(len(newtext[j])<6):
                    j-=1
                end_index = j
                state_flag = True
            if(state_flag and name_flag):
                break
            
        llimit = newcoord[end_index][0]-10
        rlimit = newcoord[end_index][0]+10
        temptxt = []

        for i in range(len(newtext)):
            if(i<start_index):
                continue
            if(i>end_index):
                break
            if(newcoord[i][0]>=llimit and newcoord[i][0]<=rlimit):
                temptxt.append(newtext[i])
                
        def aadhaarNumber_Extractor(text):
            list = text
            aadhaarnum = ""
            for word in list:
                word = word.replace(" ","")
                if(len(word) == 12 and word.isdigit() == True):
                    aadhaarnum+= word
                    break
            return aadhaarnum
        
        def DOB_Extractor(text):
            list = text
            date = ""
            flag = False
            for word in list:
                if(word == ''):
                    continue
                if "DOB" in word:
                    date += word[word.find("DOB")+3:len(word)]
                    break
                elif "DB" in word or "DO" in word:
                    date += word[word.find("D")+2:len(word)]
                    break
            return date
        
        def gender_Extractor(text):
            list = text
            gender = ""
            for word in list:
                if(word == ''):
                    continue
                if "Male" in word:
                    gender+= "Male"
                elif "Female" in word:
                    gender += "Female"
                elif "Transgender" in word:
                    gender += "Transgender"
                elif "MALE" in word :
                    gender += "MALE"
                elif "FEMALE" in word:
                    gender += "FEMALE"
                elif "TRANSGENDER" in word:
                    gender += "TRANSGENDER"
                if(gender != ""):
                    break
            return gender
        
        aadhaarnumber = aadhaarNumber_Extractor(newtext)
        DOB = DOB_Extractor(newtext)
        gender = gender_Extractor(newtext)
        name = ""
        address = ""
        state = ""
        city = ""
        flag = False
        for word in temptxt:
            if(word == "To" or word == "To," or word == "To " or word == "TO." or word == "TO," or word == "TO "):
                continue
            if((word == name) or (name != "" and (name[0:name.index(" ")] in word))):
                continue
            if(name == ""):
                name = word
                continue
            if(address == ""):
                address+= word
                flag = True
                continue
            if(flag):
                address+=', '
                address+=word
        pincode = address[len(address)-6:]
                
        finaltxt = {}
        finaltxt["name"] = name
        finaltxt["DOB"] = DOB
        finaltxt["gender"] = gender
        finaltxt["aadhaarnumber"] = aadhaarnumber
        finaltxt["state"] = state
        finaltxt["city"] = city
        finaltxt["pincode"] = pincode
        finaltxt["address"] = address
        # print(name)
        # print(address)

        new_note = Note(data=name, user_id=current_user.id)  #providing the schema for the note 
        new_note1 = Note(data=DOB, user_id=current_user.id)  #providing the schema for the note 
        new_note2 = Note(data=gender, user_id=current_user.id)  #providing the schema for the note 
        new_note3 = Note(data=aadhaarnumber, user_id=current_user.id)  #providing the schema for the note 
        new_note4 = Note(data=state, user_id=current_user.id)  #providing the schema for the note 
        new_note5 = Note(data=city, user_id=current_user.id)  #providing the schema for the note 
        new_note6 = Note(data=pincode, user_id=current_user.id)  #providing the schema for the note 
        new_note7 = Note(data=address, user_id=current_user.id)  #providing the schema for the note 
        db.session.add(new_note) #adding the note to the database 
        db.session.add(new_note1) #adding the note to the database 
        db.session.add(new_note2) #adding the note to the database 
        db.session.add(new_note3) #adding the note to the database 
        db.session.add(new_note4) #adding the note to the database 
        db.session.add(new_note5) #adding the note to the database 
        db.session.add(new_note6) #adding the note to the database 
        db.session.add(new_note7) #adding the note to the database 
        
        # my_data = MyTable(**finaltxt)
        # db.session.add(my_data)
        db.session.commit()
        flash('Note added!', category='success')
        os.remove(filename)
        # data = session.query(MyTable).first()
    return render_template("aadhaar.html", user=current_user)
    # return render_template("home.html", name = data.name,)
    
    
@views.route('/aadhar_details()', methods=['GET', 'POST'])


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})




#===============================================================================================================================


