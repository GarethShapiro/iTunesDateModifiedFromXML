#
# This file interrogrates an iTunes XML file and provided it can find files with a similar sub path
# from a specific folder down updates the files modified date to the date added in the XML file.
#
# This is because DateAdded is a computer property determined by iTunes when a file is added to the 
# database and so cannot be transferred from an iTunes XML file representing an old iTunes library to an old one.
#
# So this is the next best thing.
#
# Params:
#
# 1. The source XML file as a relative path from this file.  Eg. ./data/oldiTunes.xml
# 2. Optional. The specific folder to look for.  
#		For. eg.  
#		The old library might have had file locations like :
# 		/old/music/ambient		
#
#		The new library might have locations like :
#		/new/music/ambient
#
#		Either music or ambient could be used as the second parameter depending on the required scope 
#	
#		If none is suppled then a folder of Tunes is implied and parameter 3 cannot be supplied.
#
# 3.  Optional.  Test run.
#		Supply: True or False
#
#		If none is suppied then False is assumed
import sys, os, time, plistlib, urllib.parse
from datetime import datetime
from Utilities.Terminal import Terminal

def makeMap(root, commonFolderName):
	map = {}

	# trackId is required here otherwise atttributes is a tuple which doesn't have get()
	for trackId, attributes in root['Tracks'].items():

		itemKey = makeKey(attributes, commonFolderName)
		
		if itemKey is None:
			#Terminal.warning(f"itemKey is None, potentially no {commonFolderName} is not in the path {attributes.get('Location')}")
			continue

		if map.get(itemKey) != None:
			Terminal.warning(f"duplicate itemKey:{itemKey}")
			continue

		map[itemKey] = attributes

	return map

def makeKey(attributes, commonFolderName):
	trackFile = getTrackFile(attributes, commonFolderName)
	if trackFile is not None:
		return (attributes.get('Name'), attributes.get('Album'), attributes.get('Total Time'),
			attributes.get('Size'), trackFile)
	return None


# location path from commonFolderName down to the file
#
def getTrackFile(attributes,commonFolderName):

	location = attributes.get('Location')
	newPath = None

	if location is None: return ''

	locationComponents = location.split("/")
	try:
		index = locationComponents.index(commonFolderName)
		newPath = "".join(["/" + component for component in locationComponents[index:]])

	except ValueError:
		Terminal.fail(f"{commonFolderName} is not an element of this path {location}")
		return None

	if newPath != None:
		return newPath

def getRoot(file):
	Terminal.info(f"loading {file}")
	with open(file, "rb") as f:
		return plistlib.load(f)

def updateModifiedDate(track, value):
	Terminal.info(f"updateModifiedDate {track} to {value}")

def updateModifiedDateIfNeeded(targetMap, testRun):
	
	for key in targetMap:
		targetDateAdded = targetMap[key]['Date Added']

		modTime = time.mktime(targetDateAdded.timetuple())
		unquoteLocation = urllib.parse.unquote(targetMap[key]['Location']).lstrip("file:/")
		unquoteLocation = "/" + unquoteLocation #but why
		
		infoPrefix = ""

		if testRun == False:
			os.utime(unquoteLocation, (modTime, modTime))
		else:
			infoPrefix = "*** TestRun ** "

		Terminal.info(f"{infoPrefix}" + f"update {unquoteLocation} modified date to {targetDateAdded}")

def merge(target, testRun, commonFolderName):

	targetMap = makeMap(getRoot(target), commonFolderName)
	Terminal.info(f"source has {len(targetMap)} tracks with metadata")

	updateModifiedDateIfNeeded(targetMap, testRun)

if __name__ == '__main__':

	commonFolderName = "Tunes"
	if len(sys.argv) > 2:
		commonFolderName = sys.argv[2]

	testRun = False
	if len(sys.argv) > 3:
		testRun = sys.argv[3]

	merge(sys.argv[1], testRun, commonFolderName)

