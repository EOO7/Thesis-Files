import os
import sys
import re

# defining ECG sampling rate
sampling_rate = 360

# opening the input file and creating the output file name
input_file = open(sys.argv[1], "r")
file_name_without_type = re.sub(r"\.txt", '', sys.argv[1])
output_file_name = "sample_numbers_" + file_name_without_type + ".txt"

# if a file with the same name as the output file exists, delete it
exists = os.path.isfile(output_file_name)
if exists:
	os.remove(output_file_name)

# open the output file
output_file = open(output_file_name, "w")

# variable used to ignore the first line of the input file
i = 0

# for each line in the input .txt file
for lines in input_file:
	# ignore the first line
	if (i != 0):
		# read the column of the line that stores the seconds index
		fields = lines.split()
		time_of_p_wave = fields[0]
		# convert the seconds index to a sample number and write
		# it to the output file
		sample_number = float(time_of_p_wave) * sampling_rate
		output_file.write(str(round(sample_number)) + '\n')
	else:
		i += 1