import requests
import json
import httpx
import tls_client
import time
import sys
import re
import pystyle
import threading
import os
import subprocess
import hashlib
import base64
import pickle
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import date
from gettoken import gettokenclass
from proxy import loadproxyclass
from get_discord_headers import getheadersclass
from hcaptchasolver import bypasscaptcha
from vaksms import vakverification
from fivesim import fivesimverification
from smshub import smshubverification
from load import config


def get_hwid():
    p = subprocess.Popen('wmic csproduct get uuid', stdout=subprocess.PIPE)
    out, _ = p.communicate()
    hwid = out.decode().split('\n')[1].strip()
    return hwid

def generate_license_key(hwid):
    salt = "https://github.com/mzeeshanzafar28".encode()
    key = hwid.encode() + salt
    hashed_key = hashlib.sha256(key).digest()
    encoded_key = base64.urlsafe_b64encode(hashed_key)[:16].decode()
    return encoded_key

def verify_key(key,saved_key):
    if key == saved_key:
        pystyle.Write.Print("\t*** Success ***\n", pystyle.Colors.green, interval=0)
        with open('reg.dat', 'wb') as reg:
            pickle.dump(key, reg)    
        pass   
    else:
        pystyle.Write.Print("\t*** Invalid License Key ***", pystyle.Colors.red, interval=0)
        exit()

