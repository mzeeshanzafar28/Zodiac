import sys
import pystyle
import threading

class initializethreadsclass:
    def initthread():
        with open("files/tokens.txt") as tc:
            tcline = tc.readlines()
            if tcline == []: pystyle.Write.Print("\t-> No Token found inside files/tokens.txt!\n", pystyle.Colors.red, interval=0), sys.exit(69)

        totalthreads = int(pystyle.Write.Input("\t-> Enter No of Threads to use : ", pystyle.Colors.orange, interval=0))
        proxyinput = pystyle.Write.Input("\t-> Proxy Type to implement? http | https | socks5. Hit ENTER to skip: ", pystyle.Colors.orange, interval=0)
        
        if proxyinput == "https": proxyinput = "http"

        return totalthreads, proxyinput
