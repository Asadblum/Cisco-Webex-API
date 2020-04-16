import requests
import datetime
import getpass
import xml.etree.ElementTree as ET

# create new webex meeting
def CreateXMLBody(subDomain, username, password, meetingPassword, confName, name, email, duration):
    now = datetime.datetime.now()
    startTime = now.strftime("%m/%d/%Y %H:%M:%S")
    doc = '''<?xml version="1.0" encoding="UTF-8"?>
    <serv:message xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <header>
            <securityContext>
                <siteName>{sub}</siteName>
                <webExID>{user}</webExID>
                <password>{pwd}</password>   
            </securityContext>
        </header>
        <body>
            <bodyContent
                xsi:type="java:com.webex.service.binding.meeting.CreateMeeting">
                <accessControl>
                    <meetingPassword>{mPwd}</meetingPassword>
                </accessControl>
                <metaData>
                    <confName>{cName}</confName>
                    <agenda>Test</agenda>
                </metaData>
                <participants>
                    <maxUserNumber>4</maxUserNumber>
                    <attendees>
                        <attendee>
                            <person>
                                <name>{displayname}</name>
                                <email>{mail}</email>
                            </person>
                        </attendee>
                    </attendees>
                </participants>
                <enableOptions>
                    <chat>true</chat>
                    <poll>true</poll>
                    <audioVideo>true</audioVideo>
                    <supportE2E>TRUE</supportE2E>
                    <autoRecord>TRUE</autoRecord>
                </enableOptions>
                <schedule>
                    <startDate>{start}</startDate>
                    <openTime>900</openTime>
                    <joinTeleconfBeforeHost>true</joinTeleconfBeforeHost>
                    <duration>{dur}</duration>
                    <timeZoneID>4</timeZoneID>
                </schedule>
                <telephony>
                    <telephonySupport>CALLIN</telephonySupport>
                    <extTelephonyDescription>
                        Call 1-800-555-1234, Passcode 98765
                    </extTelephonyDescription>
                </telephony>
            </bodyContent>
        </body>
    </serv:message>   
    '''.format(sub=subDomain,user=username,pwd=password,mPwd=meetingPassword,cName=confName,displayname=name,mail=email,dur=duration,start=startTime)
    return doc


def meetingDetails(subDomain, user, password, meetingKey):

    doc = '''<?xml version="1.0" encoding="ISO-8859-1"?>
    <serv:message
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:serv="http://www.webex.com/schemas/2002/06/service">
        <header>
            <securityContext>
                <siteName>{sub}</siteName>
                <webExID>{username}</webExID>
                <password>{pwd}</password>
            </securityContext>
        </header>
        <body>
            <bodyContent xsi:type="java:com.webex.service.binding.meeting.GetMeeting">
                <meetingKey>{key}</meetingKey>
            </bodyContent>
        </body>
    </serv:message>
    '''.format(sub=subDomain,username=user,pwd=password,key=meetingKey)
    return doc

# input params
subDomain = input("Subdomain:")
user=input("Username:")
pwd=getpass.getpass("Password:")
confName =input("Conf Name:")
duration=input("Meeting Duration:")
# url to post requests
url = 'https://{sub}.webex.com/WBXService/XMLService'.format(sub=subDomain)

doc = CreateXMLBody(subDomain,user,pwd,'291119942020',confName,'Asad blum','asad.blum@gmail.com',duration)
headers = {'Content-Type': 'text/xml'}
response =  requests.post(url, data=doc, headers=headers)
xmlResponse = ET.fromstring(response.text)
# exporting meeting key from the response 
if response.ok:
    for child in xmlResponse.iter():
        if child.tag == "{http://www.webex.com/schemas/2002/06/service/meeting}meetingkey":
            meetingKey = child.text
        if child.tag == "{http://www.webex.com/schemas/2002/06/service/meeting}meetingPassword":
            meetingPassword = child.text
# establishing a new request to get meeting details using meeting key
doc = meetingDetails(subDomain,user,pwd,meetingKey)
response = requests.post(url, data=doc, headers=headers)
xmlResponse = ET.fromstring(response.text)
# exporting meeting details
if response.ok:
    for child in xmlResponse.iter():
        if child.tag == "{http://www.webex.com/schemas/2002/06/service/meeting}meetingLink":
            meetingLink = child.text
        if child.tag == "{http://www.webex.com/schemas/2002/06/service/meeting}guestToken":
            guestToken = child.text
        if child.tag == "{http://www.webex.com/schemas/2002/06/service/meeting}displayMeetingUrl":
            displayMeetingUrl =child.text
#display results
print("======================================")
print("        meeting details               ")
print('======================================')
print('Meeting Link:',meetingLink)
print('Meeting Password:',meetingPassword)
print('Guest Token:', guestToken)
print('Display Meeting URL:',displayMeetingUrl)


