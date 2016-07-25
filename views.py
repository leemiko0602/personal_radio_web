#coding=utf-8
from datetime import  datetime,date
from django.contrib.auth.models import User
from django.http import  HttpResponse
from django.shortcuts import render,render_to_response
from django.core import serializers
from user_info.models import Users,AuthUser,UserProgramCollect,RbcProgram,UserStationCollect,LiveTelecastRadio
import re

#用户修改密码
def change_pwd(request):
    org_pwd=request.POST['_org_pwd']
    new_pwd=request.POST['_new_pwd']
    conf_pwd=request.POST['_conf_pwd']
    #request.session['preURL']='userInfoChange'
    def is_chinese(uchar):
        if uchar>=u'\u4e00'and uchar<=u'\u9fa5':
            return True
        else:
            return  False
    u1=is_chinese(org_pwd)
    u2=is_chinese(new_pwd)
    u3=is_chinese(conf_pwd)
    if request.user.is_authenticated():
        if not(org_pwd and new_pwd and conf_pwd):
            error1='初始密码\密码\确认密码不能为空'
            return  HttpResponse(error1)
        elif (u1 and u2 and u3):
            error2='初始密码\密码\确认密码必须为字符和数字的组合'
            return HttpResponse(error2)
        elif (len(new_pwd)<8):
            error3='密码长度不能少于8'
            return HttpResponse(error3)
        elif not(new_pwd==conf_pwd):
            error4='两次输入的密码不一致'
            return HttpResponse(error4)
        elif org_pwd==new_pwd:
            error5='你要修改的密码与初始密码相同'
            return HttpResponse(error5)
        else:
            user=Users.objects.get(name=request.user.username)
            if user.login_type==0:
                if not (user.password == org_pwd):
                    error6 = '你输入的初始密码错误'
                    return HttpResponse(error6)
                else:
                    if user.password == new_pwd:
                        error7= "你要修改的密码与原密码相同"
                        return HttpResponse(error7)
                    else:
                        user.password = new_pwd
                        user.save()
                        auth_user=User.objects.get(username=user.name)
                        auth_user.set_password(new_pwd)
                        auth_user.save()
                        flag=1
                        print('1'+request.session['preURL'])
                        request.session['preURL']='userInfo'
                        print('2'+request.session['preURL'])
                        return HttpResponse(flag)
            else:
                error8='微博登录用户不能修改密码'
                return HttpResponse(error8)
    else:
        error9='请登录'
        return HttpResponse(error9)




#用户收藏的节目
def program_collect(request):
    id=request.user.id
    program_collect=UserProgramCollect.objects.filter(user_id=id)
    program_id = []
    program=[]
    for p in program_collect:
        program_id.append(p.program_id)
    for i in range(0,len(program_id)):
        rbc=RbcProgram.objects.get(id=program_id[i])
        program.append((rbc.block_name+'#'+str(rbc.id)+'$'+str(rbc.radio_id)+'%'+str(rbc.duration)+'*'+rbc.file_name+'@'))
    return HttpResponse(program)


#用户收藏的电台
def station_collect(request):
     id=request.user.id
     _station_collect=UserStationCollect.objects.filter(user_id=id)
     station_id=[]
     station=[]
     for s in _station_collect:
         station_id.append(s.radio_id)

     for i in range(0,len(station_id)):
         station.append(LiveTelecastRadio.objects.get(id=station_id[i]))
     return HttpResponse(e.name+'.'for e in station)

#用户收藏节目删除
def program_collect_delete(request):
     _user_id=request.user.id
     _program_id=request.POST['pro_id']
     _collect=UserProgramCollect.objects.filter(user_id=_user_id).get(program_id=_program_id)
     _collect.delete()
     return HttpResponse(1)

#用户收藏节目全选删除
def program_collect_delete_all(request):
    _user_id=request.user.id
    _collect = UserProgramCollect.objects.filter(user_id=_user_id)
    _collect.delete()
    return HttpResponse(1)

#用户收藏节目多选删除
def program_collect_multi_delete(request):
    user_id=request.user.id
    program_str=request.POST['p_str']
    ret=re.split('m', program_str)
    for i in range(1,len(ret)):
        _collect = UserProgramCollect.objects.filter(user_id=user_id).get(program_id=ret[i])
        _collect.delete()
    return HttpResponse(1)

#用户收藏电台删除
def station_collect_delete(request):
    _user_id=request.user.id
    _station_name=request.POST['station_name']
    _radio=LiveTelecastRadio.objects.get(name=_station_name)
    _collect=UserStationCollect.objects.filter(user_id=_user_id).get(radio_id=_radio.id)
    _collect.delete()
    return HttpResponse(1)
#用户收藏电台全选删除
def station_collect_delete_all(request):
    user_id=request.user.id
    _collect = UserStationCollect.objects.filter(user_id=user_id)
    _collect.delete()
    return HttpResponse(1)

#用户收藏电台多选删除
def station_collect_multi_delete(request):
    _user_id=request.user.id
    station_str=request.POST['s_str']
    ret=re.split('l', station_str)
    for i in range(1, len(ret)):
        _radio = LiveTelecastRadio.objects.get(name=ret[i])
        _collect = UserStationCollect.objects.filter(user_id=_user_id).get(radio_id=_radio.id)
        _collect.delete()
    return HttpResponse(1)

# 测试收藏接口 http://127.0.0.1:8000/collectAPI/?userid= 输入用户id
def collectAPI(request,userID):
    try:
        userID = int(userID)
    except ValueError:
        raise Http404()
    program_id = []#存放节目id
    program = []#存放节目的信息，名字和时长等等
    program_collect = UserProgramCollect.objects.filter(user_id=userID)
    for s in program_collect:
        program_id.append(s.program_id)
    for i in range(0, len(program_id)):
        program.append((RbcProgram.objects.get(id=program_id[i])))
    userCollectList = serializers.serialize("json", program)
    # return HttpResponse(userCollectList, content_type='application/json; charset=utf-8')
    return HttpResponse(simplejson.dumps(uni_str(userCollectList, encode)), mimetype = "application/json")

#修改密码接口 http://127.0.0.1:8000/changepasswordAPI/?userid=&newpwd= 输入用户id和新密码
def changepasswordAPI(request):
    if 'userid'and'newpwd' in request.GET:
        _userid=request.GET['userid']
        _newpwd=request.GET['newpwd']
        user=Users.objects.get(id=_userid)
        user.password=_newpwd
        user.save()
        auth_user = User.objects.get(id=_userid)#修改django认证表的内容
        auth_user.set_password(_newpwd)
        auth_user.save()
        user_info=serializers.serialize("json",Users.objects.filter(id=_userid))
        return HttpResponse(user_info, content_type='application/json; charset=utf-8')
