$(window).load(function(){
	//loadBG();


       differentiateplaystatus();


    $(".start em[play-status='playing']").trigger("click");
   //$(".start em[play-status='playing']").click();
    //   getStar();



});

function getStar()
{
    //console.log(1);
        $(".star").each(function(){
            var scored=$(this).attr("scored");
            //console.log(scored);
         $(this).raty(
       {
         size: 35,
         score:scored,
         click: function (score, evt) {
            // console.log(score);

              var programID=$(this).attr("program-id");
             //console.log(programID);
             $.post('/programScore/',{score:score,program_id:programID});

           }


       });



    });

}

//区分节目现在播的状态
function differentiateplaystatus(){
     isPlayed=[];
    isPlaying=[];
     isNotPlayed=[];
    overNow=[];

     $(".start em").each(function(){
        var _this = $(this);
        var time = _this.attr("start-time");
        //console.log(time);
        ProgramNameChange(time,function(isOverNow){
            if(isOverNow>=0){
                //var isPlayed=new Array();
				isPlayed.push(_this.attr("sonN"));
				//console.log(isPlayed);

				overNow.push(isOverNow);
				_this.attr({"play-status":"played"});
                //console.log(_this.attr("play-status"));
            }


			else{
				//var isNotPlayed=new Array();
				isNotPlayed.push(_this.attr("sonN"));
                overNow.push(Math.abs(isOverNow));
				_this.attr({"play-status":"notplay"});
			}

        });


    });
	 isPlaying.push(isPlayed.pop());
	 songIndex=parseInt(isPlaying[0]);
	$(".start em[sonN="+songIndex+"]").attr({"play-status":"playing"});
  console.log(isPlayed);
	 console.log(isPlaying);
    console.log(overNow);
    return (isPlayed,isPlaying,isNotPlayed,overNow);

}

function fPlay(){
	//songIndex=parseInt(isPlaying[0]);
	//console.log(songIndex)


	//$(".start em[play-status='playing']").trigger("click");

}

var isPlayed=new Array();
var isPlaying=new Array();
var isNotPlayed=new Array();
var overNow=new Array();
var prowidthInt;
var vorprowidthInt;

var duration;
function getProwith(prowidth)
{
    var arrpro=String(prowidth).split("p");
    prowidthInts=parseInt(arrpro[0]);
    return prowidthInts;
}

//function differentiateplaystatusagain(isPlaying,isNotPlayed,isPlayed)
//{
//    isPlayed.push(isPlaying.pop());
//
//    isPlaying.push(isNotPlayed.shift()) ;
//
//    return (isPlaying,isNotPlayed,isPlayed)
//
//}



var songIndex;


function ProgramNameChange(PlayTime,callback)
{
    var arr = PlayTime.split(":");
    var now = new Date();
    var date;
    if(arr[0]<6)
    {
        date = new Date(now.getFullYear(),now.getMonth(),now.getDate()+1,arr[0],arr[1],arr[2]);
    }
    else
    {
        date = new Date(now.getFullYear(),now.getMonth(),now.getDate(),arr[0],arr[1],arr[2]);
    }


    var isOverTime =now.getTime()-date.getTime();

	//console.log(date.getTime());
	//console.log(now.getTime());


    return callback(isOverTime);

}


