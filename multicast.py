import argparse
from time import sleep

import pychromecast
from pychromecast.controllers.youtube import YouTubeController


CASTS = []

# default video
VIDEO_ID = "O-OWdsu2Kmg"


parser = argparse.ArgumentParser(
    description="Cast yt vid to all chromecasts on lan."
)

parser.add_argument(
    "--known-host",
    help="Add known host (IP), can be used multiple times",
    action="append",
)
parser.add_argument(
    "--videoid", help='Youtube video ID (default: "%(default)s")', default=VIDEO_ID
)
args = parser.parse_args()

if args.videoid:
    VIDEO_ID = args.videoid

def discoverChromecasts():
    global browser, CASTS
    devices, browser = pychromecast.discovery.discover_chromecasts(
        known_hosts=args.known_host
    )

    print(f"╔═Discovered {len(devices)} device(s)")
    for device in devices:
        CASTS.append(device.friendly_name)      
    
    chromecasts, browser = pychromecast.get_listed_chromecasts(
        friendly_names=CASTS, known_hosts=args.known_host
    )

    if not chromecasts:
        print(f'╚═No chromecasts connected with the friendly names')
        return
    else:
        print(f"╚═Connected to {len(chromecasts)} device(s)")

    
    for n in range(len(chromecasts)):
        cast = chromecasts[n]
        cast.wait()

        yt = YouTubeController()
        cast.register_handler(yt)
        yt.play_video(VIDEO_ID)

    

print("""                                                                                                     
███╗   ███╗██╗   ██╗██╗  ████████╗██╗ ██████╗ █████╗ ███████╗████████╗
████╗ ████║██║   ██║██║  ╚══██╔══╝██║██╔════╝██╔══██╗██╔════╝╚══██╔══╝
██╔████╔██║██║   ██║██║     ██║   ██║██║     ███████║███████╗   ██║   
██║╚██╔╝██║██║   ██║██║     ██║   ██║██║     ██╔══██║╚════██║   ██║   
██║ ╚═╝ ██║╚██████╔╝███████╗██║   ██║╚██████╗██║  ██║███████║   ██║   
╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚═╝   ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝   ╚═╝   
                                                       valedmar3301
                                                     
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║   A script to mass cast a youtube video to at chromecast enabled   ║
║                        devices on the LAN.                         ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝

""",) 
print('░ casting http://youtube.com/watch?v=' + VIDEO_ID, 'to all available chromecasts')
print('')

try:
    while True:
        discoverChromecasts()
        sleep(5)
except KeyboardInterrupt:
    pass

# Shut down discovery
browser.stop_discovery()

print('░ Halted discovery process, still casting though. Goodluck extracting covertly.')