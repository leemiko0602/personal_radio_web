from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.http import HttpResponse
from personalRecommend.models import Users,UserRecommendPlayList,RbcProgram,UserProgramCollect,UserProgramScore
from datetime import datetime,date
import time
import suds.client
# url='http://222.31.101.40:8988/WS_Server/DataTransfer?wsdl' #已发布的接口
# client=suds.client.Client(url)
# service = client.service
import json

#用户认证
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib import auth
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core import serializers
# Create your views here.
@login_required
def personalHome(request):
    #微博用户
    request.session['preURL']='personalHome'
    if (request.user.is_authenticated() and request.user.is_active) :
        # uname=request.user.username
        # myuser = Users.objects.get(name=uname)
        # id=myuser.id
        recommend_lists=UserRecommendPlayList.objects.filter(user_id=request.user.id)
        lists=list()
        Scored=0              #未评分
        Collected=0            #未收藏
        for recommend_list in recommend_lists:
            programID=recommend_list.program_id
            program=RbcProgram.objects.get(id=programID)
            fileName=program.file_name
            radioID=program.radio_id
            URL="http://101.201.81.34:8089/rbc_fm/"+str(radioID)+"/"+fileName
            try:
                userScore=UserProgramScore.objects.filter(user_id=request.user.id).get(program_id = programID)
                Scored=userScore.score
            except UserProgramScore.DoesNotExist:
                Scored=0
            try:
                user_collect = UserProgramCollect.objects.filter(user_id=request.user.id).get(program_id =programID)
                Collected=1
            except UserProgramCollect.DoesNotExist:
                Collected=0

            recommend_program={}
            recommend_program['recommend_list']=recommend_list
            recommend_program['program']=program
            recommend_program['score']=Scored
            recommend_program['collect']=Collected
            recommend_program['url']= URL
            lists.append(recommend_program)

        return render_to_response('personalRecommend/personalHome.html',{'lists': lists,'uname':request.user.username})
    # else:
    #     errorlog="请先登录，才能完成个性化推荐"
    #     return render_to_response('home.html',{'errorlog':errorlog})
    # error="请先登录，才能完成个性化推荐"
    # return render_to_response('home.html',{'error':error})

#节目收藏
def collectProgram(request):
    if (request.user.is_authenticated() and request.user.is_active) :
        program_id = request.POST['program_id']
        userID=request.user.id
        try :
            #收藏已存在，取消收藏
            user_collect = UserProgramCollect.objects.filter(user_id = userID).get(program_id = program_id)
            user_collect.delete()
            #传输用户行为数据
            transdata=getUser_exolicit_behavior(userID,'',program_id,'1','3','0','')
            f=open("cms123.txt",'a')
            f.write(transdata)
            transUserBehaviorData(transdata)
            return HttpResponse(1)
        except UserProgramCollect.DoesNotExist:
            #增加收藏
            UserProgramCollect.objects.create(user_id=userID,program_id=program_id)
            #传输用户行为数据
            transdata=getUser_exolicit_behavior(userID,'',program_id,'1','3','1','')
            f=open("cms123.txt",'a')
            f.write(transdata)
            transUserBehaviorData(transdata)
            return HttpResponse(0)
#节目评分
def programScore(request):
    if (request.user.is_authenticated() and request.user.is_active) :
        score=request.POST['score']
        program_id = request.POST['program_id']
        userID=request.user.id
        try :
            #用户已评分，更新评分
            user_score = UserProgramScore.objects.filter(user_id = userID).get(program_id = program_id)
            user_score.score=score
            user_score.save()
            #传输用户行为数据
            transdata=getUser_exolicit_behavior(userID,'',program_id,'1','4',score,'')
            f=open("cms123.txt",'a')
            f.write(transdata)
            transUserBehaviorData(transdata)
            return HttpResponse(4)
        except UserProgramScore.DoesNotExist:
            #用户评分
            UserProgramScore.objects.create(user_id=userID,program_id=program_id,score=score)
            #传输用户行为数据
            transdata=getUser_exolicit_behavior(userID,'',program_id,'1','4',score,'')
            f=open("cms123.txt",'a')
            f.write(transdata)
            transUserBehaviorData(transdata)
            return HttpResponse(4)


