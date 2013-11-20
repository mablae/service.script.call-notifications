import datetime
from twisted.protocols.basic import LineReceiver

class NcidLineReceiver(LineReceiver):
        def __init__(self):
                global global_muted
                global_muted = None
                self.resetValues()

        def resetValues(self):
                self.number = None
                self.caller = None
                self.date = '01011970'
                self.time = '0001'
                self.line = ''

        def notifyAndReset(self):
                # notifyCall(self.date, self.number, self.caller)
                self.resetValues()

        def lineReceived(self, line):
                print("[NcidLineReceiver] lineReceived: %s" % line)
                    #200 NCID Server: ARC_ncidd 0.01
                    #CIDLOG: *DATE*21102010*TIME*1454*LINE**NMBR*089999999999*MESG*NONE*NAME*NO NAME*
                    #CIDLOG: *DATE*21102010*TIME*1456*LINE**NMBR*089999999999*MESG*NONE*NAME*NO NAME*
                    #CID: *DATE*22102010*TIME*1502*LINE**NMBR*089999999999*MESG*NONE*NAME*NO NAME*

                    #Callog entries begin with CIDLOG, "current" events begin with CID
                    #we don't want to do anything with log-entries
                if line.startswith("CID:"):
                        line = line[6:]
                        print("[NcidLineReceiver.lineReceived] filtered Line: %s" % line)
                else:
                        return

                items = line.split('*')

                for i in range(0, len(items)):
                        item = items[i]

                        if item == 'DATE':
                                self.date = items[i + 1]
                        elif item == 'TIME':
                                self.time = items[i + 1]
                        elif item == 'LINE':
                                self.line = items[i + 1]
                        elif item == 'NMBR':
                                self.number = items[i + 1]

                date = datetime.strptime("%s - %s" % (self.date, self.time), "%d%m%Y - %H%M")
                self.date = date.strftime("%d.%m.%Y - %H:%M")

                if not self.number:
                        print("[NcidLineReceiver] lineReceived: no number")
                        self.number = _("number suppressed")
                        self.caller = _("UNKNOWN")
                else:
                        if config.plugins.NcidClient.internal.value and len(self.number) > 3 and self.number[0] == "0":
                                debug("[NcidLineReceiver] lineReceived: strip leading 0")
                                self.number = self.number[1:]
                        else:
                                if self.number[0] != '0':
                                        debug("[NcidLineReceiver] lineReceived: add local prefix")
                                        self.number = config.plugins.NcidClient.prefix.value + self.number

                        self.number = stripCbCPrefix(self.number, config.plugins.NcidClient.country.value)

                        debug("[NcidLineReceiver] lineReceived phonebook.search: %s" % self.number)
                        self.caller = phonebook.search(self.number)
                        debug("[NcidLineReceiver] lineReceived phonebook.search reault: %s" % self.caller)
                        if not self.caller:
                                if config.plugins.NcidClient.lookup.value:
                                        NcidReverseLookupAndNotify(self.number, self.caller, self.date)
                                        return                                                        # reverselookup is supposed to handle the message itself
                                else:
                                        self.caller = _("UNKNOWN")

                self.notifyAndReset()

