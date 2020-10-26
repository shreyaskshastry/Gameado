import csv
import json
import urllib.request

def get_app_id( json ):
    try:
        return int( json["appid"] )
    except KeyError:
        return 0

def main():
	# Steam API url to get the list of all available apps.
	app_list_url = "http://api.steampowered.com/ISteamApps/GetAppList/v0002/?key=STEAMKEY&format=json"
	response = urllib.request.urlopen( app_list_url )

	# Read the API response (which is in json format) to a json object.
	app_list_json = json.loads( response.read() )

	# All the app related json object is in the `[applist][apps]` array.
	app_list_json = app_list_json["applist"]["apps"]

	# Sort the list by app ids.
	app_list_json.sort( key = get_app_id )

	# Open the csv file and write the csv header.
	out = csv.writer( open( "app_list.csv", "w+", encoding = "utf-8", newline = '' ) )
	out.writerow( ["app_id", "app_title"] )

	# Write the applications data.
	for app in app_list_json:
		out.writerow( [app["appid"], app["name"]] )


if __name__ == "__main__":
	main()