
    /**
          * @return {string}
          */
     function GetQueryString(name)
        {
             let reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
             let r = window.location.search.substr(1).match(reg);//search,查询？后面的参数，并匹配正则
             if(r != null){
                 return  unescape(r[2]);
             }else {
                 return '';
             }
        }

    function delete_scene(id) {
            let scene_page = GetQueryString('page');
            window.location.href = '{{ url_for("testcase_scene_blueprint.testcase_scene_delete")}}?testcase_scene_id=' + id + '&scene_page=' + scene_page
    }


$(document).ready(function() {

    href = window.location.href.split('/')[3];
    var ths = window.localStorage.getItem(href + '_not_show_ths');
    if( ths != undefined) {
        ths = JSON.parse(ths);
        for (let i = 0; i < ths.length; i++) {
            $('th:contains(' + ths[i] + ')').css('width', '0')
        }
    }

    let config_sql = window.localStorage.getItem('config_sql_content');
    let wait_sql = window.localStorage.getItem('config_wait_content');
    if(config_sql === "0"){
         $('div[class*="config_sql_content"]').each(function () {
                $(this).attr('hidden', 'hidden');
            });
    }else {
        $('div[class*="config_sql_content"]').each(function () {
            $('#config_sql').attr('checked', 'checked')
        });
    }
    if(wait_sql === "0"){
         $('div[class*="config_wait_content"]').each(function () {
                $(this).attr('hidden', 'hidden');
            });
    }else {
        $('div[class*="config_wait_content"]').each(function () {
            $('#config_wait').attr('checked', 'checked')
        });
    }
    let $fullText = $('.admin-fullText');
        $('#admin-fullscreen').on('click', function() {
            $.AMUI.fullscreen.toggle();
        });


    $("td,th",$(this)).hover(function () {
       $(this).attr('title',$(this).text())
    }, function () {
        $(this).removeAttr('title')
    });
     $("td,th").on("click",function() {
            $('#request_body_show').css('overflow','auto').text($(this).text())
    });
    $(".dots",$(this)).hover(function(){
        $(this).attr('title',$(this).text());
    });

        $('table').each(function () {
                var table = $(this).get(0);
                for (j = 0; j < table.rows[0].cells.length; j++) {
                    table.rows[0].cells[j].onmousedown = function() {
                        //记录单元格
                        tTD = this;
                        if (event.offsetX > tTD.offsetWidth - 10) {
                            tTD.mouseDown = true;
                            tTD.oldX = event.x;
                            tTD.oldWidth = tTD.offsetWidth;
                        }
                        //记录Table宽度
                        //table = tTD; while (table.tagName != ‘TABLE') table = table.parentElement;
                        //tTD.tableWidth = table.offsetWidth;
                    };
                    table.rows[0].cells[j].onmouseup = function() {
                        //结束宽度调整

                        if (tTD == undefined) tTD = this;
                        tTD.mouseDown = false;
                        tTD.style.cursor = 'default';
                    };
                    table.rows[0].cells[j].onmousemove = function() {
                        //更改鼠标样式
                        if (event.offsetX > this.offsetWidth - 10)
                            this.style.cursor = 'col-resize';
                        else
                            this.style.cursor = 'default';
                        //取出暂存的Table Cell
                        try {
                              if (tTD == undefined) tTD = this;
                        //调整宽度
                        if (tTD.mouseDown != null && tTD.mouseDown == true) {
                            tTD.style.cursor = 'default';
                            if (tTD.oldWidth + (event.x - tTD.oldX) > 0)
                                tTD.width = tTD.oldWidth + (event.x - tTD.oldX);
                            //调整列宽
                            tTD.style.width = tTD.width;
                            tTD.style.cursor = 'col-resize';
                            //调整该列中的每个Cell
                            table = tTD;
                            while (table.tagName != 'TABLE') table = table.parentElement;
                            for (j = 0; j < table.rows.length; j++) {
                                table.rows[j].cells[tTD.cellIndex].width = tTD.width;
                            }
                            //调整整个表
                            //table.width = tTD.tableWidth + (tTD.offsetWidth – tTD.oldWidth);
                            //table.style.width = table.width;
                        }
                        }catch(e){
                        }

                    };
                }
                });
    function add_col_select() {
        let ths = window.localStorage.getItem(href + '_not_show_ths');
        $('th').each(function () {
            let checked = "";
            try {
                if (ths.indexOf($(this).text()) !== -1) {
                    checked = ""
                } else {
                    checked = "checked"
                }
            } catch (e) {
                checked = "checked"
            }
            $('#layer-content').append(
                "<div class=\"form-group col-md-4 no-padding\" style=\"background-color: #ddd\">\n" +
                "                              <div class=\"col-md-9\" >\n" +
                "                              <label for=" + $(this).text() + "class=\"dots control-label col-md-8\" style=\"font-weight: normal;text-align: left\">" + $(this).text() + "</label>\n" +
                "                              </div>\n" +
                "                              <div class=\"col-md-3\">        " +
                "                              <input   type=\"checkbox\" id=" + $(this).text() + " value=" + $(this).text() + " name=\"layer-th\" style=\"zoom:1.5;width: 20px\" " + checked + ">\n" +
                "                              </div>" +
                "                         </div>");

        });
    }
    function alertMCLayer(layerStr, activeStr) {
         let oLayer = $(layerStr);
        add_col_select();
         //触发弹出蒙层
         $(activeStr).on('click', function () {
             oLayer.css({
                 'display': 'flex',
                 'display': '-webkit-flex',
             })
         });
         oLayer.css({
             'position': 'fixed',
             'left': '0',
             'top': '0',
             'width': '100%',
             'height': '100%',
             'background': 'rgba(0,0,0,0.7)',
             'display': 'none',
             'justify-content': 'center',
             'align-items': 'center',
             'z-index':999
         });
         $('#layer-sub').click(function () {
                 $('#cm_layer').css('display','none');
                 let show_ths = [];
                 $('input[name="layer-th"]').each(function () {
                     let text = $(this).get(0).value;
                    if($(this).attr('checked') != 'checked'){
                        show_ths.push(text);
                       $('th:contains(' + text +')').css('width','0')
                    }else {
                        $('th:contains(' + text +')').css('width','100%')
                    }
                    window.localStorage.setItem(href+'_not_show_ths', JSON.stringify(show_ths));
                 });
             });
        $('#layer-reset').click(function () {
           $('#cm_layer').css('display','none');
           $('#layer-content').empty();
           add_col_select();
        });
     }
    $(function(){
        alertMCLayer('#cm_layer','#btn_alert');
      });
    $('input[id*="config"]').click(function () {
        let name = $(this).attr('id');
        if($(this).attr('checked') === 'checked') {
            $('div[class*='+name + '_content]').each(function () {
                $(this).removeAttr('hidden');
            });
            window.localStorage.setItem(name + '_content', "1")
        }else {
            $('div[class*='+name + '_content]').each(function () {
                $(this).attr('hidden', 'hidden');
            });
            window.localStorage.setItem(name + '_content', "0")
        }
    });

    // 设置提示框淡出时间
    $('.toast__close').click(function(e) {
     $('.toast').stop().fadeOut(1000);
    });
    $('.toast').fadeOut(5000);

    $('.alert').fadeOut(3000);


});


window.onbeforeunload=function(){
    let layout = $('#layout');
    let west = layout.layout('panel','west').css('display');
    let east = layout.layout('panel','east').css('display');
    let south = layout.layout('panel','south').css('display');
    localStorage.setItem('west', west);
    localStorage.setItem('east', east);
    localStorage.setItem('south', south)

};

