from slackclient import SlackClient
import schedule
import time
from datetime import date
from datetime import datetime, timedelta
import requests

token = "xoxb-118976894853-ypenVhWFgnlrfGmHXhrsImeq"
slackClient = SlackClient(token)

def getdate(dateString):
    dateObject = datetime.strptime(dateString, "Date(%Y,%m,%d,%H,%M,%S)")
    return dateObject.strftime("%H:%M")
def job():

    nine_hours_from_now = datetime.now() + timedelta(hours=9)
    todayString = nine_hours_from_now.strftime("%Y-%m-%d")

    url = "http://115.68.116.16/swmaestro/admin/getData1.php?dt="+todayString
    r = requests.get(url).json()
    

    sw = False
    for row in r['rows']:
        if row['c'][1]['v'] == "정성민" or row['c'][1]['v'] == "최평강" or row['c'][1]['v'] == "이종현": 
            print(row)
            sw = True
            stTime = getdate(row['c'][2]['v'])
            edTime = getdate(row['c'][3]['v'])
            roomNum = row['c'][0]['v'] 
            break
    
    roomString = ""
    if sw == True:
        roomString = stTime+"부터 "+edTime+"까지 "+ roomNum+" 입니다."
    else:
        roomString = "없습니다."

    d0 = date.today()
    d1 = date(2017, 7, 23)
    diff = d1 - d0
    d2 = date(2016, 12, 23)
    diff2 = d2 - d0
    text = ("좋은 아침입니다!:computer: \n" +
            "오늘은 " + todayString + "이고, 프로젝트가 " + 
            str(diff.days)+"일("+str(round(diff.days / 204 * 100))+"%) 남았고,\n" +
            "1차 아이디어 평가가 " + str(diff2.days)+"일 남았습니다.\n" + 
            "오늘 예약된 회의는 " + roomString
    )
    slackClient.api_call(
        "chat.postMessage", 
        channel="#testbed", 
        text=text,
        username='hotsan', 
        icon_emoji=':robot_face:'
    )
    return 0

schedule.every().day.at("09:00").do(job)

job()

while True:
    schedule.run_pending()
    time.sleep(1)
