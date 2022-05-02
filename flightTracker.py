import argparse
import requests
import csv
import time
import sys
from os import path

parser = argparse.ArgumentParser(prog='flight tracker', description='Track flights given their icao24 address and save the data to a .csv file')

parser.add_argument('icao', help='the icao24 address')
parser.add_argument('-p', '--path', help='where to save the file (default is the current directory)', default="")
parser.add_argument('-d', '--duration', help='write to file for d seconds (if 0 write forever)', default=0)
parser.add_argument('-t', '--time', help='wait t seconds before requesting again for new data(minimum and default is 5 seconds)', default=5)


def get_data(icao): #returns a dictionary with the data about the aircraft
    print("fetching data...")
    r = requests.get("https://opensky-network.org/api/states/all?icao24=" + icao).json()
    try:
        data = (r['states'][0])
    except TypeError:
        print("No data found")
        return None    
    
    properties = ['icao24', 'callsign', 'origin_country', 'time_position', 'last_contact', 'longitude', 'latitude', 'baro_altitude', 'on_ground', 'velocity', 'true_track', 'vertical_rate', 'sensors', 'geo_altitude', 'squawk', 'spi', 'position_source']
    d = dict(zip(properties, data))

    return d


def write_to_file(savePath, data, duration, sleep_time):
    if duration > 0: 
        t_end = time.time() + float(duration)
    else:
        t_end = sys.maxsize  # loop forever  

    with open(savePath, 'w') as f:
        fieldnames = data.keys() #properties array
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        while time.time() < t_end:
            print('writing to file ', savePath)
            writer.writerow(data)
            time.sleep(int(sleep_time))
            data = get_data(data['icao24'])
            if not data:
                print('data are not available anymore. QUITTING')
                exit(1)

def main():
    args = parser.parse_args()

    file_extension = '.csv'
    if not args.path:
        filename = args.icao + str(round(time.time()))
        path = args.path + filename + file_extension
    else:
        path = args.path  
    icao = args.icao.lower()

    data = get_data(icao)
    if not data:
        exit(1)
    print("aircraft found\n")
    print(data)
    print('Ctrl + C to stop')
    write_to_file(path, data, args.duration, args.time)

if __name__ == "__main__":
    main()