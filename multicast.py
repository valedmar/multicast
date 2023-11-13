import argparse, pychromecast
from time import sleep
from pychromecast.controllers.youtube import YouTubeController

# create an empty list lol
CASTS = []

# default video (only the video id)
VIDEO_ID = "coaN2VBNgYA"


parser = argparse.ArgumentParser(
    prog='Multicast',
    description="Cast yt vid to all chromecasts on lan.",
    epilog='-valedmar'
)

parser.add_argument(
    "--known-host",
    help="Add known host (IP), can be used multiple times",
    action="append"
)
parser.add_argument(
    "-v",
    "--videoid",
    help='Youtube video ID (default: "%(default)s")',
    default=VIDEO_ID
)

parser.add_argument(
    '-V',
    "--verbose",
    help='Output extra information',
    action='store_true'
)

args = parser.parse_args()

# if a video link is specified, we override the default.
if args.videoid:
    VIDEO_ID = args.videoid

# check if verbose is enabled
debug = True if args.verbose else False

def discoverChromecasts():
    global browser, CASTS
    # basically, we search the network for all chromecasts
    # in case we specified 1 or more ip adresses with the --known-host flag, we also search those
    # after the search is done, all the devices 'friendly names' is put in a list
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
        print(f"╚═Connecting to {len(chromecasts)} device(s)")

    # for every chromecast we found that we connected to, we actually begin casting to them
    
    for n in range(len(chromecasts)):
        cast = chromecasts[n]
        cast.wait()

        if debug:
            print('casting to: ', cast.device.friendly_name)

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
                                                              valedmar
                                                     
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║   A script to mass cast a youtube video to all chromecast enabled  ║
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

print('░ Halted discovery process, still casting though.')