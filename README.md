微信：15155492421

安装过程：
1：下载https://github.com/yangleiqing0/MyFlask.git  

2：需要下载的安装包:flask_apscheduler requests xlsxwriter flask_wtf wtforms flask_sqlalchemy
flask flask_migrate flask_script flask_mail flask_apscheduler requests flask_sqlalchemy selenium  

3：如果是windows的pycharm，需要将运行时的环境变量设置为Flask环境运行, 命令行的话在app.py目录打开cmd执行python -m flask run -h 0.0.0.0 -p 9000，
如果是linux上部署，需要linux下：commons/tail_font_log.py的 with open(FRONT_LOGS_FILE, 'a', encoding='gbk') as logs:
行里改为encoding='utf-8',将db下的test.sqlite 执行命令mv test.sqlite db\\\test.sqlite再mv ..(linux和windows路径问题导致),
再在app.py层级执行python -m flask run -h 0.0.0.0 -p 9000

4：由于邮件发送的html格式在邮箱解析可能不兼容，需要图片发送的，需要将phantomjs文件放在python路径下，如:C:\Users\NING MEI\AppData\Local\Programs\Python\Python37 
再把文件目录bin下的 phantomjs.exe  复制到python的  Scripts路径下，即安装完毕，由于文件不小，可以自行网上下载，或者联系微信获取,linux相同



使用教程：

1：默认账号admin/admin，只有admin用户可以进行注册用户，每个用户都有自己的配置     

2: 需要先配置请求头部，格式有校验：如 {"Content-Type": "application/json;charset=UTF-8"}  

3：测试用例是最基本的一个测试单元，由请求头部，请求方式，请求报文，请求接口(url),注册变量，正则匹配，数据库验证组成，
可以对测试用例进行添加/编辑/删除/复制/设置模板

4：测试用例场景是集合测试用例作为一个整体，可以对测试用例场景进行执行/复制，在测试场景内进行添加/编辑/删除/复制测试用例，
测试结果也是以测试场景作为一个整体，有一个失败，场景即为失败    

5：测试分组 是可以作为测试用例的集合分组，可以包含测试场景，可用于在测试执行页面执行的一类分组   
 
6：测试报告生成页面和excel，excel可以下载, 在测试报告发送邮件的时候可以选择图片，图片是长截图方式发送

7：关于全局变量，全局变量的格式按照${ZDBM_IP}中的${变量名}，写在请求中，支持名称/URL/请求报文/请求头部,变量均为全局，尽量不要重名，
测试报告的一些主题内容都在全局变量中，以_开头，可根据自己项目更改    
  

8：预期结果的格式  如 ：     包含:123，指请求的响应结果包含123数字

9：定时任务,在测试执行页面选择需要的用例和场景点击添加任务，会自动生成任务，名称是"任务"+当前时间,
cron表达式支持分秒时天月年 如 0 42/10 * * * *  每个小时的42分钟开始执行每过10分钟执行




![](https://github.com/yangleiqing0/test/blob/master/20190819154824.png)
![](https://github.com/yangleiqing0/test/blob/master/20190819131549.png)
![](https://github.com/yangleiqing0/test/blob/master/20190819132150.png)


