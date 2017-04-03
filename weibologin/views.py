from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from weibologin.models import Program,LiveRadioDictionary,LiveTelecastRadio,LiveRadioPlayList,Users,UserRecommendPlayList
from datetime import datetime,date
import time
from django.db import connection


#用户认证
from django.contrib import auth
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
from django.template.context import RequestContext
from django.core import serializers
#微博登录
from weibo import APIClient


# Create your views here.
#微博登录
URL='http://radio.cucplus.com'
APP_KEY = '1028043534'# 设置你申请的appkey
APP_SECRET = 'ecf27fb12a960424b9b3ff42c5639939'# 设置你申请的appkey对于的secret
CALLBACK_URL = URL+'/weiboLogcheck/'
#用户职业类型
liveJob_list= LiveRadioDictionary.objects.filter(type='job')
liveType_list= LiveRadioDictionary.objects.filter(type='type')
liveArea_list = LiveRadioDictionary.objects.filter(type='area')
# Create your views here.
#主页
def home(request):
    logout(request)
    return render_to_response('liveTelecast/liveType.html', {'liveType':liveType_list,'uname':request.user.username})
#登录
def log(request):
    return render_to_response('weibologin/login.html', {'current_time': datetime.now()})
#注册
def register(request):
    return render_to_response('weibologin/register.html', {'current_time': datetime.now()})

#退出
def userlogout(request):
    logout(request)
    return render_to_response('liveTelecast/liveType.html', {'liveType':liveType_list,'uname':request.user.username})
#用户信息字典列表

def userInformationlist(request):
    if request.user.is_authenticated():
        uname=request.user.username
        sex=""
        myuser = Users.objects.get(name=uname)
        if myuser.sex == 0 :
            sex = "男"
        else :
            sex = "女"
        Dictionary=LiveRadioDictionary.objects.get(id=myuser.occupation)
        occupation=Dictionary.name
        #口味测试未展示,由李利补充
        userInformation= {'uname':uname,'sex': sex, 'birth': myuser.birth,'occupation':occupation}
        return userInformation
    else :
        uname=""
        return uname
#展示个人信息
#@login_required
def personalInformation(request):
    #userInformation  = userInformationlist(request)
    request.session['preURL']='userInfo'

    return render_to_response('personalInformation/personalInformation.html',userInformationlist(request))

def personalTaste(request):
    #userInformation  = userInformationlist(request)
    #request.session['preURL']='userInfo'
    request.session['preURL']='userTaste'
    return render_to_response('personalInformation/personalTaste.html',userInformationlist(request))

#注册成功后，将用户名和密码存入数据库
def registersave(request):
    username=request.POST.get('userName','')
    password=request.POST.get('password','')
    passwordagain=request.POST.get('passwordAgain','')
    def is_chinese(uchar):
        """判断一个unicode是否是汉字"""
        if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
                return False
        else:
                return True
    U1=is_chinese(username)
    U2=is_chinese(password)
    U3=is_chinese(passwordagain)
    if not (username and password and passwordagain):
        error1="用户名/密码/重复密码不能为空"
        return render_to_response('weibologin/register.html', {'current_time': datetime.now(),'error':error1})
    elif not (username.isalnum() and password.isalnum() and passwordagain.isalnum() and U1 and U2 and U3):
        error4="用户名/密码/重复密码应为字母或数字"
        return render_to_response('weibologin/register.html', {'current_time': datetime.now(),'error':error4})

    elif (len(password)<8):
        error2="密码长度不能小于8"
        return render_to_response('weibologin/register.html', {'current_time': datetime.now(),'error':error2})
    elif not (password==passwordagain):
        error3="两次输入密码不一致"
        return render_to_response('weibologin/register.html', {'current_time': datetime.now(),'error':error3})

    else:
        try:

            existuser=Users.objects.filter(login_type='0').get(name=username)
            error4="用户名已存在，请重新输入"
            return render_to_response('weibologin/register.html', {'current_time': datetime.now(),'error':error4})
        except Users.DoesNotExist :
            #creatTime=time.strftime('%Y-%m-%d',time.localtime(time.time()))
            #User.objects.create(name=username,password =password, create_time=creatTime,login_type=0)
            Users.create_myUser(username,password)
            #验证用户名和密码
            user = authenticate(username=username,password= password)
            if user is not None:
                login(request, user)
                request.session['logintype']=0
                return render_to_response('weibologin/tasteTest.html',
                                      {'current_time': datetime.now(),'liveJob_list':liveJob_list,'liveType_list':liveType_list})
            else:
                return render_to_response('weibologin/register.html',{'error':'user is None'})


