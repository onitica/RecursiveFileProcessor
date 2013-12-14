import sys
import argparse
from os import listdir, system, rename, remove
from os.path import isfile, isdir, join

#Script functions
def passesFilter(file, fileFilter):
	lfile = file.lower();
	if not fileFilter:
		return True
	else: 
		return reduce(lambda x, y: x or lfile.endswith(y.lower()), fileFilter, False)
		
def processCommand(newpath, command):
	tempfile = "temp232130-0230-120-312301-231" 
	system(command.replace("%fsafe", tempfile).replace("%f", newpath));
	if isfile(tempfile):
		remove(newpath)
		rename(tempfile, newpath)

def applyScript(dir, command, fileFilter):
	for file in listdir(dir):
		if not file.startswith("."): #Ignore dot files/directories, and files that do not pass filter
			newpath = join(dir, file)
			if isfile(newpath) and passesFilter(newpath, fileFilter):
				processCommand(newpath, command)
				print str(newpath) #Print filepaths we are applied to
			elif isdir(newpath):
				applyScript(newpath, command, fileFilter)
	return

#Parsing functions
def dirArg (string):
	if isdir(string):
		return string
	else:
		raise argparse.ArgumentTypeError('Path must be a directory!')
		
def commandArg(string):
	if string.find("%f") != -1:
		return string
	else:
		raise argparse.ArgumentTypeError('Command must have a %f parameter!')

parser = argparse.ArgumentParser()
parser.add_argument("path", type=dirArg, help="The folder path we want to parse")
parser.add_argument("command", type=commandArg, help="The command we want to execute. Must have a %f parameter. %fsafe can be used when we want to do unsafe operations on the same file (ex: unexpand -t 4 %f > %fsafe)")
parser.add_argument("filter", default=[], nargs='*', help="An optional filePath filter")

args = parser.parse_args()
applyScript(args.path, args.command, args.filter)
