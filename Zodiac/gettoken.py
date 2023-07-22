import time
import sys
import pystyle


class gettokenclass:

    def gettoken(totalthreads, threadindex):
        with open("files/tokens.txt", "a+") as tokenfile:
            tokenfile.seek(0)
            LINES = tokenfile.readlines()
            TOKENCOMBO = []

            for I, TOKENCOMBO in enumerate(LINES):
                if I%totalthreads == threadindex:
                    if ":" in TOKENCOMBO: break

            if TOKENCOMBO == []: pystyle.Write.Print(f"\t-> tokens.txt contains no more usable tokens\n", pystyle.Colors.red, interval=0), time.sleep(2), sys.exit(0)
            elif ":" not in TOKENCOMBO: pystyle.Write.Print("\t-> Incorrect Token Format inside tokens.txt , Correct Format => token:password\n", pystyle.Colors.orange, interval=0), sys.exit(1)

            EMAIL, PASSWORD, TOKEN = TOKENCOMBO.split(":")
        return TOKENCOMBO, TOKEN, PASSWORD