def verify(totalthreads, threadindex, proxytype, isRepeating, repetitions):
    HEADERS = getheadersclass.getheaders(totalthreads, threadindex)
    CONFIG = list(config().loadconfig())
    CAPTCHASERVICE = CONFIG[0]
    CAPTCHAPIKEY = CONFIG[1]
    CAPTCHASITEKEY = CONFIG[2]
    PHONESERVICE = CONFIG[3]
    TOTALRETRIES = CONFIG[4]
    OPERATOR = CONFIG[5]
    VAKAPIKEY = CONFIG[6]
    VAKCOUNTRY = CONFIG[7]
    FIVESIMAPIKEY = CONFIG[8]
    FIVESIMCOUNTRY = CONFIG[9]
    SMSHUBAPIKEY = CONFIG[10]
    SMSHUBCOUNTRY = CONFIG[11]
    WEBHOOKURL = CONFIG[12]
    NUMBERREUSE =CONFIG[13]
    
    captcha_required = False
    lock = threading.Lock()
    vaksms = vakverification(
        TOTALTHREADS=totalthreads,
        THREADINDEX=threadindex,
        CAPTCHASERVICE=CAPTCHASERVICE,
        CAPTCHAPIKEY=CAPTCHAPIKEY,
        CAPTCHASITEKEY=CAPTCHASITEKEY,
        PHONESERVICE=PHONESERVICE,
        TOTALRETRIES=TOTALRETRIES,
        OPERATOR=OPERATOR,
        VAKAPIKEY=VAKAPIKEY,
        VAKCOUNTRY=VAKCOUNTRY,
        FIVESIMAPIKEY=FIVESIMAPIKEY,
        FIVESIMCOUNTRY=FIVESIMCOUNTRY,
        SMSHUBAPIKEY=SMSHUBAPIKEY,
        SMSHUBCOUNTRY=SMSHUBCOUNTRY,
        WEBHOOKURL=WEBHOOKURL
    )

    fivesim = fivesimverification(
        TOTALTHREADS=totalthreads,
        THREADINDEX=threadindex,
        CAPTCHASERVICE=CAPTCHASERVICE,
        CAPTCHAPIKEY=CAPTCHAPIKEY,
        CAPTCHASITEKEY=CAPTCHASITEKEY,
        PHONESERVICE=PHONESERVICE,
        TOTALRETRIES=TOTALRETRIES,
        OPERATOR=OPERATOR,
        VAKAPIKEY=VAKAPIKEY,
        VAKCOUNTRY=VAKCOUNTRY,
        FIVESIMAPIKEY=FIVESIMAPIKEY,
        FIVESIMCOUNTRY=FIVESIMCOUNTRY,
        SMSHUBAPIKEY=SMSHUBAPIKEY,
        SMSHUBCOUNTRY=SMSHUBCOUNTRY,
        WEBHOOKURL=WEBHOOKURL
    )

    smshub = smshubverification(
        TOTALTHREADS=totalthreads,
        THREADINDEX=threadindex,
        CAPTCHASERVICE=CAPTCHASERVICE,
        CAPTCHAPIKEY=CAPTCHAPIKEY,
        CAPTCHASITEKEY=CAPTCHASITEKEY,
        PHONESERVICE=PHONESERVICE,
        TOTALRETRIES=TOTALRETRIES,
        OPERATOR=OPERATOR,
        VAKAPIKEY=VAKAPIKEY,
        VAKCOUNTRY=VAKCOUNTRY,
        FIVESIMAPIKEY=FIVESIMAPIKEY,
        FIVESIMCOUNTRY=FIVESIMCOUNTRY,
        SMSHUBAPIKEY=SMSHUBAPIKEY,
        SMSHUBCOUNTRY=SMSHUBCOUNTRY,
        WEBHOOKURL=WEBHOOKURL
    )

    bypasscap = bypasscaptcha(
        CAPTCHASERVICE=CAPTCHASERVICE,
        CAPTCHAPIKEY=CAPTCHAPIKEY,
        CAPTCHASITEKEY=CAPTCHASITEKEY,
        PHONESERVICE=PHONESERVICE,
        TOTALRETRIES=TOTALRETRIES,
        OPERATOR=OPERATOR,
        VAKAPIKEY=VAKAPIKEY,
        VAKCOUNTRY=VAKCOUNTRY,
        FIVESIMAPIKEY=FIVESIMAPIKEY,
        FIVESIMCOUNTRY=FIVESIMCOUNTRY,
        SMSHUBAPIKEY=SMSHUBAPIKEY,
        SMSHUBCOUNTRY=SMSHUBCOUNTRY,
        WEBHOOKURL=WEBHOOKURL
    )

    proxyauth = loadproxyclass().loadproxy(proxytype=proxytype)[0]
    session = tls_client.Session(client_identifier="chrome_108")
    TOKENCOMBO, TOKEN, PASSWORD = gettokenclass.gettoken(totalthreads, threadindex)

    def removetoken():
        with open("files/tokens.txt", "r+") as tokenfile:
            tokenfile.seek(0)
            LINES = tokenfile.readlines()
            if TOKENCOMBO in LINES:
                LINES.remove(TOKENCOMBO)
                tokenfile.seek(0), tokenfile.truncate(), tokenfile.writelines(LINES)
            else: pass
        with open("files/failedverify.txt", "a+") as failedfile: failedfile.write(TOKENCOMBO)

    def removeinvalidtoken():
        with open("files/tokens.txt", "r+") as tokenfile:
            tokenfile.seek(0)
            LINES = tokenfile.readlines()
            if TOKENCOMBO in LINES:
                LINES.remove(TOKENCOMBO)
                tokenfile.seek(0), tokenfile.truncate(), tokenfile.writelines(LINES)
            else: pass
        with open("files/invalidtokens.txt", "a+") as invalidfile: invalidfile.write(TOKENCOMBO)

    def checktoken():
        response = session.get(url="https://discord.com/api/v9/users/@me", headers=HEADERS, proxy=proxyauth if proxytype != "" else None)

        try:
            if response.json()["message"] == "401: Unauthorized":
                removeinvalidtoken()
                pystyle.Write.Print(f"\t-> Token: {TOKEN} is not valid\n", pystyle.Colors.red, interval=0)
                verify(totalthreads, threadindex, proxytype, isRepeating, repetitions)

        except KeyError:
            if "id" in response.json(): lock.acquire(), pystyle.Write.Print(f"\t-> Token {TOKEN} is valid\n", pystyle.Colors.green, interval=0), lock.release()
    checktoken()
    def write_data_to_file(thread_id, number, tzid):
        
        try:
            with open("data.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}

        data[str(thread_id)] = {"number": number, "tzid": tzid}

        with open("data.json", "w") as f:
            json.dump(data, f)
            
    def read_data_from_file(thread_id):
        try:
            with open("data.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}

        thread_data = data.get(str(thread_id), {})
        number = thread_data.get("number")
        tzid = thread_data.get("tzid")
        return number, tzid
        
    if str(NUMBERREUSE).lower() == "true" and isRepeating and str(PHONESERVICE).lower() == "vaksms":
        NUMBER, TZID = read_data_from_file(threadindex)
        NUMBER, TZID = vaksms.reusenumber(NUMBER, TZID)
        NUMBER = f"+{NUMBER}"
        repetitions += 1
        if repetitions > 4:
            isRepeating = False
    elif str(NUMBERREUSE).lower() == "true" and not isRepeating and str(PHONESERVICE).lower() == "vaksms":
        NUMBER, TZID = vaksms.ordernumber()
        write_data_to_file(threadindex, NUMBER, TZID)
        NUMBER = f"+{NUMBER}"
        isRepeating = True
        repetitions = 0
    else:
        if str(PHONESERVICE).lower() == "vaksms": NUMBER, TZID = vaksms.ordernumber()
        elif str(PHONESERVICE).lower() == "fivesim": NUMBER, TZID = fivesim.ordernumber()
        elif str(PHONESERVICE).lower() == "smshub": NUMBER, TZID = smshub.ordernumber(); NUMBER = f"+{NUMBER}"
    def verifiedtoken():
        with open("files/verifiedtoken.txt", "a+") as verifiedfile: verifiedfile.write(TOKENCOMBO)
        with open("files/tokens.txt", "a+") as tokenfile:
            lines = tokenfile.readlines()
            for line in lines:
                if line.strip("\n") != TOKENCOMBO:
                    tokenfile.write(line)
            removetoken()
        lock.acquire(), pystyle.Write.Print(f"\t-> Successfully verified {TOKEN} with {NUMBER}\n", pystyle.Colors.green, interval=0), print(), lock.release()

        if WEBHOOKURL != "":
            webhook = DiscordWebhook(url=WEBHOOKURL, content="<@820352750344077332>", rate_limit_retry=True)
            iconurl = "https://cdn.discordapp.com/avatars/902582070335914064/a_87212f988d5e23f8edb2de2a8162744e.gif?size=1024"
            embed = DiscordEmbed(
                title='New Verified Token!',
                color='03b2f8'
                )

            embed.add_embed_field(name='Token', value=f"`{TOKEN}`", inline=False)
            embed.add_embed_field(name='Number', value=f"`{NUMBER}`", inline=False)
            embed.add_embed_field(name='SMS Code', value=f"`{VERIFYCODE}`", inline=False)
            embed.add_embed_field(name='Captcha Required', value=f"`{captcha_required}`", inline=False)
            embed.set_author(name='twez_verifier', icon_url=iconurl)
            embed.set_footer(text='Discord Token Verifier', icon_url=iconurl)
            embed.set_timestamp()
            webhook.add_embed(embed)
            webhook.execute()
        verify(totalthreads, threadindex, proxytype, isRepeating, repetitions)

    lock.acquire()
    pystyle.Write.Print(f"\t-> Sucessfully equipped Number {NUMBER}\n", pystyle.Colors.green, interval=0)
    lock.release()

    data1 = {"captcha_key": None, "change_phone_reason": "user_settings_update", "phone": NUMBER}
    resp2 = session.post(
        url="https://discord.com/api/v9/users/@me/phone",
        json=data1,
        headers=HEADERS,
        proxy=proxyauth if proxytype != "" else None
    )
    if "captcha_key" in resp2.json():
        if resp2.json()["captcha_key"] == ["You need to update your app to verify your phone number."]:

            lock.acquire()
            pystyle.Write.Print("\t-> Solving captcha now ...This may take a while, please be patient . . .\n", pystyle.Colors.yellow, interval=0)
            lock.release()

            CAPTCHATOKEN = False
            while CAPTCHATOKEN is False:
                CAPTCHATOKEN = bypasscap.hcaptcha()

            data1["captcha_key"] = CAPTCHATOKEN


            resp2 = session.post(
                url="https://discord.com/api/v9/users/@me/phone",
                json=data1,
                headers=HEADERS,
                proxy=proxyauth if proxytype != "" else None
            )

            captcha_required = True

    else:
        lock.acquire()
        pystyle.Write.Print("\t-> Captcha Solving not required... Skipping now \n", pystyle.Colors.yellow, interval=0)
        lock.release()

    lock.acquire()
    if resp2.status_code == 204: pystyle.Write.Print("\t-> Successfully requested verification code \n", pystyle.Colors.green, interval=0)
    lock.release()

    def waitsms():
        waitcount = 0
        retries = 0
        if str(PHONESERVICE).lower() == "vaksms": waitcount, verifycode = vaksms.getcode()
        elif str(PHONESERVICE).lower() == "fivesim": waitcount, verifycode = fivesim.getcode()
        elif str(PHONESERVICE).lower() == "smshub": waitcount, verifycode = smshub.getcode()

        if waitcount == "TIMEOUT":
            retries += 1
            if retries >= TOTALRETRIES:
                pystyle.Write.Print(f"\t-->> Failed to obtain verification code after {TOTALRETRIES} attempts, switching token to continue\n", pystyle.Colors.red, interval=0)
                removetoken()

                if str(PHONESERVICE).lower() == "vaksms": vaksms.deletenumber()
                elif str(PHONESERVICE).lower() == "fivesim": fivesim.deletenumber()
                elif str(PHONESERVICE).lower() == "smshub": smshub.deletenumber()
                verify(totalthreads, threadindex, proxytype, isRepeating, repetitions)

            else:
                pystyle.Write.Print(f"\t-->> Discord didn't sent SMS to {NUMBER}! Trying again with another Number...\n", pystyle.Colors.red, interval=0)
                if str(PHONESERVICE).lower() == "vaksms": vaksms.deletenumber()
                elif str(PHONESERVICE).lower() == "fivesim": fivesim.deletenumber()
                elif str(PHONESERVICE).lower() == "smshub": smshub.deletenumber()
                verify(totalthreads, threadindex, proxytype, isRepeating, repetitions)

        return verifycode
    VERIFYCODE = waitsms()

    if VERIFYCODE is not None:
        lock.acquire(), pystyle.Write.Print(f"\t-> Found Verificationcode: {VERIFYCODE}, sending it to Discord...\n", pystyle.Colors.pink, interval=0), lock.release()
        data2 = {"phone": NUMBER, "code": VERIFYCODE}

        resp4 = session.post(
            url="https://discord.com/api/v9/phone-verifications/verify",
            json=data2,
            headers=HEADERS,
            proxy=proxyauth if proxytype != "" else None
        ).json()
        try: phone_token = resp4["token"]
        except KeyError: phone_token = None



        data3 = {"change_phone_reason": "user_settings_update", "password": PASSWORD.rstrip(), "phone_token": phone_token}
        session.post(
            url="https://discord.com/api/v9/users/@me/phone",
            json=data3,
            headers=HEADERS,
            proxy=proxyauth if proxytype != "" else None
        )

        verifiedtoken()

    elif VERIFYCODE is None:
        lock.acquire(), pystyle.Write.Print(f"\t-> Failed to fetch verification code. Running it again...\n", pystyle.Colors.red, interval=0), lock.release()
        removetoken()
        verify(totalthreads, threadindex, proxytype, isRepeating, repetitions)

if __name__ == "__main__":
    import design
    from init_threads import initializethreadsclass
    

    design.logo()
    hwid = get_hwid()
    saved_key = ""

    json_data = {'hwid' : hwid}
    return_response = requests.post("https://zeetechorg.000webhostapp.com/twez/verify_hwid.php", json=json_data)
    response_content = return_response.text
    # print (response_content)
    if (response_content == 'false'):
        print(pystyle.Write.Input("\n\tLicense not Activated", pystyle.Colors.red, interval=0))
        sys.exit(1)


    # if os.path.isfile('reg.dat'):
    #     try:
    #         with open('reg.dat', 'rb') as reg:
    #             saved_key = pickle.load(reg)
    #     except Exception as ex:
    #         pass
    #     if saved_key == generate_license_key(hwid):
    #         pass
    #     else:
    #         key = input("Enter your license key : ")
    #         verify_key(key, generate_license_key(hwid))

    totalthreads, proxyinput = initializethreadsclass.initthread()
    isRepeating = False
    repetitions = 0
    threads = []
    try:
        for threadindex in range(int(totalthreads)):
            t = threading.Thread(target=verify, args=(int(totalthreads), threadindex, proxyinput, isRepeating, repetitions))
            t.start()
            threads.append(t)
            time.sleep(3)
    except ValueError:
        print(pystyle.Write.Input("\t-> Enter a valid Thread Number!\n", pystyle.Colors.red, interval=0))
        sys.exit(1)