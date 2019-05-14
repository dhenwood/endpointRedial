import requests
import xmltodict
import time
from base64 import b64encode


# Replace following details
endpointUsername = "admin"
endpointPassword = "C!sco123"
myMaxTimer = 10         #seconds
cmrAddress = "dhenwood.space@ciscolabs.com"
hostPin = "1234"

myEndpoints = [
        {"addr": "10.20.30.40", "isHost": "false"},
        {"addr": "10.20.30.45", "isHost": "true"}
        ]



authTokenBytes = b64encode(bytes(endpointUsername + ':' + endpointPassword, "utf-8"))
authToken = authTokenBytes.decode('utf-8')

def queryEndpoint(myIpAddr,isHost):
        print("Checking endpoint " + myIpAddr)
        myRequest = requests.get("http://"+myIpAddr+"/status.xml", verify=False, headers={'Authorization': 'Basic '+ authToken})
        if myRequest.status_code == 200:
                xmlData = xmltodict.parse(myRequest.text)
                muteStatus = xmlData['Status']['Audio']['Microphones']['Mute'] #currently not used
                duration = xmlData['Status']['Call']['Duration']
                durationInt = int(duration)
                if durationInt > myMaxTimer:
                        disconnectCall(myIpAddr,isHost)

        else:
                print("Error: "+myIpAddr+" - "+myRequest.reason)


def disconnectCall(myIpAddr,isHost):
        print("disconnecting call")
        xmlMsg = "<Command><Call><Disconnect></Disconnect></Call></Command>"
        myRequest = requests.post("http://"+myIpAddr+"/putxml", verify=False, headers={'Authorization': 'Basic '+ authToken}, data=xmlMsg)
        time.sleep(5)
        callCmr(myIpAddr,isHost)        


def callCmr(myIpAddr,isHost):
        print("Calling CMR " + number)

        xmlMsg = "<Command><Dial><Number>"+cmrAddress+"</Number></Dial></Command>"
        myRequest = requests.post("http://"+myIpAddr+"/putxml", verify=False, headers={'Authorization': 'Basic '+ authToken}, data=xmlMsg)


        
        if myRequest.status_code == 200:
                time.sleep(5)

                for digit in hostPin:
                        print("entering pin " + digit)
                        xmlMsg = "<Command><Call><DTMFSend><DTMFString>"+digit+"</DTMFString></DTMFSend></Call></Command>"
                        myRequest = requests.post("http://"+myIpAddr+"/putxml", verify=False, headers={'Authorization': 'Basic '+ authToken}, data=xmlMsg)
                        time.sleep(1)

                xmlMsg = "<Command><Call><DTMFSend><DTMFString>#</DTMFString></DTMFSend></Call></Command>"
                myRequest = requests.post("http://"+myIpAddr+"/putxml", verify=False, headers={'Authorization': 'Basic '+ authToken}, data=xmlMsg)

        else:
                print("Error: "+myIpAddr+" - "+myRequest.reason)


for endpoint in myEndpoints:
        device = endpoint['addr']
        isHost = endpoint['isHost']

        queryEndpoint(myIpAddr=device, isHost=isHost)   
