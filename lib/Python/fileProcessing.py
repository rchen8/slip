import os
import pipes
import errno
import subprocess

HOMENAME = "Slip"

def moveToHome(homename = HOMENAME):
	"""Moves up until reaching the home directory and returns a full path to home"""
	while os.path.split(os.getcwd())[-1] != homename
		os.chdir("..")
	return os.getcwd()

def extractKeyFrames(videoLocation, frameFolder):
	"""Extracts the key frames from the video at videoLocation and puts
	them all into frameFolder
	NOTE: frameFolder should not have any frames in it to start

	returns: timestamps - A list of the second at which every key frame occurs
	"""

	fullVideoLocation = pipes.quote(os.path.join(moveToHome(), videoLocation)) #absolute path

	if (os.path.exists(frameFolder) == False): #try creating the frame folder
		try:
			os.mkdir(frameFolder)
		except OSError as exc:
			if exc.errno != errno.EEXIST:
				raise exc
			pass
	os.chdir(frameFolder)

	filename = videoLocation.split('/')[-1]
	outputFileName = 'output-{0}.txt'.format(filename)
	with open(outputFileName, 'w') as out:
		#now the longass ffmpeg command to split the file
		cmd = "ffmpeg -i {0} -vf select='eq(pict_type\,PICT_TYPE_I)' -vsync " \
		"passthrough -s 320x180 -f image2 %03d.png -loglevel debug 2>&1 | grep " \
		"select:1".format(fullVideoLocation)
		p = subprocess.Popen(cmd, shell = True, stdout = out)
		p.wait()
		out.flush()

	timestamps = []
	outFile = open(outputFileName,'r')
	for line in outFile:
		#some processing to get the time out of the line
		time = line.split(' t:')[1].split(' ')[0]
		time = float(time)

		#decrease time by 1 second so the video starts just before the correct point
		time = max(0, time - 1) #stay positive :D
		timestamps.append(time)

	return timestamps

