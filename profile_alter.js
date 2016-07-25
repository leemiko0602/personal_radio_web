/**
 * Created by CMS on 2016/5/23.
 */
//change_pwd.js change to profile_alter.js

var audio = document.getElementById("myAudio");
var prowidth=$("._progress").css("width");//进度条
var changestyle=document.getElementById("btn_play");//底部播放键

$(document).ready(function(){
    $("#submit").click(function()
    {
        var org_pwd=$("#org_pwd").val();
        var new_pwd=$("#new_pwd").val();
        var conf_pwd=$("#conf_pwd").val();
        $.post("/changepassword/",{_org_pwd: org_pwd,_new_pwd:new_pwd,_conf_pwd:conf_pwd},function(ret)
        {
            if(ret==1) {
                $("#error").html("修改成功，请重新<a style='color:#108d4e' href='/login/'>登录</a>");
            }
            else
            {
                $("#error").text(ret);
            }
            

        });
    });
});
// 收藏的节目显示
$(document).ready(function() {
    $.get("/user_program_collect/", function (ret)
    {
        // alert(ret);
        // var id=ret.match(/\d+/g);
        // var _split=ret.split('(\'');
        var _split=ret.split('@');
        var temp1,name;
        var temp2,id;
        var temp3,radio_id;
        var duration;
        var file_name;
        for(var i=0;i<_split.length-1;i++)
        {
            // temp=_split[i].split('\'\,')[1];
            // id=temp.split(')')[0];
            // name=_split[i].split('\'\,')[0];
            name=_split[i].split('#')[0];
            temp1=_split[i].split('#')[1];
            id=temp1.split('$')[0];
            temp2=temp1.split('$')[1];
            radio_id=temp2.split('%')[0];
            temp3=temp2.split('%')[1];
            duration=temp3.split('*')[0];
            file_name=temp3.split('*')[1];
            var row='<tr id=row'+i+'><td ><label  class="checkbox m-n i-checks" id=p_choose'+i+'><input  type="checkbox" name="checkbox" id=p_check'+i+' value='+id+' ><i></i></label></td><td  >'+name+'</td> <td> <a id=play_box'+i+' data-toggle="class" ><i class="icon-control-play text" name='+name+' file_name='+file_name+' radio_id='+radio_id+' duration='+duration+' id=p_play'+i+' onclick="getinfo(this)"></i><i class="text-active" id=p_pause'+i+' onclick="pause()" >&nbsp;&nbsp;&nbsp;&nbsp;</i></a><td> <i onclick="p_delete(this.parentNode)" class="fa fa-times text-danger text" id=p_delete'+i+'></i></td></tr>';//class="icon-control-pause text"
            $("#program").append(row);
        }
        $("#sum_programcollet").text(_split.length-1);//信息栏显示收藏的节目数量
        // var program_id=$('#p_check1').val();
        // play_prepare(program_id);
        if(_split.length-1>0)
        {
            $("#myAudio").attr('playing_row', 0);
            $("._songName").html(_split[0].split('#')[0]);//节目名
            $("._duration").html(calcTime(Math.floor(_split[0].split('#')[1].split('$')[1].split('%')[1].split('*')[0])));//节目时长
            audio.src = 'http://101.201.81.34:8089/rbc_fm/' + _split[0].split('#')[1].split('$')[1].split('%')[0] + '/' + _split[0].split('#')[1].split('$')[1].split('%')[1].split('*')[1] + '';
        }
    });
});
//收藏的电台显示
$(document).ready(function() {
    $.post("/user_station_collect/",function (ret)
    {
        var name=ret.split('.');
        for(var i=0;i<name.length-1;i++)
        {   
            var s_row='<tr id=row'+i+'><td ><label class="checkbox m-n i-checks" ><input type="checkbox" id=s_check'+(i+1)+' value='+name[i]+' ><i></i></label></td><td >'+name[i]+'</td> <td> <i onclick="s_delete(this.parentNode)" class="fa fa-times text-danger text" id=s_delete'+i+'></i></td></tr>';
            $("#station").append(s_row);
        }
      $("#sum_stationcollect").text(name.length-1);
    });


});
//删除当前行所收藏的节目
function p_delete (k){ //节目名有数字时，划分会出现问题，会出现删除不成功的bug
    var tr_Seq = $(k).parent().parent().find("tr").index($(k).parent()[0]);//获取当前所在的行
    // var name= $(k).parent().parent().find("tr").eq(tr_Seq).children("td").eq(0);//获取当前行的节目所在列
    var _id=$('#p_check'+tr_Seq+'').val();
    var flag=confirm("确定删除吗？");
    if(flag)
    {
         $(k).parent().remove();
        $.post("/program_collect_delete/",{pro_id:_id} );

    }
}