$(function(){
    /*节目评分*/
     getStar();
	//setTimeout("fPlay()",500);
	/*歌曲列表效果*/
	//$(".songList").hover(function(){
	//	$(this).find(".more").show();
	//	$(this).find(".dele").show();
	//},function(){
	//	$(this).find(".more").hide();
	//	$(this).find(".dele").hide();
	//});
	/*自定义滚动条*/
	$(".songUL").rollbar({zIndex:80});
	//$("#lyr").rollbar({zIndex:80});

	///*收藏节目*/
     $(".love").click(function(){
       //$(this).css("background-position","0px -130px");
         _this=$(this);
       var programID=$(this).attr("program-id");
       $.post('/collectProgram/',{program_id: programID},function(data){
           if(data==0){
                   _this.css("background-position","0px -130px");
                }
                if(data==1){
                    _this.css("background-position","-28px -130px");
                }

       });
   });

    ///*节目评分*/
    //$(".star").click(
    //    function(score,evt){
    //        alert('u selected '+score);
    //
    //
    //    });







//[play-status='played']"
	/*点击列表播放按钮*/
	$(".start em").click(function(){
        $(".songList").css("background-color", "#181F24");
        //$(this).parent(".songList").css("background-color", "#F0F0F0");
        //differentiateplaystatus();
        var prowidth=$(".progress").css("width");
        //console.log("process"+prowidth);
        prowidthInt=getProwith(prowidth);
        //console.log( prowidthInt);
        var volprowidth=$(".volControl").css("width");
        vorprowidthInt=getProwith(volprowidth);

       // console.log(prowidthInt);

        var play_status=$(this).attr("play-status");
        //console.log(play_status);
        var sid = $(this).attr("sonN");
        var programURL = $(this).attr("programURL");
        console.log(programURL);
        audio = document.getElementById("audio");
        if (play_status=="playing")
        {
            songIndex = sid;
            var this2=$(".start em[sonN="+sid+"]");
            var programID=$(this2).attr("program-id");
            $("#audio").attr("src", programURL);
            /*显示歌曲总长度*/
            if (audio.paused) {
                audio.currentTime=Math.round(overNow[sid-1]/1000);

                audio.play();
                console.log('playing');
                $.post('/getUserPlayPause/',{playtag:0,program_id:programID,newstart:1});

            }
            else
            {
                 audio.pause();
                 $.post('/getUserPlayPause/',{playtag:1,program_id:programID,newstart:0});

            }


            audio.addEventListener('timeupdate', updateProgress, false);

            audio.addEventListener('play', audioPlay, false);
            audio.addEventListener('pause', audioPause, false);
            audio.addEventListener('ended', audioEnded, false);
            var surplustime=parseInt((audio.duration-audio.currentTime)*1000);
            //console.log("audio.duration:"+audio.duration);
            //console.log("audio.currentTime:"+audio.currentTime);
            //console.log("surplustime:"+surplustime);
            //setTimeout(differentiateplaystatus(),surplustime);
            //setTimeout(fPlay(),surplustime);
            //对audio元素监听pause事件
            /*外观改变*/
            var html = "";
            html += '<div class="manyou">';
            html += '	<a href="#" class="manyouA">&nbsp;&nbsp;&nbsp;&nbsp;正在直播</a>';
            html += '</div>';
            $(".start em").css({
                "background": "",
                "color": ""
            });
            $(".manyou").remove();

            this2.css({
                "background": 'url("/static/images/T1X4JEFq8qXXXaYEA_-11-12.gif") no-repeat',
                "color": "transparent"
            });
            $(this).parent().parent().parent().append(html);
            $(this).parent().parent().parent().css({"background-color": "#232C32"});
            /*底部显示歌曲信息*/
            var songName = $(this).parent().parent().find(".colsn").html();
            var singerName = $(this).parent().parent().find(".colcn").html();
            $(".songName").html(songName);
            $(".songPlayer").html(singerName);
            // 获取结束时间$(".start em[sonN="+sid+"]")
            var sid1 = parseInt(songIndex)+1;
            var endTime=$(".colsn[sonN="+sid1+"]").html();
            //console.log(endTime);
            $(".endTime").html(endTime);

            //setTimeout('loadBG()',100);
            $(".blur").css("opacity", "0");
            $(".blur").animate({opacity: "1"}, 1000);


            ///*底部进度条控制*/
            //$( ".dian" ).draggable({
            //    containment:".pro2",
            //    drag: function() {
            //        var l=$(".dian").css("left");
            //        var le = parseInt(l);
            //        audio.currentTime = audio.duration*(le/prowidthInt);
            //    }
            //});


        }
		/*状态为isplayed,开始播放*/
		if(play_status=="played"){

            songIndex = sid;
            var this1=$(".start em[sonN="+sid+"]");
            //console.log(this1);
            var programID=$(this1).attr("program-id");
            $("#audio").attr("src", programURL);
            //audio = document.getElementById("audio");//获得音频元素
            /*显示歌曲总长度*/
            if (audio.paused) {

                audio.play();
                //收集点播的播放行为：playtag为o,播放,newstart表示一个新的播放
                console.log('play');
                $.post('/getUserPlayPause/',{playtag:0,program_id:programID,newstart:1});


            }
            else
            {
                //收集点播的暂停行为：playtag为o,暂停,不肯为新的播放
                audio.pause();
                $.post('/getUserPlayPause/',{playtag:1,program_id:programID,newstart:0});

            }

            audio.addEventListener('timeupdate', updateProgress, false);

            audio.addEventListener('play', audioPlay, false);
            audio.addEventListener('pause', audioPause, false);
            audio.addEventListener('ended', audioEnded, false);

            //对audio元素监听pause事件
            /*外观改变*/
            var html = "";
            html += '<div class="manyou">';
            html += '	<a href="#" class="manyouA">&nbsp;&nbsp;&nbsp;&nbsp;回到直播</a>';
            html += '</div>';
            $(".start em").css({
                "background": "",
                "color": ""
            });
            $(".manyou").remove();

            this1.css({
                "background": 'url("/static/images/T1X4JEFq8qXXXaYEA_-11-12.gif") no-repeat',
                "color": "transparent"
            });
            $(this).parent().parent().parent().append(html);
            $(this).parent().parent().parent().css("background-color", "#232C32");

            /*底部显示歌曲信息*/
            //获取播放时间
            var songName = $(this).parent().parent().find(".colsn").html();
            //获取节目名
            var singerName = $(this).parent().parent().find(".colcn").html();
            $(".songName").html(songName);
            $(".songPlayer").html(singerName);
            // 获取结束时间$(".start em[sonN="+sid+"]")
             var sid1 = parseInt(songIndex)+1;
            var endTime=$(".colsn[sonN="+sid1+"]").html();
           // console.log(endTime);
            $(".endTime").html(endTime);



            //setTimeout('loadBG()',100);
            $(".blur").css("opacity", "0");
            $(".blur").animate({opacity: "1"}, 1000);

            if(jQuery.ui)
            /*底部进度条控制*/
            $( ".dian" ).draggable({
                containment:".pro2",
                drag: function() {
                    var l=$(".dian").css("left");
                    var le = parseInt(l);
                    audio.currentTime = audio.duration*(le/prowidthInt);
                   //console.log(prowidthInt);
                }
            });

            $(".playBtn").unbind();
            /*底部播放按钮*/
            $(".playBtn").click(function(event){
                var p = $(this).attr("isplay");
                //console.log(p);
                if (p=="0") {
                    $(this).css("background-position","0 -30px");
                    $(this).attr("isplay","1");
                }
               else if (p=="1")  {
                    $(this).css("background-position","");
                    $(this).attr("isplay","0");
                     // console.log($(this));
                     //console.log(p);
                    //console.log($(this).attr("isplay"));


                }
                if(audio.paused)
                {
                    audio.play();
                    //收集点播的播放行为：playtag为o,播放,底部按钮不能产生新的播放事件
                    $.post('/getUserPlayPause/',{playtag:0,program_id:programID,newstart:0});
                }

                else
                {
                    audio.pause();
                    $.post('/getUserPlayPause/',{playtag:1,program_id:programID,newstart:0});

                }


            });
            //$(".mode").click(function(){
            //    // var t = calcTime(Math.floor(audio.currentTime))+'/'+calcTime(Math.floor(audio.duration));
            //    // //alert(t);
            //    // var p =Math.floor(audio.currentTime)/Math.floor(audio.duration);
            //    // alert(p);
            //    //alert(lytext[1]);
            //});
            /*切歌*/
            $(".prevBtn").unbind();
            $(".prevBtn").click(function(){
                var sid = parseInt(songIndex)-1;
                $(".start em[sonN="+sid+"]").click();
            });
             $(".nextBtn").unbind();
            $(".nextBtn").click(function(){
                var sid = parseInt(songIndex)+1;
                $(".start em[sonN="+sid+"]").click();
            });

            /*回到直播*/
            $(".manyouA").unbind();
             $(".manyouA").click(function(){
               $(".start em[play-status='playing']").trigger("click");
            });

        }
	});


    //公共部分
      /*音量控制*/
            if(jQuery.ui)
            $( ".dian2" ).draggable({
                containment:".volControl",
                drag: function() {
                    var l=$(".dian2").css("left");
                    var le = parseInt(l);
                    audio.volume=(le/vorprowidthInt);
              }
            });

            //     /*双击播放*/
            //$(".songList").unbind();
            //$(".songList").dblclick(function(){
            //    var sid = $(this).find(".start em").html();
            //    console.log(sid);
            //    $(".start em[sonN="+sid+"]").click();
            //});





	});








