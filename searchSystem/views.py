#!/usr/bin/env python
#-*- coding: utf-8 -*- 
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.http import HttpResponse
from searchSystem.models import LiveRadioDictionary,LiveTelecastRadio,LiveRadioPlayList,UserStationCollect
from datetime import datetime,date

#微博登录

#from weibo import APIClient



from django.core import serializers
import json, webbrowser 
from django.http import Http404
from django.db.models import Q
#import datetime

from django.contrib.auth.models import User
from django.conf import settings
from django.contrib import auth
from django.contrib.auth import login, logout, authenticate



#微博登录	
# APP_KEY = '1028043534'# 设置你申请的appkey
# APP_SECRET = 'ecf27fb12a960424b9b3ff42c5639939'# 设置你申请的appkey对于的secret
# CALLBACK_URL = 'http://radio.cucplus.com/live/'

# Create your views here.

def search(request) :
    return render(request, 'search.html', {'current_time': datetime.now()})
	




#地区导航
def displayArea(request):
    try:
        liveArea_list = LiveRadioDictionary.objects.filter(type='area')
        #liveType_list= LiveRadioDictionary.objects.filter(type='type')
    except LiveRadioDictionary.DoesNotExist :
        raise Http404

    return render_to_response('liveTelecast/liveArea.html', {'liveAreas':liveArea_list,'uname':request.user.username})
##类型导航
def displayType(request):
    try:
        #liveArea_list = LiveRadioDictionary.objects.filter(type='area')
        liveType_list= LiveRadioDictionary.objects.filter(type='type')
    except LiveRadioDictionary.DoesNotExist :
        raise Http404

    return render_to_response('liveTelecast/liveType.html', {'liveType':liveType_list,'uname':request.user.username})
#显示具体广播台
def displayRadio(request):
    try:
        query_id = request.GET.get('id', '')

    except  LiveTelecastRadio.DoesNotExist:
        raise Http404
    Radio_list=LiveTelecastRadio.objects.filter(Q(area=query_id )| Q(type=query_id))
    #导航开头
    area=LiveRadioDictionary.objects.get(id=query_id)
   # Radio_list=LiveTelecastRadio.objects.all()
    return render_to_response('liveTelecast/liveradio.html',{'Radiolists':Radio_list,'area':area ,'uname':request.user.username})

#播放
def radioPlay(request):
    # import pdb; pdb.set_trace()
    mmsadress = request.GET.get('address', '')
    radio=LiveTelecastRadio.objects.get(url= mmsadress)
    request.session['URL']=request.get_full_path()
    #判断是否收藏
    exist=''
    if request.user.is_authenticated():
        try :
            UserStationCollect.objects.filter(user_id =request.user.id).get(radio_id= radio.id)
            exist = '1'
        except UserStationCollect.DoesNotExist:
            exist = ''
    #北京地区节目单单独显示
    if radio.name.__contains__("北京"):
        radioBeijingID=radio.id
        today=date.today()
        radioBeijingProgramList=LiveRadioPlayList.objects.filter(radio_id=radioBeijingID)
        #radioBeijingProgramList=LiveRadioPlayList.objects.filter(radio_id=radioBeijingID).filter(play_date__contains=today)
        #if(radioBeijingProgram. play_date==datetime.now()):
        return render_to_response('liveTelecast/1.html',
                                  {'mmsadress':mmsadress,'radio':radio,'radioBeijingProgramList':radioBeijingProgramList,
                                   'uname':request.user.username,'collect':exist,'today':today})
    else:
    #其他地区节目单显示
        return render_to_response('liveTelecast/1.html',
                                  {'mmsadress':mmsadress,'radio':radio,'radioBeijingProgramList':'','uname':request.user.username,'collect':exist})


    #return render_to_response('liveTelecast/radioPlay.html',{'mmsadress':mmsadress,'radio':radio})


#收藏，将用户ID，节目id存入数据库
def collect(request):
    if (request.user.is_authenticated() and request.user.is_active) :
        userId=request.user.id
        radioID=request.POST['radio_id']
        try:
            #1 表示删除收藏
            user_collect = UserStationCollect.objects.filter(user_id = userId).get(radio_id = radioID)
            user_collect.delete()
            return HttpResponse(1)
        except UserStationCollect.DoesNotExist:
            #0表示收藏
            UserStationCollect.objects.create(user_id=userId,radio_id=radioID)
            return HttpResponse(0)
    else:
        #表示未登录
        request.session['preURL']='collect'
        return HttpResponse(3)




