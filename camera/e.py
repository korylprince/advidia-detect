import requests
import json
import urllib
import hashlib
from .camera import Camera, InvalidCredentialsException, CameraLockedException

e_serials = {
	"2M02619": "E-37-V",
        "2J059E2": "E-37-V",
        "2K0173D": "E-37-V",
	}

request_headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }

class ECamera(Camera):

    default_username = "admin"
    default_password = "12345"

    def login(self):
        session, realm, random = self.getAuthParams()
        hash = self.generateHash(session, realm, random)
        self.authenticate(session, hash)
        self.getInfo(session)

    def getAuthParams(self):
        data = {
                "method": "global.login",
                "params": {
                        "userName": self.Username,
                        "password": "",
                        "clientType": "Web3.0",
                        },
                "id": 10000,
            }
        r = requests.post("http://{ip}/RPC2_Login".format(ip=self.ip_address), data=json.dumps(data), headers=request_headers)

        session = r.json()['session']
        realm = r.json()['params']['realm']
        random = r.json()['params']['random']
        return session, realm, random

    def generateHash(self, session, realm, random):
        m1 = hashlib.md5()
        m1.update("{user}:{realm}:{passwd}".format(
            user=self.Username,
            realm=realm,
            passwd=self.Password,
            ).encode('utf-8'))

        m2 = hashlib.md5()
        m2.update("{user}:{random}:{m1}".format(
            user=self.Username,
            random=random,
            m1=m1.hexdigest().upper(),
            ).encode('utf-8'))
        return m2.hexdigest().upper()

    def authenticate(self, session, hash):
        #login
        data = {
                "method": "global.login",
                "params": {
                        "userName": self.Username,
                        "password": hash,
                        "clientType": "Web3.0",
                        },
                "session": session,
                "id": 10000,
            }
        r = requests.post("http://{ip}/RPC2_Login".format(ip=self.ip_address), data=json.dumps(data), headers=request_headers)
        if not r.json()["result"]:
            if r.json()["params"]["error"] == "HasBeenLocked":
                raise CameraLockedException("Camera account has been locked")
            else:
                raise InvalidCredentialsException("Credentials are invalid")

    def getInfo(self, session):
        cookies = {
                "DhWebClientSessionID": str(session),
                "DHLangCookie30": "English",
                }

        data = {
                "method": "system.multicall",
                "params": [
                    {
                        "method": "netApp.getNetInterfaces",
                        "params": "",
                        "session": session,
                        "id": 11,
                    },
                    {
                        "method": "magicBox.getProductDefinition",
                        "params": {
                            "name": "WebVersion",
                            },
                        "session": session,
                        "id": 12,
                    },
                    {
                        "method": "magicBox.getSerialNo",
                        "params": "",
                        "session": session,
                        "id": 13,
                    },
                ],
                "session": session,
                "id": 10,
            }


        r = requests.post("http://{ip}/RPC2".format(ip=self.ip_address), data=json.dumps(data), cookies=cookies, headers=request_headers)

        mapped = {x["id"]:x["params"] for x in r.json()["params"]}
        self.MACAddress = mapped[11]["netInterface"][0]["PhysicalAddress"]
        self.Firmware = mapped[12]["definition"]
        self.SerialNumber = mapped[13]["sn"]
        self.Model = e_serials[self.SerialNumber[:7]]
