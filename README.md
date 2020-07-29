# Semic

Semic (Satellite Environmental and Meteorological Information Collect ) is a Python library for collecting weather, environmental data and satellite images from GPS coordinates.

## Installation

If you want to collect Sentinel2 image data you will need to install :\
* rasterio (https://rasterio.readthedocs.io/en/latest/installation.html)\
* OpenJPEG (https://www.openjpeg.org/)\
We invite you to follow the official installation guides.\ 
You will also need a valid SciHub-Copernicus free account, you can create it at : https://scihub.copernicus.eu/dhus/#/self-registration

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install semic.
```bash
pip install semic
```

## Usage
### Import library and create an object.

```python
from semic import DataRequest

obj = DataRequest('./', (200,200))
```

| parameter | description |
|:---------------|:---------------:|
| path_to_folder (str) | The path where you will save the data |
| size_img (tuple of int) | The size of returned images |


### Set Sentinel2 parameters.

```python
obj.set_sentinel_param(user, password, 1)
```
| parameter | description |
|:---------------|:---------------:|
| user (str) | Username of Sentinel account |
| pwd (str) | Password of Sentinel account |
| width (int) | Size in km of the zone (a square) you want to capture around the GPS coord |
| nb_of_tile (int, default = 1) | The number max of tiles a sentinel query will return |
| path_to_sentinel (str, default = './') | Path where Sentinel2 tiles will be downloaded |
| tile_name (str, default = None) | Sentinel query with the specific name of a tile |
| dl_option (str, default = 'n') | Can be 'y' or 'i'. If you find a tile that has not been already downloaded you can choose if you want to do it (y) or not (n) or his you want to interact and choose later (i) |
| cloudcover (tuple, default = (0,10)) | Cloudcover percentage for Sentinel images |

If you want to do the process without Sentinel2 data you just don’t set its parameters.


### Search data from GPS coordinates and date

```python
dic = obj.point((1.8, 43.2), 2019, 2)
```

| parameter | description |
|:---------------|:---------------:|
| coords (tuple) | GPS coordinates (longitude, latitude) |
| year (int) | Year for the weather |
| month (int, default = None) | Month for the weather |
| day (int, default = None) | Day for the weather |
| outputs (list, default = all the possible outputs) | outputs wanted |


List of available outputs :
- 'max_temp' : maximum temperature in °C (d)
- 'min_temp' : minimum temperature in °C (d)
- 'avg_temp' : average temperature in °C (m/y)
- 'record_max_temp' : highest temperature in °C (m/y)
- 'record_min_temp' : lowest temperature in °C (m/y)
- 'wind_speed' : average wind speed in km/h (d/m/y)
- 'humidity' : humidity in % (d/m/y)
- 'visibility' : visibility in km (d/m/y)
- 'cloud_coverage' : cloud coverage in % (d/m/y)
- 'heat_index' : heat index (d/m/y)
- 'dew_point_temp' : dew point in °C (d/m/y)
- 'pressure' : pressure in hPa (d/m/y)
- 'sunrise_time' : sunrise time in hour:minute:second (d/m/y)
- 'sunset_time' : sunset time in hour:minute:second (d/m/y)
- 'day_length' : day length in hour:minute:second (d/m/y)
- 'rainfall' : total rainfall in mm (d/m/y)
- 'avg_rainfall_per_day' : average rainfall per day in mm (m/y)
- 'record_rainfall_day' : highest rainfall in mm (m/y) 
- 'img_plan' : PIL map image of the zone near the point (d/m/y)
- 'img_sat' : PIL satellite image of the zone near the point (d/m/y)
- 'elevation' : elevation of the point (d/m/y)
- 'img_sentinel : PIL image of the zone taken in Sentinel2 data (d/m/y)
- 'city' : Nearest city of the GPS point (d/m/y)

### Save data

```python
obj.to_json(dic, 'point')
```

| parameter | description |
|:---------------|:---------------:|
| dic (dict) | Dictionary containing the to be save |
| name (str) | Name of the .json file created |
| sort (bool, default = True) | Sort the keys in alphabetical order or not|



The previous codes collect all the different data of February 2019 from a tuple (longitude, latitude) and store it in dic.\
The function to_json will save the dictionary as a .json file into the folder indicated as parameter ('./') of the object DataRequest. Images of size (200,200) will be save in the same folder and only their path in the .json file.

## Examples

```python
from semic import DataRequest

obj = DataRequest('./', (200,200))
obj.set_sentinel_param(user, password, 1)

dic = obj.line([(1.88, 43.26), (1.85, 43.26)], 2019, 2, outputs=['max_temp', 'min_temp', 'avg_temp', 'record_max_temp', 'record_min_temp', 'wind_speed', 'humidity', 'img_sat'])
print(dic)
```
> {'avg_temp': 10.0,\
> 'record_max_temp': 23.0,\
> 'record_min_temp': 9.0,\
> 'max_temp': 14.0,\
> 'min_temp': 5.0,\
> 'wind_speed': 21.0,\
> 'humidity': 76.0,\
> 'img_sat': <PIL.Image.Image image mode=RGB size=200x200 at 0x20C0F7D55F8>}
```python
dic['img_sat'].show()
```
![img_sat](./images/img_sat.png?raw=true "Satellite image")

```python
obj.to_json(dic, 'line')
```

This will collect the selected outputs data of February 2019 from a list of GPS coordinates and save it into a json file. 
The only different parameter from _point_ to _line_ function is ‘coords’ which need to be a list of coordinates in _line_

```python
from semic import DataRequest

obj = DataRequest('./',(200,200))
obj.set_sentinel_param(user , password ,1)

dic = obj.polyline([[(1.88, 43.26), (1.85, 43.26)], [(1.86, 43.15), (1.86, 43.22)]], 2019, 2, 23)

obj.to_json(dic, 'line')
```
This will collect data of 23rd Feb. 2019 from a list of list of GPS coordinates.
The parameters are once again the same except ‘coords’ which is now a list of list of coordinates.


## License

Semic is open source and licensed under GNU General Public License v3.


