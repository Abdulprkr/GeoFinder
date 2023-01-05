import sys                                                                                                                                                                                                          def print_urlhub():
    print("""

   _____            ______ _           _
  / ____|          |  ____(_)         | |
 | |  __  ___  ___ | |__   _ _ __   __| | ___ _ __
 | | |_ |/ _ \/ _ \|  __| | | '_ \ / _` |/ _ \ '__|
 | |__| |  __/ (_) | |    | | | | | (_| |  __/ |
  \_____|\___|\___/|_|    |_|_| |_|\__,_|\___|_|

----- MADE BY ABDUL REHMAN PARKAR & UMAIR MIRZA -----


    """)

if __name__ == "__main__":
    print_urlhub()


from argparse import ArgumentParser
import colorama
import requests
from exif import Image as ImageExif

def main():
    parser = ArgumentParser(description='Image exif data founder')
    parser.add_argument('-u', '--url', help='image url')
    parser.add_argument('-l', '--list', help='list of image urls')
    parser.add_argument('-so', '--simple_output', action='store_true', help='show only url and response')
    args = parser.parse_args()
    if args.url:
        img_url = args.url
        process_image(img_url, args.simple_output)
    elif args.list:
        with open(args.list, 'r') as f:
            for line in f:
                img_url = line.strip()
                process_image(img_url, args.simple_output)

def process_image(img_url, simple_output):
    req = requests.get(img_url, stream=True)
    my_image = ImageExif(req.raw)
    meta_data_list = my_image.list_all()
    found_data = {}
    if my_image.has_exif:
        for key in meta_data_list:
            if 'gps' in key:
                value = my_image.get(key)
                found_data[key] = value
        if 'gps_longitude' in found_data and 'gps_latitude' in found_data:
            if simple_output:
                print(f'{colorama.Fore.LIGHTGREEN_EX}GeoLocation Found{colorama.Fore.RESET}')
                print(f"{colorama.Fore.LIGHTYELLOW_EX}image_url : {colorama.Fore.LIGHTGREEN_EX}{img_url}{colorama.Fore.RESET}")
            else:
                print(f'{colorama.Style.BRIGHT}{colorama.Fore.CYAN}GeoLocation Found{colorama.Fore.RESET}{colorama.Style.RESET_ALL}')
                print(f"{colorama.Fore.LIGHTYELLOW_EX}image_url : {colorama.Fore.LIGHTGREEN_EX}{img_url}{colorama.Fore.RESET}")
                for key, value in found_data.items():
                    print(f'{colorama.Fore.LIGHTYELLOW_EX}{key:30}: {colorama.Fore.LIGHTGREEN_EX}{value}{colorama.Fore.RESET}')
        else:
            print(f'{colorama.Fore.RED}GeoLocation Not Found{colorama.Fore.RESET}')
            print(f'{colorama.Fore.LIGHTYELLOW_EX}image_url : {colorama.Fore.RED}{img_url}{colorama.Fore.RESET}')

if __name__ == '__main__':
    main()
