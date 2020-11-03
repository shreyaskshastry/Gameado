
import pandas as pd
import glob
import os.path

def get_raw_data( name, script_rel_path = "" ):

	file_path = ""

	# Releative path of `get_raw_data.py` script.
	if ( script_rel_path != "" ):
		file_path = script_rel_path + "/"

	# `user_reviews_raw` is handled separately because
	# it's splitted into multiple parts.
	if ( name == "user_reviews" ):
		file_path += "user_reviews_raw/*"

		if ( os.path.exists( "user_reviews_raw.csv" ) != True ):
			new_file = open( "user_reviews_raw.csv", 'w', newline = '', encoding = "utf-8" )

			# Iterate through all user_reviews_data files.
			for part_file_path in glob.glob( file_path ):
				part_file = open( part_file_path, 'r', newline = '', encoding = "utf-8" )
				new_file.write( part_file.read() )
				part_file.close()

			new_file.close()
		return pd.read_csv( "user_reviews_raw.csv", delimiter = ',' )

	# The rest of raw datas are simply stored in a single file.
	if ( name == "app_data" ):
		file_path += "app_data_raw/app_data_raw.csv"
	elif ( name == "app_list" ):
		file_path += "app_list/app_list.csv"
	elif ( name == "app_reviews" ):
		file_path += "app_reviews_raw/app_reviews_raw.csv"

	return pd.read_csv( file_path, delimiter = ',' )
