/**
 * Created by Administrator on 2016/4/12.
 */
/*加载年份*/

function years(obj, Cyear) {
    var len = 134; // select长度,即option数量
    var selObj = document.getElementById(obj);
    //selObj.length = 0;
    var selIndex = len - 1;
    var newOpt; // OPTION对象
    // 循环添加OPION元素到年份select对象中
    for (var i =134; i >= 1; i--) {
        if (selObj.options.length != len) { // 如果目标对象下拉框升度不等于设定的长度则执行以下代码
            newOpt = window.document.createElement("OPTION"); // 新建一个OPTION对象
            newOpt.text = Cyear - len + i; // 设置OPTION对象的内容
            newOpt.value = Cyear - len + i; // 设置OPTION对象的值
            selObj.options.add(newOpt, i-134); // 添加到目标对象中
        }

    }
}


function months(){
    var month = document.getElementById("month");
    console.log(month);
    month.length = 0;//删除所有<option>标签
    for (i = 1; i < 13; i++) {
        month.options.add(new Option(i, i));
    }

}

//function ProgramNameChange(PlayTime,callback)
//{
//    var arr = PlayTime.split(":");
//    var now = new Date();
//
//    var date = new Date(now.getFullYear(),now.getMonth(),now.getDate(),arr[0],arr[1],now.getSeconds());
//
//    var isOverTime = date.getTime() < now.getTime();
//
//    return callback(isOverTime);
//
//    //var playTimeStr = date.getFullYear()+"-"+(date.getDate()+1)+date.getDay()+" "+arr[0]+":"+arr[1]+":"+date.getSeconds();
//    //playTimeStr = playTimeStr.replace(/-/g,"\/");
//    //
//    //console.log(PlayTime);
//    //console.log(new Date(playTimeStr).getTime());
//    //console.log(date.getTime());
//    //if(new Date(playTimeStr).getTime() <= date.getTime()){
//    //   obj.style.color="#FF0000";
//    //}
//
//}

function change_date(){
   // var birthday = document.birthday;
    var year  = document.getElementById("year");
    var month = document.getElementById("month");
    var day   = document.getElementById("date");
    vYear  = parseInt(year.value);//解析数值
    vMonth = parseInt(month.value);
    date.length=0;//删除所有<option>标签

    //根据年月获取天数
    var max = (new Date(vYear,vMonth, 0)).getDate();
    for (var i=1; i <= max; i++) {
        date.options.add(new Option(i, i));
    }
}

//window.onload = function()
//{
//    $(".program_play_time").each(function(){
//        var _this = $(this);
//        var time = _this.attr("data-time");
//        //console.log(time);
//        ProgramNameChange(time,function(isOverNow){
//            if(isOverNow){
//                //console.log("change css");
//                _this.css("color","#808080");
//                _this.prev().css("color","#808080");
//                //$(".program_play_time1").css("color","#808080");
//            }
//        });
//    })
//}


