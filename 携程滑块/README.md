https://m.ctrip.com/restapi/soa2/11470/getToken.json  
需要先获取到返回的token  

第一步  
获取滑动图片  
https://ic.ctrip.com/captcha/v4/risk_inspect

"callback": "captcha00899045683872961"  
"extend_param": **`ep`**  
"appid": "100009556"  
"business_site": "search_airticketscivil_online_pic"  
"version": "2.0.4"  
"dimensions": **`dim`**  
"sign": **`sign(_sign)`**  
#####三个加密参数：  
ep:可以固定   
dim:环境参数（修改rt连接的ip，sfp根据token生成）   
sign:将上述参数加在一起进行md5加密  

第二步  
滑动成功，获取点选图片  
https://ic.ctrip.com/captcha/v4/verify_jigsaw

第三步  
点选成功，返回参数  
https://ic.ctrip.com/captcha/v4/verify_icon

selectMoveTrace:可以随机生成一些轨迹（鼠标滑动的轨迹，随意就好）  

第四步
带入参数请求  
https://flights.ctrip.com/itinerary/api/12808/eliminateRisk