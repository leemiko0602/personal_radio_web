/**
 * Created by CMS on 2016/5/17.
 */
$(window).load(function(){
    //differentiateplaystatusprogram();
    flushProgramUI();
   $(".collect").click(function(){
       //$(this).css("color","#F76F12");
       var radioID=$(this).attr("radio-id");
       $.post('/collect/',{radio_id: radioID},function(data){
           if(data==0){
                    $(".collects").html("<span class='glyphicon glyphicon-heart' style='color: #F76F12;font-size: 25px' ></span>取消收藏");
                }
                if(data==1){
                    $(".collects").html("<span class='glyphicon glyphicon-heart' style='color: rgb(224,224,224);font-size: 25px' ></span>添加收藏");
                }
                if(data==3){
                    var r = confirm('请先登录');
                    if (r==true){window.location="/login";}
                    else {}
                }
       });
   });

});
//console.log('flush'+str(programIndex+1));
 var flushTime;
var  programIndex;
var isPlayed=new Array();
var isPlaying=new Array();
var overNow=new Array();
function ProgramNameChange(PlayTime,callback)
{
    var arr = PlayTime.split(":");
    var now = new Date();

    var date = new Date(now.getFullYear(),now.getMonth(),now.getDate(),arr[0],arr[1],now.getSeconds());

    var isOverTime = now.getTime()-date.getTime();

    return callback(isOverTime);
}

//区分节目现在播的状态
function differentiateplaystatusprogram(callback){
     isPlayed=[];
    isPlaying=[];
     //isNotPlayed=[];
    overNow=[];

     $(".thumb-sm").each(function(){
        var _this = $(this);
        var time = _this.text();
        //console.log('time'+time);
        ProgramNameChange(time,function(isOverNow){
            var lilist=_this.parent().attr("nprogram");
            if(isOverNow>=0){
				isPlayed.push(lilist);
				overNow.push(isOverNow);

            }
			else{
				//isNotPlayed.push(lilist);
                overNow.push(Math.abs(isOverNow));
			}

        });


    });
	 isPlaying.push(isPlayed.pop());
	 programIndex=parseInt(isPlaying[0]);
    var predom=$(".list-group-item[nprogram="+(programIndex-1)+"]");
    predom.removeClass("active");
    predom.children().first().removeClass("active");
    var nowdom=$(".list-group-item[nprogram="+programIndex+"]");
	nowdom.addClass("active");
    nowdom.children().first().addClass("active");
    nowdom[0].scrollIntoView(); //使页面滚动到底部
    //console.log('isPlayed'+isPlayed);
    //console.log('isPlaying'+isPlaying);
    //console.log(overNow);
    return callback(overNow);
}

//节目单界面刷新
function flushProgramUI()
{
    differentiateplaystatusprogram(
        function(overNow){
            //console.log((programIndex+1));
            flushTime=parseInt(overNow[programIndex+1]);
            //console.log(flushTime);
         //setTimeout("differentiateplaystatusprogram()",flushTime);
            setTimeout("flushProgramUI()",flushTime);
        }
    );


}