/*首尾模糊效果*/
function loadBG(){
	//alert();
	// stackBlurImage('canvas1', 'canvas', 60, false);
	var c=document.getElementById("canvas");
	var ctx=c.getContext("2d");
	var img=document.getElementById("canvas1");
	ctx.drawImage(img,45,45,139,115,0,0,1366,700);
	stackBlurCanvasRGBA('canvas',0,0,1366,700,60);
}
function calcTime(time){
	var hour;         	var minute;    	var second;
	hour = String ( parseInt ( time / 3600 , 10 ));
	if (hour.length ==1 )   hour='0'+hour;
	minute=String(parseInt((time%3600)/60,10));
	if(minute.length==1) minute='0'+minute;
	second=String(parseInt(time%60,10));
	if(second.length==1)second='0'+second;
	return (hour+":"+minute+":"+second);
}
function updateProgress(ev){
	/*显示歌曲总长度*/
   // console.log(Math.floor(audio.duration));
	var songTime = calcTime(Math.floor(audio.duration));
   // console.log(songTime);

	$(".duration").html(songTime);
	/*显示歌曲当前时间*/
	var curTime = calcTime(Math.floor(audio.currentTime));
	$(".position").html(curTime);
	/*进度条*/
	var lef = prowidthInt*(Math.floor(audio.currentTime)/Math.floor(audio.duration));
	var llef = Math.floor(lef).toString()+"px";
	$(".dian").css("left",llef);
}
function audioPlay(ev){
	$(".iplay").css("background",'url("/static/css/images/T1oHFEFwGeXXXYdLba-18-18.gif") 0 0');
	$(".playBtn").css("background-position","0 -30px");
	$(".playBtn").attr("isplay","1");
}
function audioPause(ev){
	$(".iplay").css("background","");
	// $(".start em").css({
	// 	"background":'url("css/images/pause.png") no-repeat 50% 50%',
	// 	"color":"transparent"
	// });
}
function audioEnded(ev){
    var sid = parseInt(songIndex)+1;
    console.log("audioEnded:"+sid);
    differentiateplaystatus();
	$(".start em[sonN="+sid+"]").click();
}

