import base64
import hashlib
import pystyle


def generate_license():
    pystyle.Write.Print("Enter the Device|HD id to genrate license key : ", pystyle.Colors.yellow, interval=0)
    hwid = input()
    salt = "https://github.com/mzeeshanzafar28".encode()
    key = hwid.encode() + salt
    hashed_key = hashlib.sha256(key).digest()
    encoded_key = base64.urlsafe_b64encode(hashed_key)[:16].decode()
    return encoded_key

key = generate_license()
pystyle.Write.Print("[*] LICENSE KEY = " + key, pystyle.Colors.green, interval=0)
pystyle.Write.Print("\n[*] Mod by General ZodX | General ZodX @ YouTube ", pystyle.Colors.cyan, interval=0)