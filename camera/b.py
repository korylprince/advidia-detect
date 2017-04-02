import requests
import re
from .camera import Camera, InvalidCredentialsException

b_models = {
        "E921": "B-5360",
        "B95": "B-210",
        "B95A": "B-210",
        }

class BCamera(Camera):

    default_username = "admin"
    default_password = "123456"

    def login(self):
        r = requests.get("http://{ip}/cgi-bin/system?USER={user}&PWD={passwd}&LOGIN&SYSTEM_INFO".format(
            ip=self.ip_address,
            user=self.Username,
            passwd=self.Password,
            ))
        if "ERROR: bad account/password" in r.text:
            raise InvalidCredentialsException("Credentials are invalid")

        model = re.findall("^Model Number = (.*)$", r.text, re.M)[0]
        self.Model = b_models[model]
        self.Firmware = re.findall("^Firmware Version = (.*)$", r.text, re.M)[0]
        self.MACAddress = re.findall("^MAC Address = (.*)$", r.text, re.M)[0]
        self.SerialNumber = re.findall("^Production ID = (.*)$", r.text, re.M)[0]