//删除当前行收藏的电台
function s_delete(k) {
    var tr_Seq = $(k).parent().parent().find("tr").index($(k).parent()[0]);//获取当前所在的行
    var name= $(k).parent().parent().find("tr").eq(tr_Seq).children("td").eq(1);
    var _flag=confirm("确定删除吗？");
    if (_flag)
    {

        $.post("/station_collect_delete/",{station_name:name.text()});
           $(k).parent().remove();


    }

}
// 批量删除收藏节目
function  program_multiselect_delete()
{
    var len = document.getElementById("program_table").rows.length;
    var program_str='';
    var count=0;
    _flag = confirm("确定删除吗？");
    if (_flag) {
        if (document.getElementById("program_choose_all").checked) {//全选删除

            for (var i = 0; i < len - 1; i++) {

                $('#p_check' + i + '').parent().parent().parent().remove();
            }
            $.post("/p_collect_delete_all/");
        }
        else {
            for (var j = 0; j < len+1; j++)
            {
                var _id = document.getElementById("p_check" + j + "");
                if (document.getElementById("p_check" + j + ""))
                {
                    if (_id.checked)
                    {
                        count++;
                        var pro = _id.value;
                        program_str = program_str + 'm' + pro;
                        $('#p_check' + j + '').parent().parent().parent().remove();
                    }
                }
                else
                    continue;
                
            }
            if(count>0)
            {
             $.post("/collect_multi_delete/", {p_str:program_str});
            }
            else
            {
                 alert("请勾选你要删除的行");
            }

        }

    }
}
 //批量删除收藏电台
function staion_multiselect_delete()
{
      
    var len= document.getElementById("station_table").rows.length;
    var station_str='';
    var count=0;
    _flag=confirm("确定删除吗？");
    if(_flag)
    {
        if (document.getElementById("station_choose_all").checked) {
                 // var name = document.getElementById("staion" +1+ "");
                 // alert(name.value);
            for (var i = 1; i < len; i++)
            {

                $('#s_check' + i + '').parent().parent().parent().remove();
            }
            $.post("/s_collect_delete_all/");//成功
        }
        else {
            for (var j = 1; j < len+1;j++) //遍历的方式实现批量删除？是否存在问题，待考虑(添加一个事件监听）
            {
                var _name = document.getElementById("s_check" +j+ "");
                if (document.getElementById("s_check" +j+ ""))
                {
                    if (_name.checked)
                    {

                        count++;
                        var sta = _name.value;
                        station_str = station_str + 'l' + sta;
                        $('#s_check' + j + '').parent().parent().parent().remove();
                    }
                }
                else
                    continue;

            }
            if(count>0)
            {
                 // location.reload();//刷新页面重置待解决
                $.post("/multi_delete_sta/", {s_str:station_str});
            }
            else
            {
                 alert("请勾选你要删除的行");

            }


        }
    }

}


// 节目播放  http://res.audio.rbc.cn/mp3/ajgb/jqsy15dd/jqsy15dd2016041915307182.mp3
//click事件
function getinfo(k)
{
    var now=$("#myAudio").attr("playing_row");
    $('#play_box'+now+'').removeClass('_radioplay active');//移除当前播放行的外观
    var num=k.id.split('y')[1];
    if(now==num)
    {
        audio.play();
        changestyle.style.backgroundPosition=" 0px -30px";
        $('#play_box'+num+'').attr('class','_radioplay ');
    }
    else{
        var duration= k.getAttribute("duration");
    var radio_id=k.getAttribute('radio_id');
    var file_name=k.getAttribute('file_name');
    var name=k.getAttribute('name');
    var songTime = calcTime(Math.floor(duration));
    audio.src='http://101.201.81.34:8089/rbc_fm/'+radio_id+'/'+file_name+'';
    $("._songName").html(name);//节目名
    $("._duration").html(songTime);//节目时长
    audio.play();
    changestyle.style.backgroundPosition=" 0px -30px";
    $("#myAudio").attr('playing_row',num);
    $('#play_box'+num+'').attr('class','_radioplay ');//只能改变一个相关的按钮
    }

    audio.addEventListener('timeupdate', updateProgress, false);
    audio.addEventListener('ended', audioEnded, false);

}


