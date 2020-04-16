import requests
import datetime
import getpass
import xml.etree.ElementTree as ET

subDomain = input("Subdomain:")
url = 'https://{sub}.webex.com/WBXService/XMLService'.format(sub=subDomain)

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

user=input("Username:")
pwd=getpass.getpass("Password:")

doc = CreateXMLBody(subDomain,user,pwd,'291119942020','TEST','Asad blum','asad.blum@wdc.com','40')
headers = {'Content-Type': 'text/xml'}
response =  requests.post(url, data=doc, headers=headers)
xmlResponse = ET.fromstring(response.text)

if response.ok:
    for child in xmlResponse.iter():
        print(child.tag,child.text)

print('************************')
print(response.text)
