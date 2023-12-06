# VLC_Restream_Helper
This is the assist with volume control on VLC for restreams, with ability to refresh a stream to within usually 4-5 seconds slower as a stream would appear in your browser.  


The initial version still needs a lot of work, but it works to start testing to see what people like. The Gui is hideous and does have a scroll bar yet so the window has to be dragged  bigger to see all the buttons.  

I have also not tested on smaller screens so no idea how it looks there yet as I only have tested it on my own larger screens.  

High Priority work:  
Better Error logging so its easier for people to understand what might be going wrong.  
Make UI better and not so hideous.  
Testing on Linux/Mac to make sure it works as its just using default python libraries.  

Low Priority work:  
Make it more dummy proof.  
Fix tabbing index.  
Maybe be able to dynamically pull in stream info.  



# Extra Info

This is tested with Streamlink through the cli. (No idea what other stuff is out there so it may work on others as all the command go straight to VLC).  

It uses the HTTP protocal using the loop back address, with the LUA enabled through VLC Gui to enable password connection for security reasons.  

Only allows for 4 streams max at this moment. Though you can use it with 1,2,3 or 4 streams.    

When changing the main volume, it will smoothy change the volume at a rate of 3.90625% every 0.015 seconds + code time.


# Setup

1)
  You can either download the release and just run the Gui.exe (Will rename later).  
  NOTE: I did not sign the intial executable so windows might balk at it.  
  
  Or you can run the gui.py executable with the main_def.py in the same folder location.  
  NOTE: I only used the default python libraries so there isn't any libraries that need to be installed.  

2)
  In the VLC gui, you will need to go to:  
  Tools > Preferences > Interface > Main Interfaces > Check the Lua Interpreter option.  
  
  Then expand Main Interfaces > Lua > Set a password under the Lua HTTP area.  



# How to use

1) 
  When launching the twich streams, you will need to use the CLI to set the options that are needed. The extra cli options are:  
  --extraintf=http  
  --http-port [port]  
IMPORTANT:  
  You will need to replace [port] with a unique port number for every one of the streams you are using. I suggest using 8080-8083 as they are common ports and 8080 is alternative http.  
  You should also make sure you firewall allows the connection from the python script or executable to vlc on those ports.  
  While also making sure that nothing else can connect to the VLC player for extra security. Chances are slim that some malicious actor would use this, but since you are setting up the firewall rules anyway, you might as well.  

Example commands using Streamlink are:  
Streamlink -p "C:\Program Files\VideoLAN\VLC\vlc.exe" -a "--extraintf=http --http-port 8080 --meta-title 'Player 1'" https://twitch.tv/P1Stream best --twitch-disable-ads  
Streamlink -p "C:\Program Files\VideoLAN\VLC\vlc.exe" -a "--extraintf=http --http-port 8081 --meta-title 'Player 2'" https://twitch.tv/P2Stream best --twitch-disable-ads  
Streamlink -p "C:\Program Files\VideoLAN\VLC\vlc.exe" -a "--extraintf=http --http-port 8082 --meta-title 'Player 3'" https://twitch.tv/P3Stream best --twitch-disable-ads  
Streamlink -p "C:\Program Files\VideoLAN\VLC\vlc.exe" -a "--extraintf=http --http-port 8083 --meta-title 'Player 4'" https://twitch.tv/P4Stream best --twitch-disable-ads  

2)
  When you launch the gui.exe or gui.py, the first thing you should do is fill in the password in the password field in the upper left. Nothing will work without it.   
  NOTE: Remember to set that password from step 2 of Setup.  

3) 
  When filling out the rest:

  REQUIRED for everything:  
  Port = This is the http-port you set in the cli when starting Streamlink. Make sure you have the right port for the right stream.  

  REQUIRED for sound manipulation:  
  Sound % = The percent value of the sound level in VLC, you can adjust it manually and then type in the number or just type in 100 and go from there.  
  
  DO NOT add % at the end of the number as it is not currently checking for the % to remove it.  
  NOTE: This will not work unless there is a value present for the stream you are trying to change.  
  NOTE 2: The sound can go up to 200% but does not allow you to go past that as using the http commands you can go higher then 200%, but I have no idea how stable that is so I capped it at the normal 200%.  

  REQUIRED for stream refresh:  
  Stream Name Metadata = This is the --meta-title you set in the cli when starting the streams. It is not case sensitive but needs to match exactly besides that.  

Example filled out below.  
![image](https://github.com/Pyre-Echo/VLC_Restream_Helper/assets/20142822/0e49d187-89af-45e5-a021-84a7c623a3df)  


4) 
  To refresh the stream you will need to check the Refresh Stream checkbox to get those buttons to pop up. I have done that to prevent accidental stream refreshes.  
  NOTE: This will make the stream freeze once and maybe twice before it gets back going. Usually takes about 4-5 seconds and then when finished, its usually ~4-5 seconds behind what the stream would be at on your browser.

NOTE 2: Recommend you only use this if they are a significant distance behind what they should be like 20+ seconds. But the restreamers in charge of your community will tell you what they are comfortable with to catch things up for the restream.  




# Bonus Info on perplexities on use.  

1) You will not be able to inc or dec sound volume on streams that are at 0% volume to prevent accidental adjustments to the wrong stream.  

2) When the stream is the main volume, the sound % will increment and decriment when using the respective buttons. BUTT Even tho the documentation I can change by %, I was not able to get it to work so I have to convert to a specific decimal value, so when rounding you may see it skip a percent every once and a while when changing volume.  

3) Sound decimal values are 256 = 100% sound, 512 = 200% sound.  


Any questions feel free to ask me on the Free Enterprise discord in the #tools-and-projects channel.  



#Troubleshooting

Since it has crappy error logging, here is a couple things to look out for.  

1)  
  If trying to change the sound, check the VLC messages area in I think tools for any error messages they may be seeing.  

2)  
   Check the cmdline window that is open for any errors, they will be python error messages but might give you a clue.  

3)  
  Make sure your password is in the field with the correct port and meta data name.
  NOTE: Password is case sensitive.  

5)  
  Check your firewall event logs to see if any of the connections are being blocked by that.  


  
