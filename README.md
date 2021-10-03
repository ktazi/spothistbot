# Spothistbot

### What is that ?

A bot whose purpose is to gather one's spotify history and transform it into a .csv !

### Requirement

1. Have python and pip installed.

2. All the dependencies are in requirements.txt.
To install : `pip install -r requirements.txt`

3. It is advised to create a virtual environment for this bot.

4. If it isn't done, create a spotify application, then write in configure.json the client id (cid), client secret (secret), a redirect_uri that has been whitelisted i n the configurations of the app and the location and name of the future csv file. <br />
Link to spotify dashboard : https://developer.spotify.com/dashboard/login

### How to use it

This app was made using BlockingScheduler from the apscheduler library : it will run in the foreground of your terminal. To kill it a ctrl-c will suffice. <br />
 <br />
To run it simply write `python bot.py start` from the directory it is placed. IMPORTANT : the configure.json must be in the same directory as bot.py !

### What is gathered ?

The columns of the csv are the following ones :

- nam : name of the artist
- track : name of the track
- dat : date when it was listened
- genre : genre of the song
- imag : image of the album

### What will come next ?

If I have some more time to spend on this little project, I will extend the type of data that can be collected and make it possible for the user to choose what they want (customizable csv yay)
