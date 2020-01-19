import bs4
from bs4 import BeautifulSoup
import re
from urllib.request import urlopen as uReq
import time
import datetime
import pandas as pd
from collections import defaultdict
import sqlite3
import lxml



wave_height_list = ['0.1 ft','0.2 ft','0.3 ft','0.4 ft','0.5 ft','0.6 ft','0.7 ft','0.8 ft','0.9 ft',
						'1.1 ft', '1.2 ft', '1.3 ft', '1.4 ft', '1.5 ft', '1.6 ft', '1.7 ft', '1.8 ft','1.9 ft',
						'2.0 ft','2.3 ft','2.4 ft','2.5 ft','2.6 ft','2.7 ft','2.8 ft','2.9 ft']


wave_interval_list = ['1 sec', '2 sec', '3 sec', '4 sec', '5 sec', '6 sec', '7 sec']


wind_direction_list = ["SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]


def current_date_time():
	# Current Time 
	#Grab current date/time (24 hr format, includes seconds)
	current_time_AM_PM = datetime.datetime.now()
	#12-hour format
	current_time_sliced = current_time_AM_PM.strftime('%Y/%m/%d %I:%M%p')
	# separating Date from Time (DD/MM/YYY HH/MM)
	date_today = current_time_sliced.split(' ')
	date_ = date_today[0]
	time_ = date_today[1]
	# Removing first letter if it's '0', so it doesn't read as '08:07pm', etc
	if time_[0]=="0":
		time_ = time_[1:]

	print("Date:", date_)
	print("Current Time:", time_)
	print("Location: Boston Harbor")
	time.sleep(1)
	print("\n")


# This function retrieves the wave height
def surf_info_finder():
	#List of ndbc.noaa.gov URLs to scrape from
	my_url = [
	#Boston Buoy [0]
	'https://www.ndbc.noaa.gov/station_page.php?station=44013',
	#North Carolina Buoy [1] (Outer Banks)
	'https://www.ndbc.noaa.gov/station_page.php?station=41025',
	#North Carolina Buoy #2 [2] (first NC URL is incomplete: missing wave interval, wave height )
	'https://www.ndbc.noaa.gov/station_page.php?station=44095',
	#Main Buoy [3]
	'https://www.ndbc.noaa.gov/station_page.php?station=44007',
	#Rhode Island Buoy [4]
	'https://www.ndbc.noaa.gov/station_page.php?station=buzm3',
	#Rhode Island Buoy [5] (first RI URL is incomplete: missing wave interval, wave height )
	'https://www.ndbc.noaa.gov/station_page.php?station=44097'
	]

	page_soups = []

	for url in my_url:
	#initiating python's ability to parse URL
		uClient = uReq(url)
	# this will offload our content in'to a variable
		page_html = uClient.read()
	# closes our client
		uClient.close()
		page_soup = BeautifulSoup(page_html, "html.parser")

		page_soups.append(page_soup)
	return page_soups
		

def wave_height_printer():
		#List of Parsed HTMLs via my_url List
		page_soups_ = surf_info_finder()

		wave_list = []

		boston_wave_height = page_soups_[0].find('td', string='Wave Height (WVHT):').find_next_sibling().get_text().strip()
		nc_wave_height = page_soups_[2].find('td', string='Wave Height (WVHT):').find_next_sibling().get_text().strip()
		maine_wave_height = page_soups_[3].find('td', string='Wave Height (WVHT):').find_next_sibling().get_text().strip()
		ri_wave_height = page_soups_[5].find('td', string='Wave Height (WVHT):').find_next_sibling().get_text().strip()

		wave_list.append(boston_wave_height)
		wave_list.append(nc_wave_height)
		wave_list.append(maine_wave_height)
		wave_list.append(ri_wave_height)

		return wave_list

		# print("Current Boston Wave Height:" + boston_wave_height)
		# print("Current NNC Wave Height:" + nc_wave_height)


def wave_interval_printer():
	page_soups_ = surf_info_finder()

	wave_interval_list = []

	boston_wave_interval = page_soups_[0].find('td', string='Dominant Wave Period (DPD):').find_next_sibling().get_text().strip()
	nc_wave_interval = page_soups_[2].find('td', string='Dominant Wave Period (DPD):').find_next_sibling().get_text().strip()
	try:
		maine_wave_interval = page_soups_[3].find('td', string='Dominant Wave Period (DPD):').find_next_sibling().get_text().strip()
	except AttributeError:
		maine_wave_interval = "None"

	ri_wave_interval = page_soups_[5].find('td', string='Dominant Wave Period (DPD):').find_next_sibling().get_text().strip()

	wave_interval_list.append(boston_wave_interval)
	wave_interval_list.append(nc_wave_interval)
	wave_interval_list.append(maine_wave_interval)
	wave_interval_list.append(ri_wave_interval)

	return wave_interval_list

	# print("Current Boston Wave Interval:" + boston_wave_interval)
	# print("Current NC Wave Interval:" + nc_wave_interval)


def wind_direction_printer():
	page_soups_ = surf_info_finder()

	wind_direction_list = []

	boston_wind_direction_fullstring = page_soups_[0].find('td', string='Wind Direction (WDIR):').find_next_sibling().get_text().strip()
	nc_wind_direction_fullstring = page_soups_[1].find('td', string='Wind Direction (WDIR):').find_next_sibling().get_text().strip()
	maine_wind_direction_fullstring = page_soups_[3].find('td', string='Wind Direction (WDIR):').find_next_sibling().get_text().strip()
	ri_wind_direction_fullstring = page_soups_[4].find('td', string='Wind Direction (WDIR):').find_next_sibling().get_text().strip()

	boston_wind_direction_ = boston_wind_direction_fullstring.split('(')
	boston_wind_direction = boston_wind_direction_[0]

	nc_wind_direction_ = nc_wind_direction_fullstring.split('(')
	nc_wind_direction = nc_wind_direction_[0]

	maine_wind_direction_ = maine_wind_direction_fullstring.split('(')
	maine_wind_direction = maine_wind_direction_[0]

	ri_wind_direction_ = ri_wind_direction_fullstring.split('(')
	ri_wind_direction = maine_wind_direction_[0]

	wind_direction_list.append(boston_wind_direction)
	wind_direction_list.append(nc_wind_direction)
	wind_direction_list.append(maine_wind_direction)
	wind_direction_list.append(ri_wind_direction)

	return wind_direction_list



def wind_speed_printer():
	page_soups_ = surf_info_finder()

	wind_speed_list = []

	boston_wind_speed = page_soups_[0].find('td', string='Wind Speed (WSPD):').find_next_sibling().get_text().strip()
	nc_wind_speed = page_soups_[1].find('td', string='Wind Speed (WSPD):').find_next_sibling().get_text().strip()
	maine_wind_speed = page_soups_[3].find('td', string='Wind Speed (WSPD):').find_next_sibling().get_text().strip()
	ri_wind_speed = page_soups_[4].find('td', string='Wind Speed (WSPD):').find_next_sibling().get_text().strip()

	wind_speed_list.append(boston_wind_speed)
	wind_speed_list.append(nc_wind_speed)
	wind_speed_list.append(maine_wind_speed)

	return wind_speed_list

	# print("Current Boston Wind Speed:" + boston_wind_speed)
	# print("Current NC Wind Speed:" + nc_wind_speed)


def wind_speed_splicer():
	page_soups_ = surf_info_finder()

	wind_speed_abbreviated_list = []

	boston_wind_speed = page_soups_[0].find('td', string='Wind Speed (WSPD):').find_next_sibling().get_text().strip()
	nc_wind_speed = page_soups_[1].find('td', string='Wind Speed (WSPD):').find_next_sibling().get_text().strip()
	maine_wind_speed = page_soups_[1].find('td', string='Wind Speed (WSPD):').find_next_sibling().get_text().strip()
	ri_wind_speed = page_soups_[4].find('td', string='Wind Speed (WSPD):').find_next_sibling().get_text().strip()

	#Wind Speed Splicing

	#Boston
	boston_wind_speed_abbreviated = boston_wind_speed.split('.')
	boston_wind_speed_sliced = boston_wind_speed_abbreviated[0]
	boston_wind_speed_abbreviated_int = int(boston_wind_speed_sliced)
	#NC
	nc_wind_speed_abbreviated = nc_wind_speed.split('.')
	nc_wind_speed_sliced = nc_wind_speed_abbreviated[0]
	nc_wind_speed_abbreviated_int = int(nc_wind_speed_sliced)
	#Maine
	maine_wind_speed_abbreviated = maine_wind_speed.split('.')
	maine_wind_speed_sliced = maine_wind_speed_abbreviated[0]
	maine_wind_speed_abbreviated_int = int(maine_wind_speed_sliced)
	#Maine
	ri_wind_speed_abbreviated = ri_wind_speed.split('.')
	ri_wind_speed_sliced = ri_wind_speed_abbreviated[0]
	ri_wind_speed_abbreviated_int = int(ri_wind_speed_sliced)

	wind_speed_abbreviated_list.append(boston_wind_speed_abbreviated_int)
	wind_speed_abbreviated_list.append(nc_wind_speed_abbreviated_int)
	wind_speed_abbreviated_list.append(maine_wind_speed_abbreviated_int)
	wind_speed_abbreviated_list.append(ri_wind_speed_abbreviated_int)

	return wind_speed_abbreviated_list

	# print(boston_wind_speed_abbreviated_int)
	# print(nc_wind_speed_abbreviated_int)


def air_temp_printer():
	page_soups_ = surf_info_finder()

	air_temp_list = []

	boston_air_temp = page_soups_[0].find('td', string='Air Temperature (ATMP):').find_next_sibling().get_text().strip()
	nc_air_temp = page_soups_[1].find('td', string='Air Temperature (ATMP):').find_next_sibling().get_text().strip()
	maine_air_temp = page_soups_[3].find('td', string='Air Temperature (ATMP):').find_next_sibling().get_text().strip()
	ri_air_temp = page_soups_[4].find('td', string='Air Temperature (ATMP):').find_next_sibling().get_text().strip()

	air_temp_list.append(boston_air_temp)
	air_temp_list.append(nc_air_temp)
	air_temp_list.append(maine_air_temp)
	air_temp_list.append(ri_air_temp)

	return air_temp_list

	# print("Current Boston Air Temperature:" + boston_air_temp)
	# print("Current NC Air Temperature:" + nc_air_temp)


def water_temp_printer():
	page_soups_ = surf_info_finder()

	water_temp_list = []

	boston_water_temp = page_soups_[0].find('td', string='Water Temperature (WTMP):').find_next_sibling().get_text().strip()
	nc_water_temp = page_soups_[1].find('td', string='Water Temperature (WTMP):').find_next_sibling().get_text().strip()
	maine_water_temp = page_soups_[3].find('td', string='Water Temperature (WTMP):').find_next_sibling().get_text().strip()
	ri_water_temp = page_soups_[5].find('td', string='Water Temperature (WTMP):').find_next_sibling().get_text().strip()

	water_temp_list.append(boston_water_temp)
	water_temp_list.append(nc_water_temp)
	water_temp_list.append(maine_water_temp)
	water_temp_list.append(ri_water_temp)

	return water_temp_list

	# water_temp = surf_info_finder().find('td', string='Water Temperature (WTMP):').find_next_sibling().get_text().strip()
	# print(water_temp)
	# print("Current Boston Water Temperature:" + boston_water_temp)
	# print("Current NC Water Temperature:" + nc_water_temp)


def forecast_logic():
	wave_height_ = wave_height_printer()
	wave_interval_ = wave_interval_printer()
	wind_direction_ = wind_direction_printer()
	air_temp_ = air_temp_printer()
	water_temp_ = water_temp_printer()
	wind_speed_spliced_ = wind_speed_splicer()

	# if wave_height_ not in wave_height_list:
	if wave_height_ not in wave_height_list and wave_interval_ not in wave_interval_list and wind_direction_ in wind_direction_list and wind_speed_spliced_ < 17:
		print("\n")
		print("-----Conclusion-----")
		print("Good Waves Right Now in Boston! Go out & Surf!")
		print("\n")
	else:
		print("\n")
		print("-----Conclusion-----")
		print("\n")
		print("Unfortunately, surf conditions in Boston are not good right now.")
		print("\n")


#If an error gets thrown due to 'Key Error', it's because tide-forecast.com has changed table's column names
	# -- Last observed on 10/15/2019
def tide_finder():
	# Using Pandas to parse through the html table found in the URL containing Tide Data

	tide_urls = [
	#Boston [0]
	'https://www.tide-forecast.com/locations/Castle-Island-Boston-Harbor-Massachusetts/tides/latest',
	#North Carolina [1]
	'https://www.tide-forecast.com/locations/Morehead-City-North-Carolina/tides/latest',
	#Maine [2]
	'https://www.tide-forecast.com/locations/Portland-Maine/tides/latest',
	#Rhode Island [3]
	'https://www.tide-forecast.com/locations/Newport-Rhode-Island/tides/latest']

	#Initial Master Lists of Tide + Time Info from All URLs
	time_list_initial = []
	tide_list_initial = []

	#Boston Specific Lists
	boston_time_list = []
	boston_tide_list = []

	#NC Specific Lists
	nc_tide_list = []
	nc_time_list = []

	#Maine Specific Lists
	maine_tide_list = []
	maine_time_list = []

	#Maine Specific Lists
	ri_tide_list = []
	ri_time_list = []

  #	LISTS within a LIST
  # 1 & 2: Boston Tide List + Boston Time List
  # 3 & 4: NC Tide List + NC Time List
	boston_master_tides_list = []
	boston_master_tides_list.append(boston_tide_list)
	boston_master_tides_list.append(boston_time_list)

	nc_master_tides_list = []
	nc_master_tides_list.append(nc_tide_list)
	nc_master_tides_list.append(nc_time_list)

	maine_master_tides_list = []
	maine_master_tides_list.append(maine_tide_list)
	maine_master_tides_list.append(maine_time_list)

	ri_master_tides_list = []
	ri_master_tides_list.append(maine_tide_list)
	ri_master_tides_list.append(maine_time_list)

	#MASTER LIST
		#Currently Contains 2 lists (Boston [0] + NC[1])
			# Boston List[0] is comprised of 2 lists: Boston Tide List[0] + Boston Time List [1]
			# NC List[1] is comprised of 2 lists: NC Tide List[0] + NC Time List [1]
	master_all_list = []
	master_all_list.append(boston_master_tides_list)
	master_all_list.append(nc_master_tides_list)
	master_all_list.append(maine_master_tides_list)
	master_all_list.append(ri_master_tides_list)

	# Iterating for our Initial Lists Containing All URL data
	for url in tide_urls:


		tide_table = pd.read_html(url)[0]


		tide_ = tide_table['Tide'].values.tolist()

		# 11/9/2019 -- Changed to Time (EST)& Date
			# Previously Time (EDT)& Date
		# Tide Website changes value of this table's column from time to time
		# Observed at least twice now.
		time_date = tide_table['Time (EST)& Date'].values.tolist()

		time_list_initial.append(time_date)
		tide_list_initial.append(tide_)

	#Boston: Iterating through our initial lists
	for (t, i) in zip(tide_list_initial[0], time_list_initial[0]):
		time_date_sliced = i.split('(')
		time_ = time_date_sliced[0]
		date_ = time_date_sliced[1]

		#change the variable name so it makes it clear what we're printing :)
		tide_ = t

		boston_time_list.append(time_)
		boston_tide_list.append(tide_)

	#NC: Iterating through our initial lists
	for (t, i) in zip(tide_list_initial[1], time_list_initial[1]):
		time_date_sliced = i.split('(')
		time_ = time_date_sliced[0]
		date_ = time_date_sliced[1]

		#change the variable name so it makes it clear what we're printing :)
		tide_ = t

		nc_time_list.append(time_)
		nc_tide_list.append(tide_)

	#Maine: Iterating through our initial lists
	for (t, i) in zip(tide_list_initial[2], time_list_initial[2]):
		time_date_sliced = i.split('(')
		time_ = time_date_sliced[0]
		date_ = time_date_sliced[1]

		#change the variable name so it makes it clear what we're printing :)
		tide_ = t

		maine_time_list.append(time_)
		maine_tide_list.append(tide_)


	#Maine: Iterating through our initial lists
	for (t, i) in zip(tide_list_initial[3], time_list_initial[3]):
		time_date_sliced = i.split('(')
		time_ = time_date_sliced[0]
		date_ = time_date_sliced[1]

		#change the variable name so it makes it clear what we're printing :)
		tide_ = t

		ri_time_list.append(time_)
		ri_tide_list.append(tide_)

	return master_all_list

	#-----------INDEX: master_all_list -----------
		# Boston Tides = master_all_list[0][0] (First List[0], First List within[0])
		# Boston Times = master_all_list[0][1] (First List[0], Second List within[1])

		# NC Tides = master_all_list[1][0] (Second List[1], First List within[0])
		# NC Times = master_all_list[1][1] (Second List[1], Second List within[1])


def forecast_summary_printer_Boston():
	print("-----Wave Info: Boston Harbor-----")
	print("\n")
	print("Current Wave Height:", wave_height_printer())
	print("Current Wave Interval:", wave_interval_printer())
	print("Current Wind Direction:", wind_direction_printer())
	print("Current Air Temperature:", air_temp_printer())
	print("Current Water Temperature:", water_temp_printer())
	print("Current Wind Speed:", wind_speed_splicer())
	print("\n")
	print("-----Tide Info: Boston Harbor-----")
	print("\n")
	tide_finder()



def boston_surf_info_DB():
	conn = sqlite3.connect('SurfSendLive.db')
	cursor = conn.cursor()
	cursor.execute('CREATE TABLE IF NOT EXISTS SurfInfo(ID INTEGER PRIMARY KEY, Location TEXT, WaveHeight TEXT, WaveInterval TEXT, WindDirection TEXT, WindSpeed TEXT, AirTemp TEXT, WaterTemp TEXT)')

	location = "Boston"
	boston_wave_height_ = wave_height_printer()[0]
	boston_wave_interval_ = wave_interval_printer()[0]
	boston_wind_direction_ = wind_direction_printer()[0]
	boston_wind_speed_ = wind_speed_printer()[0]
	boston_air_temp_ = air_temp_printer()[0]
	boston_water_temp_ = water_temp_printer()[0]
	cursor.execute("INSERT INTO SurfInfo(Location, WaveHeight, WaveInterval, WindDirection, WindSpeed, AirTemp, WaterTemp) VALUES (?,?,?,?,?,?,?)", (location,boston_wave_height_,boston_wave_interval_,boston_wind_direction_,boston_wind_speed_,boston_air_temp_,boston_water_temp_))
	conn.commit()
	cursor.close()
	conn.close()
	print("Current Boston Surf Info Successfully Added to DB!")



def nc_surf_info_DB():
	conn = sqlite3.connect('SurfSendLive.db')
	cursor = conn.cursor()
	cursor.execute('CREATE TABLE IF NOT EXISTS SurfInfo(ID INTEGER PRIMARY KEY, Location TEXT, WaveHeight TEXT, WaveInterval TEXT, WindDirection TEXT, WindSpeed TEXT, AirTemp TEXT, WaterTemp TEXT)')

	location = "NC"
	nc_wave_height_ = wave_height_printer()[1]
	nc_wave_interval_ = wave_interval_printer()[1]
	nc_wind_direction_ = wind_direction_printer()[1]
	nc_wind_speed_ = wind_speed_printer()[1]
	nc_air_temp_ = air_temp_printer()[1]
	nc_water_temp_ = water_temp_printer()[1]
	cursor.execute("INSERT INTO SurfInfo(Location, WaveHeight, WaveInterval, WindDirection, WindSpeed, AirTemp, WaterTemp) VALUES (?,?,?,?,?,?,?)", (location,nc_wave_height_,nc_wave_interval_,nc_wind_direction_,nc_wind_speed_,nc_air_temp_,nc_water_temp_))
	conn.commit()
	cursor.close()
	conn.close()
	print("Current NC Surf Info Successfully Added to DB!")



def maine_surf_info_DB():
	conn = sqlite3.connect('SurfSendLive.db')
	cursor = conn.cursor()
	cursor.execute('CREATE TABLE IF NOT EXISTS SurfInfo(ID INTEGER PRIMARY KEY, Location TEXT, WaveHeight TEXT, WaveInterval TEXT, WindDirection TEXT, WindSpeed TEXT, AirTemp TEXT, WaterTemp TEXT)')

	location = "Maine"
	maine_wave_height_ = wave_height_printer()[2]
	maine_wave_interval_ = wave_interval_printer()[2]
	maine_wind_direction_ = wind_direction_printer()[2]
	maine_wind_speed_ = wind_speed_printer()[2]
	maine_air_temp_ = air_temp_printer()[2]
	maine_water_temp_ = water_temp_printer()[2]
	cursor.execute("INSERT INTO SurfInfo(Location, WaveHeight, WaveInterval, WindDirection, WindSpeed, AirTemp, WaterTemp) VALUES (?,?,?,?,?,?,?)", (location,maine_wave_height_,maine_wave_interval_,maine_wind_direction_,maine_wind_speed_,maine_air_temp_,maine_water_temp_))
	conn.commit()
	cursor.close()
	conn.close()
	print("Current Maine Surf Info Successfully Added to DB!")


def ri_surf_info_DB():
	conn = sqlite3.connect('SurfSendLive.db')
	cursor = conn.cursor()
	cursor.execute('CREATE TABLE IF NOT EXISTS SurfInfo(ID INTEGER PRIMARY KEY, Location TEXT, WaveHeight TEXT, WaveInterval TEXT, WindDirection TEXT, WindSpeed TEXT, AirTemp TEXT, WaterTemp TEXT)')

	location = "Rhode Island"
	ri_wave_height_ = wave_height_printer()[2]
	ri_wave_interval_ = wave_interval_printer()[2]
	ri_wind_direction_ = wind_direction_printer()[2]
	ri_wind_speed_ = wind_speed_printer()[2]
	ri_air_temp_ = air_temp_printer()[2]
	ri_water_temp_ = water_temp_printer()[2]
	cursor.execute("INSERT INTO SurfInfo(Location, WaveHeight, WaveInterval, WindDirection, WindSpeed, AirTemp, WaterTemp) VALUES (?,?,?,?,?,?,?)", (location,ri_wave_height_,ri_wave_interval_,ri_wind_direction_,ri_wind_speed_,ri_air_temp_,ri_water_temp_))
	conn.commit()
	cursor.close()
	conn.close()
	print("Current Rhode Island Surf Info Successfully Added to DB!")



def boston_tide_info_DB():
	conn = sqlite3.connect('SurfSendLive.db')
	cursor = conn.cursor()
	cursor.execute('CREATE TABLE IF NOT EXISTS TideInfo(ID INTEGER PRIMARY KEY, Location TEXT, Tide TEXT, Time_ TEXT)')

	location = "Boston"

	query = "INSERT INTO TideInfo(Tide, Time_) VALUES (?,?)"
	for tide, time in zip(tide_finder()[0][0], tide_finder()[0][1]):
		cursor.execute("INSERT INTO TideInfo(Location, Tide, Time_) VALUES (?,?,?)", (location,tide,time))
		conn.commit()
	print("Current Boston Tide Info Successfully Added to DB!")



def nc_tide_info_DB():
	conn = sqlite3.connect('SurfSendLive.db')
	cursor = conn.cursor()
	cursor.execute('CREATE TABLE IF NOT EXISTS TideInfo(ID INTEGER PRIMARY KEY, Location TEXT, Tide TEXT, Time_ TEXT)')

	location = "NC"

	query = "INSERT INTO TideInfo(Tide, Time_) VALUES (?,?)"
	for tide, time in zip(tide_finder()[1][0], tide_finder()[1][1]):
		cursor.execute("INSERT INTO TideInfo(Location, Tide, Time_) VALUES (?,?,?)", (location,tide,time))
		conn.commit()
	print("Current NC Tide Info Successfully Added to DB!")



def maine_tide_info_DB():
	conn = sqlite3.connect('SurfSendLive.db')
	cursor = conn.cursor()
	cursor.execute('CREATE TABLE IF NOT EXISTS TideInfo(ID INTEGER PRIMARY KEY, Location TEXT, Tide TEXT, Time_ TEXT)')

	location = "Maine"

	query = "INSERT INTO TideInfo(Tide, Time_) VALUES (?,?)"
	for tide, time in zip(tide_finder()[2][0], tide_finder()[2][1]):
		cursor.execute("INSERT INTO TideInfo(Location, Tide, Time_) VALUES (?,?,?)", (location,tide,time))
		conn.commit()
	print("Current Maine Tide Info Successfully Added to DB!")


def ri_tide_info_DB():
	conn = sqlite3.connect('SurfSendLive.db')
	cursor = conn.cursor()
	cursor.execute('CREATE TABLE IF NOT EXISTS TideInfo(ID INTEGER PRIMARY KEY, Location TEXT, Tide TEXT, Time_ TEXT)')

	location = "Rhode Island"

	query = "INSERT INTO TideInfo(Tide, Time_) VALUES (?,?)"
	for tide, time in zip(tide_finder()[3][0], tide_finder()[3][1]):
		cursor.execute("INSERT INTO TideInfo(Location, Tide, Time_) VALUES (?,?,?)", (location,tide,time))
		conn.commit()
	print("Current Rhode Island Tide Info Successfully Added to DB!")



surf_info_finder()

# print(wave_height_printer()[0])
# print(wave_interval_printer()[1])
# print(wind_direction_printer()[0])
# print(wind_speed_printer()[0])
# print(air_temp_printer()[1])
# print(water_temp_printer()[0])
# print(wind_speed_splicer()[1])
# print(tide_finder()[0][1][0])
boston_surf_info_DB()
nc_surf_info_DB()
maine_surf_info_DB()
ri_surf_info_DB()

boston_tide_info_DB()
nc_tide_info_DB()
maine_tide_info_DB()
ri_tide_info_DB()


# wave_interval_printer()
# wind_direction_printer() 
# wind_speed_printer() 
# air_temp_printer()
# water_temp_printer() 
# wind_speed_splicer()
# tide_finder()

# loading_screens()
# current_date_time()
# forecast_summary_printer_Boston()
# forecast_logic()
