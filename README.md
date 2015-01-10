Codl
---
Codl is a script I wrote that utilizes the [4Chan API](https://github.com/4chan/4chan-API) to download entire story times from the /co/ board on 4Chan.

How to use
---
* Run ```codl.py``` with the URL of the story time and any desired flags as command line arguments.
* By default the script will only download images that have similar file names as the first image. To stop this the ```-a``` flag will download all of the images in the thread.
* By default the script will save all the images to a directory it creates. The name of the directory is established by finding the name of the story timed comic in the subject. If one can not be found a part of the first post will be used. To use a custom name use the ```-n``` flag followed by the name you want to use.
* The ```-z``` flag will zip the directory and all files in it then delete the created directory.
