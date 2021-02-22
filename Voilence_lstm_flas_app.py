
from flask import Flask , request
import jsonify
from Model import *


app = Flask("main-webapi")
graph = tf.compat.v1.get_default_graph()
@app.route('/api/fight/',methods= ['GET','POST'])
def main_fight(accuracyfight=0.91):
    res_mamon = {}
    
    vidl = request.form["link"]
    print(vidl,'\n')
    vid = video_mamonreader(cv2,vidl)
    
    datav = np.zeros((1, 30, 160, 160, 3), dtype=np.float)
    datav[0][:][:] = vid
    millis = int(round(time.time() * 1000))
    f , precent = pred_fight(model22,datav,acuracy=0.67)
    res_mamon = {'fight':f , 'precentegeoffight':str(precent)}
    millis2 = int(round(time.time() * 1000))
    res_mamon['processing_time'] =  str(millis2-millis)
    resnd = jsonify(res_mamon)
    resnd.status_code = 200
    return resnd

app.run(port=3091)