# usage: python ECG_Windowing_WITH_OUTPUT.py annotation_file.txt raw_data_file.txt

import sys
import re
import csv
import os
import itertools
from itertools import islice
from itertools import zip_longest

# maximum bpm ever recorded is ~1000bpm
# therefore, the maximum beats per second is ~16.67
# round this 15, since it is unlikely that a patient will have 1000bpm
# therefore, we define our window size as being equal to:
	# ecg_size * ecg_sampling_frequency
	# = 1 / 15 * 360
	# = 24

# defining data window size and a line counter for the file
window_size = 24
line_counter = 1

# declaring a list to hold the sample number for the p-wave annotations
sample_numbers = []

# read in the annotation file and add the sample numbers to the list
for lines in open(sys.argv[2]):
	lines = re.sub(r"\n", '', lines)
	sample_numbers.append(int(lines))

# open an intermediary file for storing the ECG data
intermediary_file = "intermediate.txt"

# if a file with the same name already exists, delete it
exists = os.path.isfile(intermediary_file)
if exists:
	os.remove(intermediary_file)

# open the intermediary file
intermediate = open(intermediary_file, "a+")

# read each line of the raw ECG data file and append it to the intermediary file
for lines in open(sys.argv[1]):
    lines = re.sub(r"\s*", '', lines)
    lines = str(lines + '\n')
    intermediate.write(lines)

# close the intemediary file
intermediate.close()

# create an output file name
file_name_without_type = re.sub(r"\.txt", '', sys.argv[1])
output_file_name = file_name_without_type + ".csv"

# if a file with the same name already exists, delete it
exists = os.path.isfile(output_file_name)
if exists:
	os.remove(output_file_name)

# open the output file
output_file = open(output_file_name, "w", newline='')
# create a 'writer' that writes to a .csv file (i.e. output file)
writer = csv.writer(output_file)

# declare a list to hold the data to write to the output file
string = []

# open the intermediary file to write to it
with open(intermediary_file, 'r') as input_file:
	# variable used to track how much data has been read
	i = 1
	# read in the lines from the input file
	for lines in input_file:
		# if we haven't read in 24 data points, keep reading
		# and adding to the output string
		if (i != window_size):
			string.append(float(lines))
			i += 1
		# if we have read 24 data points, time to write to
		# the output file
		else:
			# reset the data point counter
			i = 1
			# if we haven't 'used' all of the sample numbers in
			# the annotation file
			if (len(sample_numbers) != 0):
				# find the lowest sample number
				current_p_wave_index = sample_numbers[0]
				# find a lower and upper bound for a specified window
				# where the sample number *might* exist
				lower_bound = (line_counter * 24) - 23
				upper_bound = line_counter * 24
				# if the sample number exists in the current window
				if (current_p_wave_index >= lower_bound) and (current_p_wave_index <= upper_bound):
					# pop the sample number off the list and add a '1' to the output column
					# of the string to write to the output file
					sample_numbers.pop(0)
					string.append(1)
				else:
					# add a '0' to the output column of 
					# the string to write to the output file
					string.append(0)
			else:
				# we've 'used' all the sample number so just 
				# add a '0' to the output column of the string
				# to write to the output file
				string.append(0)
			# write the output string to the output .csv file
			writer.writerow(string)
			# clear the string
			string = []
			# increment the window size/line counter
			line_counter += 1

# remove the intermediary file we used for processing
os.remove(intermediary_file)