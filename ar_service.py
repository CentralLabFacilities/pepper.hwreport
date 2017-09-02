import qi
import re
import sys
import time
# Python compatibility
if (sys.version_info[0] < 3):
    import urllib2
else:
    import urllib.request

# Requires ar_service.config file!
# Example ar_service.config :
# --------
# api=rsb;
# ip=127.0.0.1;
# port=5000;
# --------


class PepperApiReferrerService:
    self.std_api = "ros"
    self.base_link = ""
    
    def __init__(self, *args, **kwargs):
        self.parseConfig()
        self.send = qi.Signal()
        self.last_signal = time.time()
        
    def parseConfig(self):
        config = open("ar_service.config","r")
        config = config.read()
        
        expr = r'api=(.*?);'
        re_res = re.findall(expr, config)
        if ((len(re_res) == 0) or (len(re_res[0]) == 0)):
            pass
        else:
            self.std_api = re_res[0].replace("api=","")
        
        expr = r'ip=(.*?);'
        re_res = re.findall(expr, config)
        if ((len(re_res) == 0) or (len(re_res[0]) == 0)):
            self.base_link = "http://127.0.0.1"
        else:
            self.base_link = "http://" + re_res[0].replace("ip=","")
            
        expr = r'port=(.*?);'
        re_res = re.findall(expr, config)
        if ((len(re_res) == 0) or (len(re_res[0]) == 0)):
            self.base_link = self.base_link + ":5000/api/"
        else:
            self.base_link = self.base_link + ":" + re_res[0].replace("port=","") + "/api/"

    def request(self, api, func):
        if time.time() - self.last_signal >= 5.0:
            if (not api):
                api = self.std_api
            link = self.base_link + api + "/" + func
            # Python compatibility
            if (sys.version_info[0] < 3):
                request = urllib2.Request(link)
                data = urllib2.urlopen(request).read()
            else:
                request = urllib.request.Request(link)
                data = urllib.request.urlopen(request).read()
            self.send(data)

app = qi.Application(sys.argv)
app.start()
pars = PepperApiReferrerService()
sess = app.session
the_id = sess.registerService("pepper_api_referrer_service", pars)
app.run()
