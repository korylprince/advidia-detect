import hashlib
import requests
from camera import ACamera, BCamera, ECamera, InvalidCredentialsException

class UnknownCameraException(Exception):
    pass

class CameraConnectionError(Exception):
    pass


hashes = {
        "7bde2659cce21d30dcc12aef8076e8a1": ACamera,
        "366c24c5c180d6453c9a7439d05efba2": BCamera,
        "f9b42c69faf52bef44bc81390a43ac04": ECamera,
        }

def detect(ip, username, password, try_default=True):
    try:
        r = requests.get("http://{ip}/".format(ip=ip))
    except requests.exceptions.ConnectionError:
        raise CameraConnectionError("Unable to connect to Camera: IP: {ip}".format(ip=ip))

    h = hashlib.md5()
    h.update(r.text.encode('utf-8'))
    md5sum = h.hexdigest()

    try:
        cls = hashes[md5sum]
    except KeyError:
        raise UnknownCameraException("Unknown Camera Type: IP: {ip}, MD5 Hash: {md5}".format(ip=ip, md5=md5sum))
    
    if try_default:
        try:
            return cls(ip)
        except InvalidCredentialsException:
            return cls(ip, username, password)
    else:
        return cls(ip, username, password)