def getUser_exolicit_behavior(userID,radioID,programID,programType,behaviorType,behaviorContent,No):
    user_time= round(time.time())  #用户终端时间
    user_id=userID
    loginType=Users.objects.get(id=user_id).login_type  #0：用户 1：微博
    user_ip=''    #暂时为空
    radio_id=radioID
    program_id=programID
    program_type=programType  #0：交通广播节目 1：rbc广播节目2：音乐节目
    behavior_type=behaviorType ##播放为0，暂停为1，搜索为2，节目收藏为3，节目评分为4，分享为5
    behavior_content=behaviorContent #播放,暂停,一键分享为空，搜索为关键字，收藏：0：取消收藏/1：收藏，评分：具体分数1-5
    No_tag=No #播放，暂停为登录时间戳+播放时间戳，其他为空
    dev_name=''  #暂时为空
    os_name=''   #暂时为空
    data=str(user_time)+"\t"+str(user_id)+"\t"+str(loginType)+"\t"+user_ip+"\t"+str(radio_id)+"\t"+str(program_id)+"\t"+str(program_type)+"\t"+str(behavior_type)+"\t"+str(behavior_content)+"\t"+str(No_tag)+"\t"+dev_name+"\t"+os_name+"\n"
    return data

pre_program={'pragramID':'','noTag':'','playtag':'1'} #上一条节目的状态 0表示播放 1表示暂停
def getUserPlayPause(request):
    print('startpre_programplaytag'+str(pre_program['playtag']))
    if (request.user.is_authenticated() and request.user.is_active) :
        userID=request.user.id
        login_time=round(time.mktime((request.user.last_login).timetuple()))  #转化为时间戳
        program_id = request.POST['program_id']
        play_tag=request.POST['playtag']
        new_start=request.POST['newstart'] #1表示是新的节目 0表示是老节目
        if new_start=='1':   #肯定是处于播放状态，新的click事件
            if pre_program['playtag']=='1': #上条节目已经是暂停状态，不需要传上条节目的暂停行为
                #计算新的notag表示，登录时间戳和播放事件戳
                play_time=round(time.time())
                notag=str(login_time)+'_'+str(play_time)
                #传输用户行为
                transdata=getUser_exolicit_behavior(userID,'',program_id,1,0,'',notag)
                f=open("cms123.txt",'a')
                f.write(transdata)
                transUserBehaviorData(transdata)
                #记录这条行为
                pre_program['pragramID']=program_id
                pre_program['noTag']=notag
                pre_program['playtag']=0  #更改为播放状态
            else: #上条节目是播放状态，需要传输上条节目的暂停行为
                #传输上条节目的暂停
                transdata=getUser_exolicit_behavior(userID,'',pre_program['pragramID'],1,1,'',pre_program['noTag'])
                f=open("cms123.txt",'a')
                f.write(transdata)
                transUserBehaviorData(transdata)
                #传输这条节目的新播放
                #计算新的notag表示，登录时间戳和播放事件戳
                play_time=round(time.time())
                notag=str(login_time)+'_'+str(play_time)
                transdata=getUser_exolicit_behavior(userID,'',program_id,1,0,'',notag)
                f=open("cms123.txt",'a')
                f.write(transdata)
                transUserBehaviorData(transdata)
                #记录这条行为
                pre_program['pragramID']=program_id
                pre_program['noTag']=notag
                pre_program['playtag']=0  #更改为播放状态
        else: #不是新节目，对底部按钮的播放或暂停,不管是播放还是暂停，都要传输该行为，并且不需要计算notag
            transdata=getUser_exolicit_behavior(userID,'',program_id,1,play_tag,'',pre_program['noTag'])
            f=open("cms123.txt",'a')
            f.write(transdata)
            transUserBehaviorData(transdata)
            #记录这条行为
            pre_program['playtag']=play_tag
            print('overpre_programplaytag'+str(pre_program['playtag']))
        return HttpResponse(5)


