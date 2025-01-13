# tiktok-shutdown
Backing up my tic tac likes and favs videos
----

These two scripts will download all of your Liked and Favorited videos and build a local website for you to browse them. It works using your user data requested from tik tok and [pyktok](https://github.com/dfreelon/pyktok)


## How to use:

Before we start you need to make sure you have your TikTok User data file called `user_data_tiktok.json` (called `TikTok_Data_######.zip` zipped). To download this on your app go to:
1. Settings and privacy
2. Account
3. Download your data
4. Switch format to "JSON"
5. Request Download (wait)
6. Click Download. It will open up in a browser and prompt to download. You can copy that URL to get it on your computer or air drop from phone or whatever.

You also need a recent Python3 installed and this repo so clone it using command like (`git clone https://github.com/thisismattmiller/tiktok-shutdown.git`) or save this repo as zip file and extract it.

You then need to put `user_data_tiktok.json` in the same directory as the scripts.

Next install the requirements by doing a pip install: `pip3 install -r requirements.txt`

Now you are all set to run the download script. This will download the likes and favorites videos: `python3 download.py`

You need to have a browser installed, it is configured by default to use Firefox, if you rather use chrome change this line to "chrome": https://github.com/thisismattmiller/tiktok-shutdown/blob/main/download.py#L13

You can try to make it faster by changing the wait time setting: https://github.com/thisismattmiller/tiktok-shutdown/blob/main/download.py#L12

Regardless the servers are flaky and probably will timeout/crash at some point. If that happens just run the download script again and it will pick up where it left off.

Once you have downloaded all your videos run `python3 build.py` to make the data for the website. 

Now you can run the it like a local website to browse your videos: `python3 -m http.server` and open http://localhost:8000/ in your browser. Should look like this:


![Screenshot 2025-01-12 at 6 33 33 PM](https://github.com/user-attachments/assets/adb3b6d8-fca6-4c4b-b228-8cf3c60d0120)






