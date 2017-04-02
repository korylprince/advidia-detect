import requests
import xml.etree.ElementTree as ElementTree
from .camera import Camera, InvalidCredentialsException

class ACamera(Camera):

    default_username = "admin"
    default_password = "12345"

    def login(self):
        r = requests.get("http://{ip}/ISAPI/System/deviceInfo".format(ip=self.ip_address), auth=(self.Username, self.Password))
        if r.status_code != 200:
            raise InvalidCredentialsException("Credentials are invalid")
        xml = ElementTree.fromstring(r.content)
        self.Model = xml.find("{http://www.std-cgi.com/ver20/XMLSchema}model").text
        self.Firmware = xml.find("{http://www.std-cgi.com/ver20/XMLSchema}firmwareVersion").text
        self.MACAddress = xml.find("{http://www.std-cgi.com/ver20/XMLSchema}macAddress").text
        self.SerialNumber = xml.find("{http://www.std-cgi.com/ver20/XMLSchema}serialNumber").text
