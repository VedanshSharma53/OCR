from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from paddleocr import PaddleOCR,draw_ocr
from IPython.display import display

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    # from .views2 import views2
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    # app.register_blueprint(views2, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import MyTable,User,Note
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
        
        

# def extract():
#     from .extractor import extractor
#     ocr = PaddleOCR(lang='en') # need to run only once to download and load model into memory
#     img_path = r"C:\Users\user\Desktop\full len aadhaar 1.jpg"
#     # img_path = r"C:\Users\VIGNESH SHARMA\Desktop\digilocker format AADHAR.jpg"
#     # img_path = r"C:\Users\VIGNESH SHARMA\Desktop\APPLICATION DOCUMENTS\AADHAAR CARD.jpg"
#     result = ocr.ocr(img_path, cls=False)
#     for idx in range(len(result)):
#         res = result[idx]
#         for line in res:
#             print(line)

#     # draw result
#     from PIL import Image
#     result = result[0]
#     image = Image.open(img_path).convert('RGB')
#     boxes = [line[0] for line in result]
#     txts = [line[1][0] for line in result]
#     scores = [line[1][1] for line in result]
#     # im_show = draw_ocr(image, boxes, txts, scores, font_path=r"C:\Users\VIGNESH SHARMA\Desktop\simfang.ttf")
#     # im_show = Image.fromarray(im_show)

#     # result_path = 'result.jpg'
#     # im_show.save(result_path)
#     # result = Image.open(result_path)
#     # display(result)
#     # result.show()


#     newtext = []
#     newcoord = []

#     for i in range(len(txts)):
#         if(scores[i] >= 0.7):
#             newtext.append(txts[i])
#             newcoord.append(boxes[i][0])
            
            
#     start_index = 0
#     end_index = 0
#     name_flag = False
#     state_flag = False
#     for i in range(len(newtext)):
#         if("Enrol" in newtext[i]):
#             start_index = i+1
#             name_flag = True
#         if(newtext[i].isdigit()):
#             end_index = i-1
#             state_flag = True
#         if(state_flag and name_flag):
#             break


#     llimit = newcoord[end_index][0]-10
#     rlimit = newcoord[end_index][0]+10
#     temptxt = []

#     for i in range(len(newtext)):
#         if(i<start_index):
#             continue
#         if(i>end_index):
#             break
#         if(newcoord[i][0]>=llimit and newcoord[i][0]<=rlimit):
#             temptxt.append(newtext[i])
            
            
#     name = ""
#     address = ""
#     state = ""
#     # pincode = temptxt[len(temptxt)-1][len(temptxt)-6:
#     flag = False
#     for word in temptxt:
#         if(word == "To" or word == "To," or word == "To " or word == "TO." or word == "TO," or word == "TO "):
#             continue
#         if((word == name) or (name != "" and (name[0:name.index(" ")] in word))):
#             continue
#         if(name == ""):
#             name = word
#             continue
#         if(address == ""):
#             address+= word
#             flag = True
#             continue
#         if(flag):
#             address+=', '
#             address+=word
#     print(name)
#     print(address)
