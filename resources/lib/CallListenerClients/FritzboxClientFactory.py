from CallListenerClients.FritzboxLineReceiver import FritzboxLineReceiver
from twisted.internet.protocol import ReconnectingClientFactory



class FritzboxClientFactory(ReconnectingClientFactory):
        initialDelay = 20
        maxDelay = 30
        protocol = FritzboxLineReceiver
        def startedConnecting(self, connector):
                print("Connecting to Fritzbox Callmonitor...")
                # TODO
                #if config.plugins.NcidClient.connectionVerbose.value:
                #        Notifications.AddNotification(MessageBox, _("Connecting to NCID Server..."), type=MessageBox.TYPE_INFO, timeout=2)

        def clientConnectionLost(self, connector, reason):
                #global ncidsrv
                print("Connection to Fritzbox Callmonitor lost\n (%s)\nretrying..." % reason.getErrorMessage())
                #if not self.hangup_ok and config.plugins.NcidClient.connectionVerbose.value:
                #        Notifications.AddNotification(MessageBox, _("Connection to NCID Server lost\n (%s)\nretrying...") % reason.getErrorMessage(), type=MessageBox.TYPE_INFO, timeout=config.plugins.NcidClient.timeout.value)
                ReconnectingClientFactory.clientConnectionLost(self, connector, reason)
                # config.plugins.NcidClient.enable.value = False
                ncidsrv = None

        def clientConnectionFailed(self, connector, reason):
                #global ncidsrv
                print("Connecting to Fritzbox Callmonitor failed\n (%s)\nretrying..." % reason.getErrorMessage())
                #if config.plugins.NcidClient.connectionVerbose.value:
                #        Notifications.AddNotification(MessageBox, _("Connecting to NCID Server failed\n (%s)\nretrying...") % reason.getErrorMessage(), type=MessageBox.TYPE_INFO, timeout=config.plugins.NcidClient.timeout.value)
                ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)
                # config.plugins.NcidClient.enable.value = False
                #ncidsrv = None