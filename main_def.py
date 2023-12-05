import requests
import re
import time

vlc_ip = "127.0.0.1"
vlc_port = ''

status_url = f"http://{vlc_ip}:{vlc_port}/requests/status.xml"
playlist_url = f"http://{vlc_ip}:{vlc_port}/requests/playlist.xml"
streamNames = {} 
playlist_ids = {}



REX_PLAYLIST = f'name="([\w\s1]+)"\sid="(\d)'
REX_VOLUME = f'<volume>(\d+)<'
#Tupple (x[0] for x in groups)
#To play playlist:     ?command=pl_play&id=<id>


def send_vlc_command(url, pw, command=None, params=None):
    params = params or {}
    if url == playlist_url:
        vlc_url = playlist_url
    elif url == status_url:
        if command:
            vlc_url = f"{url}?command={command}"
            for key, value in params.items():
                vlc_url += f"&{key}={value}"
        else:
            vlc_url = status_url
    else:
        print("Failed to send Command, No URL provided\nReturning to options.")
    try:
        
        r = requests.get(vlc_url, auth=('', pw))
        r.raise_for_status()
        return r.text
    except requests.RequestException as e:
        print(f"Error: {e}")
        return None

def re_playlist_response(r_value, n):
    groups = re.findall(REX_PLAYLIST, r_value)
    n = n.lower()
    for i in groups:
        if i[0].lower() == n:
            id = i[1]
        
    if id:
        return id
    else:
        return "Could not find playlist id."



def re_volume_response(r_value):
    volume = re.findall(REX_VOLUME, r_value) 
    volume = int(volume[0])
    return volume


def get_vlc_playlist_info(p, n, pw):
    global playlist_url

    playlist_url = f"http://{vlc_ip}:{p}/requests/playlist.xml"

    r_text = send_vlc_command(playlist_url, pw)
    pl = re_playlist_response(r_text, n)
    return pl



def get_stream_info(input, pw):
    streamVolumes = {}
    for key, value in input.items():

        global status_url
        status_url = f"http://{vlc_ip}:{value}/requests/status.xml"
        response = send_vlc_command(status_url, pw)
        volume = re_volume_response(response)
        streamVolumes.update({key: volume})

    return streamVolumes

def change_main_sound(volume, ports, sound_lvl, pw):
    global status_url

    volume = dict(reversed(volume.items()))
    for key, value in volume.items():
        if value != 0 and key != "Main":


            vlc_port = ports[key]
            status_url = f"http://{vlc_ip}:{vlc_port}/requests/status.xml"
            smooth_sound_transfer(value, status_url, pw, "dec")

        elif key == "Main":

            vlc_port = ports[key]
            status_url = f"http://{vlc_ip}:{vlc_port}/requests/status.xml"
            smooth_sound_transfer(value, status_url, pw, "inc", sound_lvl)

        
def smooth_sound_transfer(volume, status_url, pw, direction, sound_lvl=None):
    command = 'volume'
    #300 milliseconds
    pause = (150/10000)
    if direction == "dec":
        while volume != 0:
            param = {'val': "-10"}
            send_vlc_command(status_url, pw, command, param)
            if volume <= 9:
                volume = 0
            else:
                volume = volume -10
                time.sleep(pause)
    elif direction == "inc":
        while volume != sound_lvl:
            if sound_lvl - volume <= 9:
                vol = sound_lvl - volume
                param = {'val': "+{vol}".format(vol=vol)}
                volume = sound_lvl
            else:
                param = {'val': '+10'}
                volume = volume + 10

            send_vlc_command(status_url, pw, command, param)
            time.sleep(pause)


def increment_sound(p, pw):
    global status_url

    vlc_port = p
    status_url = f"http://{vlc_ip}:{vlc_port}/requests/status.xml"
    command = 'volume'
    param = {'val': "+3"}
    send_vlc_command(status_url, pw, command, param)

def decrement_sound(p, pw):
    global status_url

    vlc_port = p
    status_url = f"http://{vlc_ip}:{vlc_port}/requests/status.xml"
    command = 'volume'
    param = {'val': "-3"}
    send_vlc_command(status_url, pw, command, param)

def setup_refresh_commands(p, id, pw):
    global status_url
    #?command=pl_play&id=<id>
    status_url = f"http://{vlc_ip}:{p}/requests/status.xml"
    command = 'pl_play'
    param = {'id': id}
    send_vlc_command(status_url, pw, command, param)