//底部播放按钮click事件
$("._pbtn._playBtn").click(function (){
    var flag=$("#myAudio").attr("src");
    if(flag)
    {
        var num=$("#myAudio").attr("playing_row");
        if(audio.paused)
        {
            audio.play();
            changestyle.style.backgroundPosition=" 0px -30px";
            $('#play_box'+num+'').attr('class','_radioplay  active');//已修改
        }
        else
        {
            audio.pause();
            $("#btn_play").removeAttr("style");
            $('#play_box'+num+'').removeClass('_radioplay active');

        }
        audio.addEventListener('timeupdate', updateProgress, false);
        audio.addEventListener('ended', audioEnded, false);
    }


});



//切歌 下一首
$("._pbtn._nextBtn").click(function () {
    var len= document.getElementById("program_table").rows.length;
    var num=$("#myAudio").attr("playing_row");
    alert(len);
    if(num<len-1) {
        var id = parseInt(num) + 1;
        while (id <len )
        {
            if (!document.getElementById('p_choose' + id + ''))
            {
                id++;
            }
            else
                break;
        }
         alert(id);
        if (id <len  )
        {
            changestyle.style.backgroundPosition = " 0px -30px";//底部播放按键
            $('#play_box' + num + '').removeAttr('class');
            $("#myAudio").attr('playing_row', id);
            var duration = $('#p_play' + id + '').attr('duration');
            var name = $('#p_play' + id + '').attr('name');
            var file_name = $('#p_play' + id + '').attr('file_name');
            var radio_id = $('#p_play' + id + '').attr('radio_id');
            var songTime = calcTime(Math.floor(duration));
            audio.src = 'http://101.201.81.34:8089/rbc_fm/' + radio_id + '/' + file_name + '';
            $("._songName").html(name);//节目名
            $("._duration").html(songTime);//节目时长
            audio.play();
            $('#play_box' + id + '').attr('class', '_radioplay active');//已修改
            audio.addEventListener('timeupdate', updateProgress, false);
            audio.addEventListener('ended', audioEnded, false);
        }
    }
});
//上一首
$("._pbtn._prevBtn").click(function () {
    var num=$("#myAudio").attr("playing_row");
    if(num>0)
    {
        var id = parseInt(num) - 1;
        while (id > 0) {
            if (!document.getElementById('p_choose' + id + ''))
            {
                 id--;
            }
             else
                break;
        }
        if (id >=0)
        {
            changestyle.style.backgroundPosition = " 0px -30px";//底部播放按键
            $('#play_box' + num + '').removeAttr('class');
            $("#myAudio").attr('playing_row', id);
            var duration = $('#p_play' + id + '').attr('duration');
            var name = $('#p_play' + id + '').attr('name');
            var file_name = $('#p_play' + id + '').attr('file_name');
            var radio_id = $('#p_play' + id + '').attr('radio_id');
            var songTime = calcTime(Math.floor(duration));
            audio.src = 'http://101.201.81.34:8089/rbc_fm/' + radio_id + '/' + file_name + '';
            $("._songName").html(name);//节目名
            $("._duration").html(songTime);//节目时长
            audio.play();
            $('#play_box' + id + '').attr('class', '_radioplay  active');//已修改
            audio.addEventListener('timeupdate', updateProgress, false);
            audio.addEventListener('ended', audioEnded, false);

        }
    }

});

//公布部分
// //播放功能
// function play(){
//     var num=$("#myAudio").attr("playing_row");
//     var changestyle=document.getElementById("btn_play");
//     if(audio.paused)
//     {
//         audio.play();
//         changestyle.style.backgroundPosition=" 0px -30px";
//         $('#play_box'+num+'').attr('class','_radioplay  active');//已修改
//     }
//     else
//     {
//         audio.pause();
//         $("#btn_play").removeAttr("style");
//         $('#play_box'+num+'').removeClass('_radioplay active');
//
//     }
//      audio.addEventListener('timeupdate', updateProgress, false);
//      audio.addEventListener('ended', audioEnded, false);
// }







