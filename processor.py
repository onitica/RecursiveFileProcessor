import sys
from os import listdir, system, rename, remove
from os.path import isfile, join

def passesFilter(file, fileFilter):
	if fileFilter is None:
		return True
	else: 
		return file.endswith(fileFilter)
		
def processCommand(newpath, command):
	tempfile = "temp232130-0230-120-312301-231" 
	system(command.replace("%fsafe", tempfile).replace("%f", newpath));
	if isfile(tempfile):
		remove(newpath)
		rename(tempfile, newpath)

def applyScript(dir, command, fileFilter):
	for file in listdir(dir):
		if not file.startswith(".") and passesFilter(file, fileFilter): #Ignore dot files/directories, and files that do not pass filter
			newpath = join(dir, file)
			if isfile(newpath):
				processCommand(newpath, command)
				print str('Applied to file: ' + newpath)
			else:
				applyScript(join(dir, file), command, fileFilter)
	return

argCount = len(sys.argv)
fileFilter = None

if argCount != 3:
	if(argCount == 4):
		fileFilter = sys.argv[3];
	else:	
		print "Error: Incorrect paramaters! Format: python processor.py <path> <commandToApply> <filter>. Filter is optional."	 
		sys.exit()
			
folderPath = sys.argv[1]
command = sys.argv[2]	

if command.find("%f") == -1:
	print "Error: Must have the file path somewhere in the command. The filepath is denoted by %f in the command."
	sys.exit()

applyScript(folderPath, command, fileFilter)