#http://127.0.0.1:8000/usercollectAPI/?userID=138  输入用户id即可
# def usercollectAPI(request):
#     if 'userID' in request.GET:
#         userID=request.GET['userID']
#         userCollectList=serializers.serialize("json",UserProgramCollect.objects.filter(user_id = userID))
#         return HttpResponse(userCollectList, content_type='application/json; charset=utf-8')
#http://127.0.0.1:8000/usercollectAPI2/138/  输入用户id即可
def usercollectAPI(request):
    if 'userID' in request.GET:
        userID=request.GET['userID']
        program_id = []  # 存放节目id
        program = []  # 存放节目的信息，名字和时长等等
        program_collect = UserProgramCollect.objects.filter(user_id=userID)
        for s in program_collect:
            program_id.append(s.program_id)
        for i in range(0, len(program_id)):
            program.append((RbcProgram.objects.get(id=program_id[i])))
        userCollectList = serializers.serialize("json", program)
        return HttpResponse(userCollectList, content_type='application/json; charset=utf-8')


#用户推荐节目接口 http://127.0.0.1:8000/personalRecommendAPI/?userID=138
#判断用户是否收藏和评分，待修改
def personalRecommendAPI(request):
    userID=request.GET['userID']
    lists = list()
    # Scored = 0  # 未评分
    # Collected = 0  # 未收藏
    recommend_lists=UserRecommendPlayList.objects.filter(user_id=userID)
    for recommend_list in recommend_lists:
        programID = recommend_list.program_id
        program = RbcProgram.objects.get(id=programID)
        try:
            userScore = UserProgramScore.objects.filter(user_id=userID).get(program_id=programID)
            Scored = userScore.score
        except UserProgramScore.DoesNotExist:
            Scored = 0
        try:
          user_collect = UserProgramCollect.objects.filter(user_id=userID).get(program_id=programID)
          Collected = 1
        except UserProgramCollect.DoesNotExist:
          Collected = 0
        recommend_program = {}
        recommend_program['programName'] =program.block_name
        recommend_program['programID'] = userScore.program_id
        recommend_program['play_link']=program.rbc_play_link#播放地址
        recommend_program['score'] = Scored
        recommend_program['collect'] = Collected
        lists.append(recommend_program)
        recommendlist=json.dumps(lists)
    return HttpResponse(recommendlist)

# http://127.0.0.1:8000/programCollectAPI/?user_id=20&program_id=17&dir_type=1
# 用户收藏节目ID接口,将收藏接口存储
def programCollectAPI(request):
    if 'user_id' and 'program_id' and 'dir_type' in request.GET:
        _user_id = request.GET['user_id']
        _program_id = request.GET['program_id']
        _dir_type = request.GET["dir_type"]

        UserProgramCollect.objects.create(user_id=_user_id,program_id=_program_id,dir_type = _dir_type)
        program_collection = serializers.serialize("json",UserProgramCollect.objects.filter(user_id = _user_id)
                                                   .filter(program_id = _program_id).filter(dir_type = _dir_type))
        return HttpResponse(program_collection, content_type='application/json; charset=utf-8')



def transUserBehaviorData(data):
    url='http://222.31.101.40:8988/WS_Server/DataTransfer?wsdl' #已发布的接口
    try:
        client=suds.client.Client(url)
        service = client.service
        result=service.userBehaviorLogTrans(data)
        print(result)
        return result
    except OSError:
        result=1
        print ('result'+str(result))
        return result








