# Semic

Semic (Satellite Environmental and Meteorological Information Collect ) is a Python library for collecting weather, environmental data and satellite images from GPS coordinates.

## Instalation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install semic.
```bash
pip install semic
```


## Usage

```python
from semic import DataRequest

obj = DataRequest('./', (200,200))
obj.set_sentinel_param(*user*, *password*,1)

dic = obj.point((1.8, 43.2),2019,2)
print(dic)
print(dic['img_sat'])

obj.to_json(dic, 'point')
```
This will collect all the different data of February 2019 from a tuple (latitude, longitude) and store it in dic.\
The function to_json will save the dictionary as a .json file into the folder indicated as parameter ('./') of the object DataRequest. Images of size (200,200) will be save in the same folder and only their path in the .json file.

```python
from semic import DataRequest

obj = DataRequest(‘./’,(200,200))
obj.set_sentinel_param(*user*, *password*,1)

dic = obj.line([(1.88, 43.26), (1.85, 43.26)], 2019, 2, outputs=['max_temp', 'min_temp', 'avg_temp', 'record_max_temp', 'record_min_temp', 'wind_speed', 'humidity'])

obj.to_json(dic, 'line')
```
This will collect the selected outputs data from a list of GPS coordinates and save it into a json file. 


```python
from semic import DataRequest

obj = DataRequest(‘./’,(200,200))
obj.set_sentinel_param(*user*, *password*,1)

dic = obj.polyline([[(1.88, 43.26), (1.85, 43.26)], [(1.86, 43.15), (1.86, 43.22)]], 2019, 2,23)

obj.to_json(dic, 'line')
```
This will collect data of 23rd Feb. 2019 from a list of list of GPS coordinates.


## License

Semic is open source and licensed under GNU General Public License v3.


