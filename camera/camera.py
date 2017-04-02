class InvalidCredentialsException(Exception):
    pass

class CameraLockedException(Exception):
    pass

class Camera:
    def __init__(self, ip_address, username=None, password=None):
        self.ip_address = ip_address
        self.username = username
        self.password = password

        self.Model = None
        self.Firmware = None
        self.MACAaddress = None
        self.SerialNumber = None

        self.login()

    @property
    def Username(self):
        return self.username if self.username is not None else self.default_username

    @property
    def Password(self):
        return self.password if self.password is not None else self.default_password

    def __repr__(self):
        return "{cls}({model}({serial}), {ip}({mac}), {firmware})".format(
                cls=self.__class__.__name__,
                model=self.Model,
                serial=self.SerialNumber,
                ip=self.ip_address,
                mac=self.MACAddress,
                firmware=self.Firmware,
                )
