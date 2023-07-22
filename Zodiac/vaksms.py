import httpx as requests
import tls_client
import pystyle
import threading
import sys
import time
from load import config
from get_discord_headers import getheadersclass


class vakverification:
    def __init__(self, **kwargs):
        self.TOTALTHREADS = kwargs.pop("TOTALTHREADS")
        self.THREADINDEX = kwargs.pop("THREADINDEX")
        self.DISCORDHEADERS = getheadersclass.getheaders(self.TOTALTHREADS, self.THREADINDEX)

        self.OPERATOR = kwargs.pop("OPERATOR")
        self.APIKEY = kwargs.pop("VAKAPIKEY")
        self.COUNTRY = kwargs.pop("VAKCOUNTRY")
        self.BALANCE = None
        self.STOCK = None
        self.PRICE = None
        self.NUMBER = None
        self.TZID = None
        self.VERIFYCODE = None
        self.BANNED = False
        self.DELETED = False
        self.TIMEOUT = requests.Timeout(20.0, read=None)

        def country(self):
            lock = threading.Lock()
            cl = {
                "Denmark": "dk",
                "Estonia": "ee",
                "Finland": "fi",
                "France": "fr",
                "Germany": "de",
                "Hong Kong": "hk",
                "Indonesia": "id",
                "Kazakhstan": "kz",
                "Latvia": "lv",
                "Lithuania": "lt",
                "Mexico": "mx",
                "Netherlands": "nl",
                "Phillipines": "ph",
                "Poland": "pl",
                "Portugal": "pt",
                "Romania": "ro",
                "Russia": "ru",
                "Spain": "es",
                "Sweden": "se",
                "Ukraine": "ua",
                "United Kingdom": "gb",
                "Vietnam": "vn"
            }

            if self.COUNTRY.title() in cl: self.COUNTRY = cl[self.COUNTRY.title()]
            else: lock.acquire(), pystyle.Write.Print(f"\t***Country: {self.COUNTRY} is not supported***\n", pystyle.Colors.red, interval=0), lock.release()
            return self.COUNTRY
        self.COUNTRY = country(self)

    def ordernumber(self):
        url = f"https://vak-sms.com/api/getNumber/?apiKey={self.APIKEY}&service=dc&country={self.COUNTRY}{f'&operator={self.OPERATOR}' if self.OPERATOR != 'any' else ''}&softId=34"
        with requests.Client(headers=None) as client: response = client.get(url).json()
        if 'tel' not in response:
            raise Exception('Failed to retrieve phone number from API')
        self.NUMBER, self.TZID = str(response["tel"]), response["idNum"]
        # self.NUMBER = f"+{self.NUMBER}"
        return self.NUMBER, self.TZID

    def reusenumber(self, NUMBER, TZID):
        url = f"https://vak-sms.com/api/setStatus/?apiKey={self.APIKEY}&status=send&idNum={TZID}"
        response = requests.get(url).json()
        if 'status' in response:
            self.NUMBER = NUMBER
            self.TZID = TZID
        else:
            raise Exception('Failed to change status from API')
        return self.NUMBER, self.TZID
        
    def deletenumber(self):
        url = f"https://vak-sms.com/api/setStatus/?apiKey={self.APIKEY}&status=end&idNum={self.TZID}"
        response = requests.get(url).json()
        if response["status"] != "update": pystyle.Write.Print(f"\t->*** Exception : Number Delete Failed ({response['status']}) ***\n", pystyle.Colors.orange, interval=0)

        # with requests.Client(headers=None) as client: response = client.get(url).json()
        # if response["status"] == "update":  self.DELETED = True
        # return self.DELETED

    def getcode(self):
        waitcount = 0
        session = tls_client.Session(client_identifier="safari_ios_16_0")
        url = f"https://vak-sms.com/api/getSmsCode/?apiKey={self.APIKEY}&idNum={self.TZID}"
        discordurl = "https://discord.com/api/v9/users/@me/phone"

        ratelimited = False
        ratelimit_duration = None
        with requests.Client() as client: response = client.get(url).json()
        while response["smsCode"] is None:
            waitcount += 1

            sys.stdout.write("\r")
            sys.stdout.write(f"\t-> Discord SMS seems stuck. Waiting... {waitcount}/400!")
            sys.stdout.flush()

            with requests.Client(timeout=self.TIMEOUT) as client:
                response = client.get(url).json()
                time.sleep(.3)

            if ratelimited:
                time.sleep(int(ratelimit_duration))

            if waitcount % 5 == 0: # run every x time to request a new sms from discord
                data = {"phone": self.NUMBER, "change_phone_reason": "user_settings_update"}

                discordresponse = session.post(
                    url=discordurl,
                    json=data,
                    headers=self.DISCORDHEADERS
                ).json()

                if "message" in discordresponse:
                    if "message" == "The resource is being rate limited.":
                        ratelimit_duration = discordresponse['retry_after']
                        sys.stdout.write("\r")
                        sys.stdout.write(f"\t-> Ratelimited for requesting a new SMS ({str(ratelimit_duration)} Seconds, trying to get SMS without requesting a new one...")
                        sys.stdout.flush()
                        ratelimited = True

            if waitcount >= 400:
                return "TIMEOUT", False

        self.VERIFYCODE = response["smsCode"]
        return waitcount, self.VERIFYCODE