function conSeconds(t)//把形如：01：25的时间转化成秒；
{	
   var m=t.substring(0,t.indexOf(":")); 
   var s=t.substring(t.indexOf(":")+1); 
   m=parseInt(m.replace(/0/,""));
   //if(isNaN(s)) s=0; 
   var totalt=parseInt(m)*60+parseInt(s); 
   //alert
   // (parseInt(s.replace(//b(0+)/gi,""))); 
   //if(isNaN(totalt))  return 0; 
  
	return totalt; 
} 
// function getSeconds()//得到当前播放器播放位置的时间 
// { var t=getPosition(); t=t.toString();//数字转换成字符串
//  var s=t.substring(0,t.lastIndexOf("."));//得到当前的秒 
//  //alert(s); 
//  return s; 
//  } 
//  function getPosition()//返回当前播放的时间位置
//   { var mm=document.getElementById("MediaPlayer1"); 
//    //var mmt=;
//    //alert(mmt); 
//    return mm.CurrentPosition; 
// } 
//function mPlay()//开始播放
//{
//	// var ms=parseInt(getSeconds());
//	// if(isNaN(ms)) show(0);
//	// else show(ms);
//   var ms =audio.currentTime;
//   show(ms);
//	window.setTimeout("mPlay()",100)
//}

// window.setTimeout("mPlay()",100);
// window.setTimeout("getReady()",100);
// function test()//测试使用，
// { 
// 	alert(lytime[lytime.length-1]); 
// }
