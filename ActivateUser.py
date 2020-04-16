import requests
import datetime
import getpass
import xml.etree.ElementTree as ET

# input params
subDomain = input("Subdomain:")
user=input("Username:")
pwd=getpass.getpass("Password:")
userid =input("User ID for Deactivation:")


# url to post requests
url = 'https://{sub}.webex.com/WBXService/XMLService'.format(sub=subDomain)

def createXMLBody(subDomain, user, password, userid):
    doc = '''<?xml version="1.0" encoding="UTF-8"?>
    <serv:message xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
      <header>
        <securityContext>
          <webExID>{username}</webExID>
          <password>{pwd}</password>
          <siteName>{sub}</siteName>
          <returnAdditionalInfo>true</returnAdditionalInfo>
        </securityContext>
      </header>
      <body>
        <bodyContent xsi:type="java:com.webex.xmlapi.service.binding.user.SetUser">
          <webExId>{id}</webExId>
            <Active>ACTIVATED</Active>
        </bodyContent>
      </body>
    </serv:message>
    '''.format(username=user,pwd=password,sub=subDomain,id=userid)
    return doc

doc =  createXMLBody(subDomain,user,pwd,userid)
headers = {'Content-Type': 'text/xml'}
response =  requests.post(url, data=doc, headers=headers)

if response.ok:
    print(userid," Deactivated Successfully")