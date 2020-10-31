# Raw Data Folder

The folder contains the raw data collected using Steam Web API. Use the script `get_raw_data.py` to access the raw data from other scripts.

##### Usage [Script]
Suppose the `get_raw_data.py` is located in the folder `xyz/raw_data` relative to the caller script. Then do the following:
```python
relative_get_data_path = "xyz/raw_data"
exec( open( relative_get_data_path + "/get_raw_data.py" ).read() )

# There are 4 different raw datas in the folder, in order to get one of
# them you need to pass the string for the respective data. The string
# names are as follows:
#   - "app_data_raw"     : for application data
#   - "app_list"         : for list of all applications
#   - "app_reviews_raw"  : for the review statistics for each application
#   - "user_reviews_raw" : for player review data for specific application
data_to_get = "app_list"

# The path to the raw datas is writted releative to the `get_raw_data.py`
# script. Therefor you must pass the actual path folder of `get_raw_data.py`
# script to be able to access the data.
# The function below will return the `app_list` data as a string.
raw_data_content = get_raw_data( data_to_get, "xyz/raw_data" )
```

##### Data discription
[TODO]