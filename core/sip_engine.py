import pjsua2 as pj
import logging

class Account(pj.Account):
    def __init__(self, engine):
        super().__init__()
        self.engine = engine

    def onRegState(self, p):
        ci = self.getInfo()
        status = "Registered" if ci.regIsActive else "Unregistered"
        logging.info(f"Registration status: {status} (Code: {p.code})")

class Call(pj.Call):
    def __init__(self, acc, call_id=pj.PJSUA_INVALID_ID):
        super().__init__(acc, call_id)
        self.acc = acc

    def onCallState(self, p):
        ci = self.getInfo()
        logging.info(f"Call {ci.id} state: {ci.stateText}")
        if ci.state == pj.PJSIP_INV_STATE_DISCONNECTED:
            self.acc.engine.on_call_disconnected(self)

    def onCallMediaState(self, p):
        ci = self.getInfo()
        for i in range(len(ci.media)):
            if ci.media[i].type == pj.PJMEDIA_TYPE_AUDIO and \
               (ci.media[i].status == pj.PJMEDIA_CONF_CONNECT_READY or \
                ci.media[i].status == pj.PJMEDIA_CONF_CONNECT_ACTIVE):
                m = self.getMedia(i)
                am = pj.AudioMedia.typecastFromMedia(m)
                # Connect call audio to sound device
                pj.Lib.instance().audDevManager().getCaptureDevMedia().startTransmit(am)
                am.startTransmit(pj.Lib.instance().audDevManager().getPlaybackDevMedia())

class SipEngine:
    def __init__(self):
        self.lib = pj.Lib()
        self.lib.init(uaConfig=pj.UaConfig(), logConfig=pj.LogConfig())
        self.lib.createTransport(pj.PJSIP_TRANSPORT_UDP, pj.TransportConfig())
        self.lib.start()
        
        self.acc = None
        self.current_call = None

    def register(self, server, username, password):
        acfg = pj.AccountConfig()
        acfg.idUri = f"sip:{username}@{server}"
        acfg.regConfig.registrarUri = f"sip:{server}"
        cred = pj.AuthCredInfo("digest", "*", username, 0, password)
        acfg.sipConfig.authCreds.append(cred)
        
        self.acc = Account(self)
        self.acc.create(acfg)

    def make_call(self, destination):
        if not self.acc:
            raise Exception("Account not registered")
        call = Call(self.acc)
        prm = pj.CallOpParam(True)
        call.makeCall(destination, prm)
        self.current_call = call
        return call

    def hangup(self):
        if self.current_call:
            prm = pj.CallOpParam(True)
            self.current_call.hangup(prm)
            self.current_call = None

    def on_call_disconnected(self, call):
        if self.current_call == call:
            self.current_call = None

    def __del__(self):
        self.lib.destroy()
