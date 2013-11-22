import datetime
from twisted.protocols.basic import LineReceiver


class FritzboxLineReceiver(LineReceiver):
    def __init__(self):
        self.resetValues()

    def resetValues(self):
        self.number = None
        self.caller = None
        self.date = '01011970'
        self.time = '0001'
        self.line = ''
        self.event = None

    def notify(self):
        print("notifyCall(" + self.date + "," + self.number + "," + self.caller + ")")
        self.resetValues()

    def lineReceived(self, line):
        print("[FritzboxLineReceiver] lineReceived: %s" % line)

        # b'21.11.13 22:36:08;RING;0;01606685404;3005988;SIP0;'
        # b'21.11.13 22:36:15;DISCONNECT;0;0;'
        self.line = line
        items = line.decode("utf-8").split(";")

        self.date = items[0]
        self.event = items[1]
        self.number = items[3]

        # TODO Lookup
        self.caller = "Unkown"

        if not self.number:
            print("[FritzboxLineReceiver] no number found")
            self.number = "Number suppressed"
            self.caller = "Unkown"
        self.notify()