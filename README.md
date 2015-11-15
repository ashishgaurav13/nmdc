nmdc
----
NMDC is Neo Modus' Direct Connect Protocol. Full protocol at http://nmdc.sourceforge.net. This is a python2 implementation of the same. 

How to use
----------
Modify test.py to reflect your hub ip, and provide your own username, password, and an UDP port (for active searches).

```
hc = HubConnection("<hub-ip>", 411 , "<username>", "<password>", "<your-ip>", "<udp-port, optional>")
```
Then do
```
$ python2 test.py
```
After you get the Message of the day and connect notifications (and oplist should be last), a simple search can be done like
```
Find <search terms, spaces allowed>
```
See the search results by ID by doing
```
ShowSearchResults
```
Choose what you want to download (in your head !), and do
```
DownloadById <id>
```
The file should download. For files greater than 10 MB, it might take some time, but the status should be shown. Rest should be fast and easy. Wait until it says exiting client communication mode, and you should be good to go !

Advanced Usage
--------------
To connect to a hub, modify test.py to reflect your own connection status (username, pass, hub ip ...)
Then, in a terminal, do

```
$ python2 test.py
```

This should connect to the preconfigured hub. To search stuff, do

```
Search <your-ip> <udp-port> F?T?0?1?<search-terms>
```

where udp-port is 5005, as in test.py, and search terms have $s instead of spaces. To show the buffer of received commands (`Quit`, `Hello` and `MyINFO` stuff ignored, can be enabled), do

```
Show
```

Search results should be visible via a `Show` command, but if needed to be seen more than once, use `ShowSearchResults` (more work to be done on this). To connect to a client, use

```
ClientConnection <remoteip> <remoteport>
```

Usually this is done after you send a `RevConnectToMe` to it. If you want to be the active side (default and better), after doing a `Search`, send a 

```
ConnectToMe <othernick> <yourip>
```

The port is randomly chosen. You'll start a TCP socket in another thread, and main thread will wait until this thread joins. After the authentication, a file can be simply downloaded like

```
ADCGET file <filename> 0 -1 ZL1
ADCGET tthl <TTH/....> 0 -1 ZL1
```

or even more simply

```
Download <tth> <filesize> <save-file-as> <mode>
```

<save-file-as> should not have spaces (for now). Mode can be 0 for uncompressed, 1 for zlib compressed (LZ77), 2 for bzip2, 3 for doing zlib decompression first, and then bzip2 (for filelists).
To see the format of commands you can use, do

```
ShowCommands
Command <single-command>
Command RevConnectToMe
...
```

Enjoy NMDC ! More to come.
   

To do
-----
1. Create a daemon that can connect to NMDC Hubs (eg VerliHub). This is an intermediary.
2. Create a client downloader program, that uses the daemon, searches stuff and downloads based on the IDs (each search result is assigned an ID).
