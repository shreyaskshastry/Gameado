import csv
import json
import time
import urllib.request
import urllib.parse

APP_LIST_FILE        = "app_list.csv"
USER_DATA_STATE_FILE = "user_data_state.json"
APP_REVIEWS_FILE     = "app_reviews_raw.csv"
USER_REVIEWS_FILE    = "user_reviews_raw.csv"


# Get the program state.
def get_state():
	state = {}
	file_state = {}

	try:
		# Read the state from file.
		with open(USER_DATA_STATE_FILE, 'r') as file:
			file_state = json.load( file )
			state = file_state["state"]
	except FileNotFoundError:
		# Build the default state.
		state["current_index"]       = 0
		state["to_read_index"]       = 104010
		state["reviews_read"]        = 0
		state["max_reviews_to_read"] = 1000

		print( "State file not found, using default state." )

	return state


# Write the program state for future reading.
def write_state( state ):
	write_state = {}

	write_state["state"] = state
	with open(USER_DATA_STATE_FILE, 'w+') as file:
		json.dump(write_state, file, indent = 4)


# Get the list of apps. The function also skips
# the entries that have already been read.
def get_app_list( state ):
	try:
		app_list_file = open( APP_LIST_FILE, 'r', newline = '', encoding = "utf-8" )
		app_list_csv = csv.reader( app_list_file, delimiter = ',' )

		# Skip the header.
		next( app_list_csv, None )

		# Skip the read entries.
		for x in range( state["current_index"] ):
			next( app_list_csv, None )
			
		return app_list_csv
	except Exception as e:
		print( "Failed to open app list file, cannot continue.", e )
		return


def get_entry( json, entry_string ):
	try:
		entry = json[entry_string]
		return entry
	except:
		return "NA"

def read_and_write_data( app_id, app_reviews_csv, user_reviews_csv, state ):
	
	user_reviews_request_url = "https://store.steampowered.com/appreviews/" + str( app_id ) + "?json=1&filter=recent&num_per_page=100&cursor="

	first_page_url = user_reviews_request_url + "*"

	print( "  Reading:", first_page_url )

	response = urllib.request.urlopen( first_page_url )
	review_data = json.loads( response.read() )
	success = bool( review_data["success"] )

	if ( success != True ):
		app_reviews_csv.writerow( [app_id, str( success ), "NA", "NA", "NA", "NA", "NA" ] )
		return

	app_reviews_list = [ app_id, str( success ) ]
	app_reviews_list.append( review_data["query_summary"]["review_score"] )
	app_reviews_list.append( review_data["query_summary"]["review_score_desc"] )
	app_reviews_list.append( review_data["query_summary"]["total_positive"] )
	app_reviews_list.append( review_data["query_summary"]["total_negative"] )
	app_reviews_list.append( review_data["query_summary"]["total_reviews"] )

	app_reviews_csv.writerow( app_reviews_list )

	total_reviews = int( review_data["query_summary"]["total_reviews"] )
	max_reviews_to_read = int( state["max_reviews_to_read"] )

	reviews_to_read = max_reviews_to_read if max_reviews_to_read < total_reviews else total_reviews

	current_page_data = review_data

	while ( True ):
		num_reviews_in_current_page = int( current_page_data["query_summary"]["num_reviews"] )

		if ( num_reviews_in_current_page == 0 ):
			return

		for x in range ( num_reviews_in_current_page ):
			review = current_page_data["reviews"][x]
			author = review["author"]

			user_review_list = [ app_id ]
			user_review_list.append( get_entry( author, "steamid" ) )
			user_review_list.append( get_entry( review, "recommendationid" ) )
			user_review_list.append( get_entry( author, "playtime_forever" ) )
			user_review_list.append( get_entry( author, "playtime_at_review" ) )
			user_review_list.append( get_entry( review, "language" ) )
			user_review_list.append( get_entry( review, "timestamp_created" ) )
			user_review_list.append( get_entry( review, "voted_up" ) )
			user_review_list.append( get_entry( review, "votes_up" ) )
			user_review_list.append( get_entry( review, "votes_funny" ) )
			user_review_list.append( get_entry( review, "weighted_vote_score" ) )
			user_review_list.append( get_entry( review, "comment_count" ) )
			user_review_list.append( get_entry( author, "num_games_owned" ) )
			user_review_list.append( get_entry( author, "num_reviews" ) )

			user_reviews_csv.writerow( user_review_list )

			reviews_to_read -= 1

			if ( reviews_to_read == 0 ):
				return

		cursor = urllib.parse.quote_plus( current_page_data["cursor"] )

		next_page_url = user_reviews_request_url + str( cursor )

		time.sleep( 1.2 )

		print( "    Reading next page:", next_page_url )

		response = urllib.request.urlopen( next_page_url )
		current_page_data = json.loads( response.read() )

def main():
	state = get_state()

	# Check if all entries have been collected.
	if ( state["current_index"] >= state["to_read_index"] ):
		print( "Already collected upto index:", state["to_read_index"] )
		return

	# Get the list of remaining apps.
	app_list = get_app_list( state )
	if app_list is None:
		return

	# Open the output files.
	try:
		app_reviews_file = open( APP_REVIEWS_FILE, "a", encoding = "utf-8", newline = '' )
		user_reviews_file = open( USER_REVIEWS_FILE, "a", encoding = "utf-8", newline = '' )
		app_reviews_csv = csv.writer( app_reviews_file )
		user_reviews_csv = csv.writer( user_reviews_file )
	except Exception as e:
		print( "Failed to open output files:", e )
		return

	# Write the header if new file.
	if ( state["current_index"] == 0 ):
		app_reviews_csv.writerow( ["app_id", "status", "review_score", "review_score_desc", "total_positive", "total_negative", "total_reviews"] )
		user_reviews_csv.writerow( ["app_id", "steam_id", "recommendation_id", "playtime_forever", "playtime_at_review", "language", "timestamp_created", "voted_up", "votes_up", "votes_funny", "weighted_vote_score", "comment_count", "num_games_owned", "num_reviews" ] )

	try:
		for row in app_list:
			if ( state["current_index"] < state["to_read_index"] ):
				print( "state.index =", state["current_index"] )
				read_and_write_data( row[0], app_reviews_csv, user_reviews_csv, state )
				app_reviews_file.flush()
				user_reviews_file.flush()
				state["current_index"] += 1
				time.sleep( 1.2 )
			else:
				break
	except Exception as e:
		print( "Error while reading app data.", e )
	except KeyboardInterrupt:
		print( "Aborting" )

	app_reviews_file.close()
	user_reviews_file.close()

	write_state( state ) 


if __name__ == "__main__":
	main()
