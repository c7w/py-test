import utils.getMcbbsScore as score
import utils.MCBBSScoreRank as rank

from flask_apscheduler import APScheduler;
from flask import Flask, Response, escape,request,render_template
from requests_html import HTMLSession

class Config(object):
    SCHEDULER_API_ENABLED = True

app = Flask(__name__)

app.config.from_object(Config())
scheduler = APScheduler();
scheduler.init_app(app)
scheduler.start()

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/get-mcbbs-score',methods=['GET'])
@app.route('/get-mcbbs-score/<int:uid>')
def get_mcbbs_score(uid=None):
    #快捷方式 直接通过UID直接获取
    if uid:
        if uid >= 1:
            #Do Something Here
            profile = score.getScoreFromUid(uid)
            return render_template('./get-mcbbs-score/score.html',list=profile)
        else:
            return render_template('./get-mcbbs-score/error.html',list = ['uid',uid])
    
    #处理表单 获取数据
    if request.method=="GET":
        source = request.args.get('source')
        val = request.args.get('val')
        
        #返回成功获取的数据
        if source and val:
            if source == 'uid':
                try:
                    val = int(val)
                except:
                    return render_template('./get-mcbbs-score/error.html',list = [source,val])
                profile = score.getScoreFromUid(val)
            else:
                profile = score.getScoreFromUsername(val)
            return render_template('./get-mcbbs-score/score.html',list=profile)

    #尝试处理不带参数的 GET 请求
    getUid = request.args.get('uid')
    getName = request.args.get('username')
    if getUid:
        try:
            uid = int(getUid)
        except:
            return render_template('./get-mcbbs-score/error.html',list = [source,getUid])
        profile = score.getScoreFromUid(getUid)
        return render_template('./get-mcbbs-score/score.html',list=profile)
    if getName:
        profile = score.getScoreFromUsername(getName)
        return render_template('./get-mcbbs-score/score.html',list=profile)
    
    #没有输入账号信息
    #进入提醒页面 提醒输入数据
    return render_template('./get-mcbbs-score/index.html')

@app.route('/mcbbs-rank')
def mcbbs_rank():
    result = rank.get()
    return render_template('./mcbbs-score-rank/result.html' , content = result)
    

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    list = {
        1: name,
        2: 2333
            }
    return render_template('index.html' , list = list)

rank.startJob(app)

if __name__ == '__main__':
    app.run()