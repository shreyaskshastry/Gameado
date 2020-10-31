
import glob

def get_raw_data( name, script_rel_path = "" ):

	try:
		file_path = script_rel_path + "/"

		if ( name == "user_reviews_raw" ):
			file_path += "user_reviews_raw/*"
			file_data = ""
			for part_file_path in glob.glob( file_path ):
				with open( part_file_path, 'r', newline = '', encoding = "utf-8" ) as file:
					file_data += file.read()
			return file_data

		if ( name == "app_data_raw" ):
			file_path += "app_data_raw/app_data_raw.csv"
		elif ( name == "app_list" ):
			file_path += "app_list/app_list.csv"
		elif ( name == "app_reviews_raw" ):
			file_path += "app_reviews_raw/app_reviews_raw.csv"

		with open( file_path, 'r', newline = '', encoding = "utf-8" ) as file:
			return file.read()
	except Exception as e:
		print( "Failed to open file:", e )