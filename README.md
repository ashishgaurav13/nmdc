NMDCX
------
NMDC is Neo Modus' Direct Connect Protocol. Full protocol at http://nmdc.sourceforge.net.

Usage
-----
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
Download <filename>
Download <TTH/....>
```

Note that this currently works for only small files. You can try doing 

```
Download files.xml.bz2
```

which every client will have. Files are compressed using zlib's LZ77 algorithm, and are not decompressed automatically (to do). Use 

```
(openssl -d <compressed>) > uncompressed 
```

to do this. One more trick, files.xml.bz2 after zlib decompression, also need to go through a bzip2 decompression, which can be done via

```
bzip2 -d <last-file>
```

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
1. Create a daemon that can connect to DC Hubs. This is an intermediary.
2. Create a client downloader program, that uses the daemon, searches stuff and downloads based on the IDs (each search result is assigned an ID).
