

class NcidClientFactory(ReconnectingClientFactory):
        initialDelay = 20
        maxDelay = 30

        def __init__(self):
                self.hangup_ok = False
        def startedConnecting(self, connector): #@UnusedVariable # pylint: disable=W0613
                if config.plugins.NcidClient.connectionVerbose.value:
                        Notifications.AddNotification(MessageBox, _("Connecting to NCID Server..."), type=MessageBox.TYPE_INFO, timeout=2)

        def buildProtocol(self, addr): #@UnusedVariable # pylint: disable=W0613
                global ncidsrv, phonebook
                if config.plugins.NcidClient.connectionVerbose.value:
                        Notifications.AddNotification(MessageBox, _("Connected to NCID Server"), type=MessageBox.TYPE_INFO, timeout=4)
                self.resetDelay()
                initAvon()
                ncidsrv = NcidCall()
                phonebook = NcidClientPhonebook()
                return NcidLineReceiver()

        def clientConnectionLost(self, connector, reason):
                global ncidsrv
                if not self.hangup_ok and config.plugins.NcidClient.connectionVerbose.value:
                        Notifications.AddNotification(MessageBox, _("Connection to NCID Server lost\n (%s)\nretrying...") % reason.getErrorMessage(), type=MessageBox.TYPE_INFO, timeout=config.plugins.NcidClient.timeout.value)
                ReconnectingClientFactory.clientConnectionLost(self, connector, reason)
                # config.plugins.NcidClient.enable.value = False
                ncidsrv = None

        def clientConnectionFailed(self, connector, reason):
                global ncidsrv
                if config.plugins.NcidClient.connectionVerbose.value:
                        Notifications.AddNotification(MessageBox, _("Connecting to NCID Server failed\n (%s)\nretrying...") % reason.getErrorMessage(), type=MessageBox.TYPE_INFO, timeout=config.plugins.NcidClient.timeout.value)
                ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)
                # config.plugins.NcidClient.enable.value = False
                ncidsrv = None