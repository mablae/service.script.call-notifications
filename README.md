xbmc.addon.call-notifications
=============================

*Call Notifications* does what the name says:
On incoming phone calls XBMC will show a notification.
It also allows to pause playback or set volume to predefined level.

The idea and parts of code are based on XBMC Yac Listener developed by @doug.

Since he won't update his code anymore I decided to code this thing as a weekend project.

Any feedback and contributions are welcome!

Features:
-----------------------------

 - Support for different clients
 - Set Volume / Mute Volume / Pause Playback on incoming calls
 - Configurable through XBMC Gui
 - i18n Support (English and German so far)
 - Reverse Search for telephone numbers


Client Support:
--------------------------------

 *  [Fritzbox Fon](http://www.avm.de/)

    This is what I use personally. Fritzboxes offer a
    "Callmonitor" Tcp Server on Port 1012.
    This feature needs to be enabled on your Fritzbox by dialing #96*5* with an
    analoge Phone connected to the Fritzbox directly.

 *  [Ncid](http://ncid.sourceforge.net/)  (Network Caller ID)

    Ncid seems to be the standard for unix based CallerID.
    It supports wide range of configurations.

 *  [YAC-Server](http://www.sunflowerhead.com/software/yac/)

    This is the original Application doug used in his addon.


What may be added?
-----------------------------

 * More Clients -> Ideas welcome
 * More Languages
 * CallLog

Credits
-------------------------------

 * doug (Orignal dev of the YAC script)
 * twisted
 * xbmc Community
