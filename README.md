# flight-tracker-csv
Track flights all around the world and save the data to a .csv file

# How it works
This script uses [OpenSky Network API](https://openskynetwork.github.io/opensky-api/) and requests the following state vectors for an aircraft

|Index|Property|Type|Description|
|----|-----|-------|------------|
0|icao24|string|Unique ICAO 24-bit address of the transponder in hex string representation.|
1|callsign|string|Callsign of the vehicle (8 chars). Can be null if no callsign has been received.|
2|origin_country|string|Country name inferred from the ICAO 24-bit address.|
3|time_position|int|Unix timestamp (seconds) for the last position update. Can be null if no position report was received by OpenSky within the past 15s.|
4|last_contact|int|Unix timestamp (seconds) for the last update in general. This field is updated for any new, valid message received from the transponder.|
5|longitude|float|WGS-84 longitude in decimal degrees. Can be null.
6|latitude|float|WGS-84 latitude in decimal degrees. Can be null.|
7|baro_altitude|float|Barometric altitude in meters. Can be null.|
8|on_ground|boolean|Boolean value which indicates if the position was retrieved from a surface position report.
9|velocity|float|Velocity over ground in m/s. Can be null.|
10|true_track|float|True track in decimal degrees clockwise from north (north=0°). Can be null.
11|vertical_rate|float|Vertical rate in m/s. A positive value indicates that the airplane is climbing, a negative value indicates that it descends. Can be null.
12|sensors|int[]|IDs of the receivers which contributed to this state vector. Is null if no filtering for sensor was used in the request.
13|geo_altitude|float|Geometric altitude in meters. Can be null.|
14|squawk|string|The transponder code aka Squawk. Can be null.
15|spi|boolean|Whether flight status indicates special purpose indicator.
16|position_source|int|Origin of this state’s position: 0 = ADS-B, 1 = ASTERIX, 2 = MLAT, 3 = FLARM

_source:https://openskynetwork.github.io/opensky-api/rest.html#response_

**Because the access to the API is unauthenticated, only the most recent data can be requested**

Also note that not every flying aircraft in the world can be tracked. The OpenSky Network uses [ADS-B](https://en.wikipedia.org/wiki/Automatic_dependent_surveillance_%E2%80%93_broadcast) receivers to obtain this information and some areas may not be covered 

# How to use it
First, you have to obtain the [ICAO24](https://en.wikipedia.org/wiki/Aviation_transponder_interrogation_modes#ICAO_24-bit_address) address of the aircraft either from the [OpenSky Network Aircraft Database](https://opensky-network.org/aircraft-database) or (the easiest way) from [FlightRadar24](https://www.flightradar24.com/data)

Then simply run
```python flightTracker.py icao24_address```

More options
```
  -p PATH, --path PATH  where to save the file (default is the current directory)
  -d DURATION, --duration DURATION write to file for d seconds (if 0 write forever)
  -t TIME, --time TIME  wait t seconds before requesting again for new data(minimum and default is 5 seconds)
```                        

The resulting .csv filename, if not specified, is the icao24 address with the current timestamp
