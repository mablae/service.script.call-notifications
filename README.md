xbmc.addon.call-notifications
=============================

What is this?
-----------------------------

XBMC Call Notifications does what the name says:
On Incoming Calls XBMC will show a notification and pause the playback.

The Addon idea and parts of code are based on XBMC Yac Listener developed by @doug.

Since he won't update his code anymore I decided to code this thing as a weekend project.

Features:
-----------------------------

 - Support for different clients
 - Set Volume / Mute Volume / Pause Playback on incoming calls
 - Configurable through XBMC Gui
 - i18n Support (English and German so far)
 - Reverse Search for telephone numbers


Client Support:
____________________________

 - Fritzbox
   This is what I use personally. The Fritzbox offers a "Callmonitor" Tcp Server on Port 1012. However this feature needs to be enabled on your Fritzbox by dialing #96*5* with an Analoge Phone connected to the Fritzbox directly.
 - [Ncid](http://ncid.sourceforge.net/)  (Network Caller ID)
   Ncid seems to be the standard for unix based CallerID. It supports wide range of configurations.
 - YAC-Server


What needs to be done?
-----------------------------