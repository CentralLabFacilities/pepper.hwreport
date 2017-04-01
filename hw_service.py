import qi
import sys
import time
import subprocess


class PepperHardwareService:
    def __init__(self, *args, **kwargs):
        self.send = qi.Signal()
        self.last_signal = time.time()

    def request(self):
        if time.time() - self.last_signal >= 5.0:
            p = subprocess.Popen(['mpstat', '-u'], stdout=subprocess.PIPE)
            out, err = p.communicate()
            self.send(out)

app = qi.Application(sys.argv)
app.start()
phws = PepperHardwareService()
sess = app.session
the_id = sess.registerService("pepper_hardware_service", phws)
app.run()
