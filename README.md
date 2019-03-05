# Reddit Thing

### Install python

- Get it here https://www.python.org
- Make sure to check **ADD TO PATH** when installing (VERY IMPORTANT)


### Download the software

- https://github.com/impshum/Reddit-Thing/archive/master.zip
- Stick it somewhere easily accessible

### Install requirements

    pip install praw pickledb psaw

### Fill out your details

- Go here https://old.reddit.com/prefs/apps/
- Create a new script app
- Grab the key and token
- Open up config.py and do your thing

### Flairs

Flairs are in a list ```['SUPER ELITE', 'OVER 9000 LEGS!!']```. Just add/remove. Single will look like this ```['SUPER ELITE']```.

### Clearing collected data

Best to just delete the .db file completely as the script creates the file when it's used.

### Test mode

Flip ```test_mode``` on and off with True/False

### Get ready to run

- Open up a terminal/prompt
- cd into the directory you put the Reddit-Thing
- ```python run.py``` will run the script
