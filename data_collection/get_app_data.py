import csv
import json
import time
import urllib.request

def write_app_data( app_id, out_csv ):

	MAX_REQUEST_RETRIES = 10000

	app_data_url = "https://store.steampowered.com/api/appdetails/?appids=" + str( app_id )

	print( "  Reading:", app_data_url )

	for x in range( MAX_REQUEST_RETRIES ):
		try:
			response = urllib.request.urlopen( app_data_url )
			break
		except:
			# sleep for 1.2 seconds
			time.sleep( 1.2 )
			MAX_REQUEST_RETRIES -= 1

			if ( MAX_REQUEST_RETRIES <= 0 ):
				print( "Failed to get data from Steam API." )
				return

	app_data = json.loads( response.read() )
	success = app_data[app_id]["success"]

	if success != True:
		out_csv.writerow( [app_id, str( success ), "NA", "NA", "NA", "NA", "NA", "NA", "NA", "NA", "NA", "NA"] )
		return

	add_data_list = [app_id, str( success )]

	app_data = app_data[app_id]["data"]

	add_data_list.append( app_data["name"] )
	add_data_list.append( app_data["type"] )
	add_data_list.append( app_data["required_age"] )

	platforms = []
	if app_data["platforms"]["windows"] == True:
		platforms.append( "windows" )
	if app_data["platforms"]["mac"] == True:
		platforms.append( "mac" )
	if app_data["platforms"]["linux"] == True:
		platforms.append( "linux" )

	seperator = ":"
	platforms = seperator.join( platforms )

	try:
		add_data_list.append( platforms )
		add_data_list.append( app_data["metacritic"]["score"] )
	except:
		add_data_list.append( "NA" )

	try:
		categories = []
		category_ids = []

		for category in app_data["categories"]:
			categories.append( category["description"] )
			category_ids.append( str( category["id"] ) )

		categories = seperator.join( categories )
		category_ids = seperator.join( category_ids )

		add_data_list.append( category_ids )
		add_data_list.append( categories )
	except:
		add_data_list.append( "NA" )
		add_data_list.append( "NA" )

	try:
		genres = []
		genre_ids = []

		for genre in app_data["genres"]:
			genres.append( genre["description"] )
			genre_ids.append( str( genre["id"] ) )

		genres = seperator.join( genres )
		genre_ids = seperator.join( genre_ids )

		add_data_list.append( genre_ids )
		add_data_list.append( genres )
	except:
		add_data_list.append( "NA" )
		add_data_list.append( "NA" )

	try:
		add_data_list.append( app_data["recommendations"]["total"] )
	except:
		add_data_list.append( "NA" )


	out_csv.writerow( add_data_list )


def read_state():
	state = []

	try:
		with open("state.json", 'r') as state:
			state = json.load( state )
	except FileNotFoundError:
		state = '{ "state": { "current_index": 0, "to_read_index": "max_index", "max_index": 104011 } }'
		state = json.loads( state )

	if ( state["state"]["to_read_index"] == "max_index" ):
		state["state"]["to_read_index"] = state["state"]["max_index"]

	if ( state["state"]["to_read_index"] > state["state"]["max_index"] ):
		state["state"]["to_read_index"] = state["state"]["max_index"]

	return state

def write_state( state ):
	with open("state.json", 'w+') as file:
		json.dump(state, file, indent = 4)

def main():
	state = read_state()

	if state["state"]["current_index"] >= state["state"]["to_read_index"]:
		print( "Already collected upto index:", state["state"]["to_read_index"] )
		return

	try:
		with open( "app_list.csv", newline = '', encoding = "utf-8" ) as app_list_file:
			app_list_csv = csv.reader( app_list_file, delimiter = ',' )

			# Skip the header.
			next( app_list_csv, None )

			# Open the csv file and write the csv header.
			out_csv = csv.writer( open( "app_data_raw.csv", "a", encoding = "utf-8", newline = '' ) )

			# Only write the header if we are not appending the file to another.
			if state["state"]["current_index"] == 0:
				out_csv.writerow( ["app_id", "status", "name", "type", "required_age", "platforms", "metacritic_score", "category_ids", "categories", "genre_ids", "genres", "recommendations"] )
			else:
				for x in range( state["state"]["current_index"] ):
					next( app_list_csv, None )

			for row in app_list_csv:
				if state["state"]["current_index"] < state["state"]["to_read_index"]:
					print( "state.index =", state["state"]["current_index"] )
					write_app_data( row[0], out_csv )
					state["state"]["current_index"] += 1
					time.sleep( 1.2 )
				else:
					break
	except Exception as e:
		print( "Error while reading app data.", e )
	except KeyboardInterrupt:
		print( "Aborting" )

	write_state( state )

	return


if __name__ == "__main__":
	main()