#当用户输完用户名和密码之后
def logincheck(request) :
    try:
        logPreURL=request.session['preURL']
    except KeyError:
        logPreURL=''

    username=request.POST.get('userName', '')
    password=request.POST.get('password', '')
    if not (username and password):# it works, just debug
        error1="用户名或密码输入为空"
        return render_to_response('weibologin/login.html', {'current_time': datetime.now(),'error':error1})
    else:
         #获取数据库里的用户列表（ login_type=0）
        try:
            existuser=Users.objects.filter(login_type='0').get(name=username)
            #request.session['id']=existuser.id
            if existuser.password==password:
                user= authenticate(username = username,password= password)
                if user is not None:
                    login(request, user)
                    #判断从哪个页面进入登录状态
                    if logPreURL=='collect':
                        logURL=request.session['URL']
                        return HttpResponseRedirect(logURL, {'current_time': datetime.now(),'uname':request.user.username})
                    elif logPreURL=='userInfo':

                        return HttpResponseRedirect('/personalInformation/', {'current_time': datetime.now(),'uname':request.user.username})
                    elif logPreURL=='userTaste':
                        return HttpResponseRedirect('/personalTaste/', {'current_time': datetime.now(),'uname':request.user.username})

                    else:
                        return HttpResponseRedirect('/personalRecommend/', {'current_time': datetime.now(),'uname':request.user.username})


            else:
                error3="密码错误，请重新输入"
                return render_to_response('weibologin/login.html', {'current_time': datetime.now(),'error':error3})
        except Users.DoesNotExist :
            error2="用户不存在，请重新输入"
            return render_to_response('weibologin/login.html', {'current_time': datetime.now(),'error':error2})

#口味测试，获得用户信息
def tasteTest(request):
    sex=request.POST.get('sex','')
    year=request.POST.get('year','')
    month=request.POST.get('month','')
    date=request.POST.get('date','')
    job=request.POST.get('job','')
    type_list=request.POST.getlist('type','')
    if not sex:
        error1="性别选项必填"
        return render_to_response('weibologin/tasteTest.html',
                                      {'current_time': datetime.now(),'liveJob_list':liveJob_list,'liveType_list':liveType_list,'error':error1})
    else:
        if sex=='male':
            sexValue=0
        elif sex=='famale':
            sexValue=1
        else:
            sexValue=2

    if not (year and month and date):
        error2="出生年月日必填"
        return render_to_response('weibologin/tasteTest.html',
                                      {'current_time': datetime.now(),'liveJob_list':liveJob_list,'liveType_list':liveType_list,'error':error2})
    else:
        birth=[]
        birth.append(year)
        birth.append(month)
        birth.append(date)
        birthjoin="-".join(birth)
    if not job:
        error3="职业必填"
        return render_to_response('weibologin/tasteTest.html',
                                      {'current_time': datetime.now(),'liveJob_list':liveJob_list,'liveType_list':liveType_list,'error':error3})
    if not type_list:
        error4="喜欢的节目类型必填"
        return render_to_response('weibologin/tasteTest.html',
                                      {'current_time': datetime.now(),'liveJob_list':liveJob_list,'liveType_list':liveType_list,'error':error4})


    username=request.user.username
    Users.objects.select_for_update().filter(name=username).update(sex=sexValue,birth =birthjoin,occupation=job,tastes=type_list)
    #调用存储过程，生成个性化节目单
    newUser= Users.objects.get(name=username)
    newUserID=newUser.id
    type_list_len=len(type_list)
    typeList=(',').join(type_list)  #转化为字符串
    cur = connection.cursor()
    #cur.callproc('generate_user_recommend_play_list',(newUserID,'35,36',2))  存储过程所需要的参数形式
    cur.callproc('generate_user_recommend_play_list',(newUserID,typeList,type_list_len))
    cur.close()
    #return render_to_response('liveTelecast/live.html', {'current_time': datetime.now(),'liveAreas':liveArea_list,'liveType':liveType_list})
    return render_to_response('home.html', {'current_time': datetime.now(),'uname':username})