//暂停功能
function pause() { //每一行的暂停功能
    var num=$("#myAudio").attr("playing_row");
    if(audio.played)
    {
        audio.pause();
        $("#btn_play").removeAttr("style");
        $('#play_box'+num+'').removeClass('_radioplay');
    }

}
//快进进度条控制
if(jQuery.ui)
/*底部进度条控制*/
    $( "._dian" ).draggable({
        containment:"._pro2",
        drag: function() {
            var l=$("._dian").css("left");
            var le = parseInt(l);
            prowidthInt=getProwith(prowidth);
            audio.currentTime = audio.duration*(le/prowidthInt);
            var curTime = calcTime(Math.floor(audio.currentTime));
            $("._position").html(curTime); /*现在播放的时间*/
            changestyle.style.backgroundPosition=" 0px -30px";//底部播放按键
            audio.addEventListener('timeupdate', updateProgress, false);
            audio.addEventListener('ended', audioEnded, false);
        }
    });
//音量大小控制
/*音量控制*/
if(jQuery.ui)
    $( "._dian2" ).draggable({
        containment:"._volControl",
        drag: function() {
            var l=$("._dian2").css("left");
            var le = parseInt(l);
            var volprowidth=$("._volControl").css("width");
            vorprowidthInt=getProwith(volprowidth);
            audio.volume=(le/vorprowidthInt);
        }
    });
//当前播放时间以及进度条实时
function updateProgress(){
    /*显示歌曲总长度*/
    var songTime = calcTime(Math.floor(audio.duration));
    prowidthInt=getProwith(prowidth);
    // $("._duration").html(songTime); /*歌曲时间长度*/  //删除
    /*显示歌曲当前时间*/
    var curTime = calcTime(Math.floor(audio.currentTime));
    $("._position").html(curTime); /*现在播放的时间*/
    /*进度条*/
    var lef = prowidthInt*(Math.floor(audio.currentTime)/Math.floor(audio.duration));
    var llef = Math.floor(lef).toString()+"px";
    $("._dian").css("left",llef);
}
//当一首节目播完了，播下一个节目
function audioEnded() {
   var len= document.getElementById("program_table").rows.length;
    var num=$("#myAudio").attr("playing_row");
    if(num<len-2)
    {
        var id=parseInt(num)+1;
        $("#myAudio").attr('playing_row',id);
        var duration=$('#p_play'+id+'').attr('duration');
        var name=$('#p_play'+id+'').attr('name');
        var file_name=$('#p_play'+id+'').attr('file_name');
        var radio_id=$('#p_play'+id+'').attr('radio_id');
        var songTime = calcTime(Math.floor(duration));
        audio.src='http://101.201.81.34:8089/rbc_fm/'+radio_id+'/'+file_name+'';
        $("._songName").html(name);//节目名
        $("._duration").html(songTime);//节目时长
        audio.play();
        audiopause();//播放时修改按键外观
        $('#play_box'+id+'').attr('class','_radioplay  active');//已修改
        audio.addEventListener('timeupdate', updateProgress, false);
        audio.addEventListener('ended', audioEnded, false);
    }
    else
    {
        $('#play_box'+(len-2)+'').removeAttr('class');
        $("#btn_play").removeAttr("style");
    }
}
//暂停时 播放键处理
// function ()
// {
//      var num=$("#myAudio").attr("playing_row");
//      $('#play_box'+num+'').removeAttr('class');
//
// }

//个人信息和修改密码页面切换
$('.btn.btn-info').click(function () {
    document.getElementById("info").style.display="block";
    document.getElementById("change").style.display="none";

});
$('.btn.btn-success').click(function () {
    document.getElementById("info").style.display="none";
    document.getElementById("change").style.display="block";
});
//节目收藏和电台收藏页面切换
$('#sec_1').click(function () {
    document.getElementById("fir_sec").style.display="block";
    document.getElementById("seco_sec").style.display="none";
});

$('#sec_2').click(function () {
    document.getElementById("fir_sec").style.display="none";
    document.getElementById("seco_sec").style.display="block";
});
