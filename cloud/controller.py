from distutils.log import error
import os, time, subprocess
import glob
import searcher
import shutil
import utils
from datetime import datetime

# TODO: api para informar erros/webserver

LOGFILE = "./logs/control.log"

def log(string):
	with open(LOGFILE, 'a+') as lf:
		print(string, flush=True)
		lf.write(string + '\n')

def main():
	log("Starting Downloader...\n")
	downloader_p = subprocess.Popen(["python3", "downloader.py"])

	file_number = 0

	while(file_number <= 1000):
		try:
			txt_list = []
			# wait for txt to finish download and conversion
			while (len(txt_list) == 0):
				txt_list = glob.glob('./input/*.txt')
				if (len(txt_list) == 0):
					time.sleep(2)
			
			# read data from previous run
			data = utils.json_read(utils.DATAFILE)

			file_number_bak = data['file_number']
			last_digits_bak = data['last_digits']
			file_number = file_number_bak + 1
			last_digits = last_digits_bak
			input_file = txt_list[0]

			log(f"{file_number}:\tStarting search in {input_file}\t{datetime.now()}")
			start_time = time.time()
			# warn if txt filename differs from expected, for any reason
			if (input_file != f"pi{file_number}.txt"):
					log(f"{file_number}:\tWARNING: txt filename is wrong. Expected: pi{file_number}.txt - continuing anyway...")

			# parameters >> start(input_file, file_number, start_idx, end_idx, previous):
			last_digits = searcher.run(input_file=input_file, file_number=file_number,
										start_idx=0, end_idx=-1, previous=last_digits) 
			last_digits = str(last_digits)

			# backup palindromes file
			shutil.copyfile("palindromes/palindromes.log", f"palindromes/palindromes{file_number}.log")

			# update json - last digits and new file_number
			data['last_digits'] = last_digits
			data['file_number'] = file_number
			utils.json_write(data, utils.DATAFILE)
			
			# delete txt file
			# os.remove(input_file) #### TODO: reabilitar

			log(f"{file_number}:\tFinished search in {input_file} in {time.time() - start_time}s")
		except:
			log(f'{file_number}:\ERROR: controller loop - resetting json to previous run')
			data['file_number'] = file_number_bak
			data['last_digits'] = last_digits_bak
			utils.json_write(data, utils.DATAFILE)


if __name__ == '__main__':
	log("Starting Controller...\n")
	main()