#def register
#微博登录
# def log(request) :
#     return render_to_response('weibologin/login.html',{'current_time': datetime.now()})
def weiboLogin(request):
     # weibo模块的APIClient是进行授权、API操作的类，先定义一个该类对象，传入参数为APP_KEY, APP_SECRET, CALL_BACK
    client = APIClient(APP_KEY, APP_SECRET, CALLBACK_URL)
    # 获取该应用（APP_KEY是唯一的）提供给用户进行授权的url
    auth_url = client.get_authorize_url()
    # 打印出用户进行授权的url，将该url拷贝到浏览器中，服务器将会返回一个url，该url中包含一个code字段（如图1所示）
   # print ("auth_url : " + auth_url)
    return redirect(auth_url)
#微博授权登录之后，存储微博ID
def weiboLogcheck(request):
    code = request.GET.get('code', None)
    if code:
        client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
        r = client.request_access_token(code)
        access_token = r.access_token   # 返回的token，类似abc123xyz456
        expires_in = r.expires_in       # token过期的UNIX时间：http://zh.wikipedia.org/wiki/UNIX%E6%97%B6%E9%97%B4
        uid = r.uid
        # 在此可保存access token
        client.set_access_token(access_token, expires_in)
        weibo_res = client.get_user_time_line(0)
        text = weibo_res.statuses
        uname = text[0]['user']['name']


        try:
            exitUser=Users.objects.filter(login_type='1').get(weibo_id=uid)
            request.session['logintype']=1
            user = authenticate(username=uname,password=uid)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/personalRecommend/', {'current_time': datetime.now(),'uname':request.user.username})

        except Users.DoesNotExist :

            Users.create_weiboUser(uname,uid)
            user = authenticate(username=uname,password=uid)
            if user is not None:
                login(request, user)
                request.session['logintype']=1
                return render_to_response('weibologin/tasteTest.html',
                                      {'current_time': datetime.now(),'liveJob_list':liveJob_list,'liveType_list':liveType_list})


# 登录接口 http://127.0.0.1:8000/loginAPI/?username= &pwd=  输入用户名和密码
def loginAPI(request):
    if 'username' and 'pwd' in request.GET:
       _name=request.GET['username']
       _pwd=request.GET['pwd']
       user=Users.objects.get(name=_name)
       if(user.password==_pwd):
           user_info = serializers.serialize("json", Users.objects.filter(name=_name))
           return HttpResponse(user_info, content_type='application/json; charset=utf-8')

#注册接口http://127.0.0.1:8000/registerAPI/?username= &password=
def registerAPI(request):
    if'username'and'password' in request.GET:
      _username=request.GET['username']
      _password=request.GET['password']
      Users.create_myUser(_username,_password)
      user=authenticate(username=_username,password=_password)
      user_info = serializers.serialize("json", Users.objects.filter(name=_username))
      return HttpResponse(user_info, content_type='application/json; charset=utf-8')

#注册年龄性别提交接口http://127.0.0.1:8000/age_sexsubmitAPI/?user_id= &birth= &sex=
def age_sexsubmitAPI(request):
    if'user_id' and 'birth' and 'sex' in request.GET:
        _userid=request.GET['user_id']
        _birth=request.GET['birth']
        _sex=request.GET['sex']
        user=Users.objects.get(id=_userid)
        user.birth=_birth
        user.sex=_sex
        user.save()
        user_info = serializers.serialize("json",Users.objects.filter(id=_userid))
        return HttpResponse(user_info, content_type='application/json; charset=utf-8')

#用户兴趣提交接口http://127.0.0.1:8000/tastesubmitAPI/?user_id= &taste=
def tastesubmitAPI(request):
        if'user_id'and'taste' in request.GET:
           _userid=request.GET['user_id']
           _taste=request.GET['taste']
           user=Users.objects.get(id=_userid)
           user.tastes=_taste
           user.save()
           user_info = serializers.serialize("json", Users.objects.filter(id=_userid))
           return HttpResponse(user_info, content_type='application/json; cweibharset=utf-8')

#微博授权登录接口 http://127.0.0.1:8000/weiboLoginAPI/?weiboname= &weiboid=
def weiboLoginAPI(request):
    if'weiboname'and'weiboid' in request.GET:
        _weiboname=request.GET['weiboname']
        _weiboid=request.GET['weiboid']
        Users.create_weiboUser(_weiboname,_weiboid)
        user=authenticate(username=_weiboname,password=_weiboid)
        user_info = serializers.serialize("json", Users.objects.filter(name=_weiboname))
        return HttpResponse(user_info, content_type='application/json; charset=utf-8')