#! coding=utf-8
$(document).ready(function() {

    $.MsgBox = {
        Alert: function (title, msg) {
            GenerateHtml("alert", title, msg);
            btnOk(); //alert只是弹出消息，因此没必要用到回调函数callback
            btnNo();
        },
        Confirm: function (title, msg, callback, href) {
            GenerateHtml("confirm", title, msg);
            btnOk(callback, href);
            btnNo();
        }
    };
    function test(href) {
        window.location.href = href
    }
    $("a[href*='delete']").each(function () {
        $(this).click(function () {
        let href = $(this).attr('href');
        $.MsgBox.Confirm("温馨提示", "确定要进行删除吗", test, href);
        return false
    });
    });
    $("a[id*='testcase_scene_delete']").each(function () {
        $(this).click(function () {
            let id = $(this).attr('id').replace('testcase_scene_delete_', '');
             $.MsgBox.Confirm("温馨提示", "确定要进行删除吗？", delete_scene, id);
        return false
        })
    });
    let GenerateHtml = function (type, title, msg) {
        let _html = "";
        _html += '<div id="mb_box"></div><div id="mb_con"><span id="mb_tit">' + title + '</span>';
        _html += '<a id="mb_ico">x</a><div id="mb_msg">' + msg + '</div><div id="mb_btnbox">';
        if (type === "alert") {
            _html += '<input id="mb_btn_ok" type="button" value="确定" />';
        }
        if (type === "confirm") {
            _html += '<input id="mb_btn_ok" type="button" value="确定" />';
            _html += '<input id="mb_btn_no" type="button" value="取消" />';
        }
        _html += '</div></div>';
        //必须先将_html添加到body，再设置Css样式
        $("body").append(_html);
        //生成Css
        GenerateCss();
    };

    //生成Css
    let GenerateCss = function () {
        $("#mb_box").css({
            width: '100%',
            height: '100%',
            zIndex: '99999',
            position: 'fixed',
            filter: 'Alpha(opacity=60)',
            backgroundColor: 'black',
            top: '0',
            left: '0',
            opacity: '0.6'
        });
        $("#mb_con").css({
            zIndex: '999999',
            width: '400px',
            position: 'fixed',
            backgroundColor: 'White',
            borderRadius: '15px'
        });
        $("#mb_tit").css({
            display: 'block',
            fontSize: '14px',
            color: '#444',
            padding: '10px 15px',
            backgroundColor: '#DDD',
            borderRadius: '15px 15px 0 0',
            borderBottom: '3px solid #009BFE',
            fontWeight: 'bold'
        });
        $("#mb_msg").css({
            padding: '20px',
            lineHeight: '20px',
            borderBottom: '1px dashed #DDD',
            fontSize: '13px'
        });
        $("#mb_ico").css({
            display: 'block',
            position: 'absolute',
            right: '10px',
            top: '9px',
            border: '1px solid Gray',
            width: '18px',
            height: '18px',
            textAlign: 'center',
            lineHeight: '16px',
            cursor: 'pointer',
            borderRadius: '12px',
            fontFamily: '微软雅黑'
        });
        $("#mb_btnbox").css({
            margin: '15px 0 10px 0',
            textAlign: 'center'
        });
        $("#mb_btn_ok,#mb_btn_no").css({
            width: '85px',
            height: '30px',
            color: 'white',
            border: 'none'
        });
        $("#mb_btn_ok").css({
            backgroundColor: '#168bbb'
        });
        $("#mb_btn_no").css({
            backgroundColor: 'gray',
            marginLeft: '20px'
        });
        //右上角关闭按钮hover样式
        $("#mb_ico").hover(function () {
            $(this).css({
                backgroundColor: 'Red',
                color: 'White'
            });
        }, function () {
            $(this).css({
                backgroundColor: '#DDD',
                color: 'black'
            });
        });
        let _widht = document.documentElement.clientWidth; //屏幕宽
        let _height = document.documentElement.clientHeight; //屏幕高
        let boxWidth = $("#mb_con").width();
        let boxHeight = $("#mb_con").height();
        //让提示框居中
        $("#mb_con").css({
            top: (_height - boxHeight) / 2 + "px",
            left: (_widht - boxWidth) / 2 + "px"
        });
    };
    //确定按钮事件
    let btnOk = function (callback, href) {
        $("#mb_btn_ok").click(function () {
            $("#mb_box,#mb_con").remove();
            if (typeof (callback) == 'function') {
                callback(href);
            }
        });
    };
    //取消按钮事件
    let btnNo = function () {
        $("#mb_btn_no,#mb_ico").click(function () {
            $("#mb_box,#mb_con").remove();
        });
    }
});




// 提示信息框

// 删除url中某个参数,并跳转  保证页面只提示一次信息，然后删除url参数
function funcUrlDel(name){
    let href = window.location.href;
    let reg = new RegExp(name + '=[^&]*');

    let href_after = href.replace(reg, '');
    window.history.pushState(null, '', href_after)
}