#接口1test
#接口1test
def liveRadioBjAPI(request):
    lists=[]
    BJradio_lists=LiveTelecastRadio.objects.filter(area=2)#北京
    HBradio_lists=LiveTelecastRadio.objects.filter(area=5)#河北
    NMGradio_lists=LiveTelecastRadio.objects.filter(area=25)#内蒙古
    LNradio_lists=LiveTelecastRadio.objects.filter(area=21)#辽宁
    TJradio_lists=LiveTelecastRadio.objects.filter(area=3)#天津
    GXradio_lists = LiveTelecastRadio.objects.filter(area=26)  # 广西
    SXradio_lists=LiveTelecastRadio.objects.filter(area=23)  #陕西
    for BJradio_list in BJradio_lists:
       BJradio={}
       BJradio['area']='北京'
       BJradio['id']=BJradio_list.id
       BJradio['name']=BJradio_list.name
       BJradio['type']=BJradio_list.type
       BJradio['url']=BJradio_list.url
       BJradio['url_playlist']=BJradio_list.url_playlist
       lists.append(BJradio)
    for HBradio_list in HBradio_lists:
        HBradio={}
        HBradio['area']='河北'
        HBradio['id'] = HBradio_list.id
        HBradio['name'] = HBradio_list.name
        HBradio['type'] = HBradio_list.type
        HBradio['url'] = HBradio_list.url
        HBradio['url_playlist'] = HBradio_list.url_playlist
        lists.append(HBradio)
    for NMGradio_list in NMGradio_lists:
        NMGradio={}
        NMGradio['area'] = '内蒙古'
        NMGradio['id'] = NMGradio_list.id
        NMGradio['name'] = NMGradio_list.name
        NMGradio['type'] = NMGradio_list.type
        NMGradio['url'] =  NMGradio_list.url
        NMGradio['url_playlist'] = NMGradio_list.url_playlist
        lists.append(NMGradio)
    for LNradio_list in LNradio_lists:
        LNradio = {}
        LNradio['area'] = '抚顺'
        LNradio['id'] = LNradio_list.id
        LNradio['name'] = LNradio_list.name
        LNradio['type'] =LNradio_list.type
        LNradio['url'] = LNradio_list.url
        LNradio['url_playlist'] = LNradio_list.url_playlist
        lists.append(LNradio)
    for TJradio_list in TJradio_lists:
        TJradio = {}
        TJradio['area'] = '天津'
        TJradio['id'] = TJradio_list.id
        TJradio['name'] = TJradio_list.name
        TJradio['type'] = TJradio_list.type
        TJradio['url'] = TJradio_list.url
        TJradio['url_playlist'] = TJradio_list.url_playlist
        lists.append(TJradio)
    for  GXradio_list in GXradio_lists:
        GXradio={}
        GXradio['area'] = '广西'
        GXradio['id'] = GXradio_list.id
        GXradio['name'] = GXradio_list.name
        GXradio['type'] = GXradio_list.type
        GXradio['url'] = GXradio_list.url
        GXradio['url_playlist'] = GXradio_list.url_playlist
        lists.append(GXradio)
    for SXradio_list in SXradio_lists:
        SXradio = {}
        SXradio['area'] = '陕西'
        SXradio['id'] = SXradio_list.id
        SXradio['name'] = SXradio_list.name
        SXradio['type'] = SXradio_list.type
        SXradio['url'] = SXradio_list.url
        SXradio['url_playlist'] =SXradio_list.url_playlist
        lists.append(SXradio)
    live_list = json.dumps(lists)
    return HttpResponse(live_list)

# http://127.0.0.1:8000/stationCollectAPI/?user_id=20&radio_id=17
# 用户收藏电台ID接口，将收藏电台存储
def stationCollectAPI(request):
    if 'user_id' and 'radio_id' in request.GET:
        _user_id = request.GET['user_id']
        _radio_id = request.GET['radio_id']
        UserStationCollect.objects.create(user_id=_user_id,radio_id=_radio_id)
        station_collection = serializers.serialize("json",UserStationCollect.objects.filter(user_id = _user_id).filter(radio_id = _radio_id))
        return HttpResponse(station_collection, content_type='application/json; charset=utf-8')