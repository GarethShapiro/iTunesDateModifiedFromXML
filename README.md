 This file interrogrates an iTunes XML file and provided it can find files with a similar sub path
 from a specific folder down updates the files modified date to the date added in the XML file.

 This is because DateAdded is a computer property determined by iTunes when a file is added to the 
 database and so cannot be transferred from an iTunes XML file representing an old iTunes library to an old one.

 So this is the next best thing.

 Params:

 1. The source XML file as a relative path from this file.  Eg. ./data/oldiTunes.xml
 2. Optional. The specific folder to look for.  

 For. eg.  
 The old library might have had file locations like :
 /old/music/ambient		

 The new library might have locations like :
 /new/music/ambient

 Either music or ambient could be used as the second parameter depending on the required scope 

 If none is suppled then a folder of Tunes is implied and parameter 3 cannot be supplied.

 3.  Optional.  Test run.
		Supply: True or False

		If none is suppied then False is assumed
