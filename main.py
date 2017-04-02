#Usage python main.py in_file.txt username password
import sys
import camera
import detect

in_file = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]

with open(in_file, "r") as f:
    for line in f:
        ip = line.strip()
        try:
            cam = detect.detect(ip, username, password)
        except detect.CameraConnectionError as e:
            print("\t".join((ip, "Connection Error")))
            continue
        except camera.InvalidCredentialsException:
            print("\t".join((ip, "Invalid Credentials")))
            continue
        except camera.CameraLockedException:
            print("\t".join((ip, "Camera Locked")))
            continue

        print("\t".join((cam.ip_address, cam.Model, cam.SerialNumber, cam.MACAddress, cam.Firmware, cam.Username, cam.Password)))
