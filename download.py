import pyktok as pyk
import json
import time
import os.path
import sys
import re
from pathlib import Path
import shutil
import requests


TIME_TO_WAIT = 10 # wait 10 seconds between videos
USE_BROWSER = 'firefox' # can be chrome

if os.path.isfile('user_data_tiktok.json') == False:
	print("Cannot find user_data_tiktok.json user data file! Make sure to put it in this directory.")
	sys.exit()

skip_cache = {}
if os.path.isfile('skip_cache.json') == True:
	skip_cache = json.load(open('skip_cache.json'))


user_data = json.load(open('user_data_tiktok.json'))

if 'Activity' not in user_data:
	print("user_data_tiktok.json not expected format (Activity)")
	sys.exit()

if "Like List" not in user_data['Activity']:
	print("user_data_tiktok.json not expected format (Like List)")
	sys.exit()

if "Favorite Videos" not in user_data['Activity']:
	print("user_data_tiktok.json not expected format (Favorite Videos)")
	sys.exit()

pyk.specify_browser(USE_BROWSER) 

Path("data/videos/likes/").mkdir(parents=True, exist_ok=True)
Path("data/videos/favorites/").mkdir(parents=True, exist_ok=True)

for list_type in [['Like List','ItemFavoriteList'],['Favorite Videos','FavoriteVideoList'] ]:

	count = 0
	print("Downloading ", list_type[0])
	for video in user_data['Activity'][list_type[0]][list_type[1]]:




		if 'Link' in video:
			video['link'] = video['Link']
		if 'Date' in video:
			video['date'] = video['Date']

		tiktok_id= re.search(r"[0-9]{8,}",video['link'])
		if tiktok_id == None:
			print("Could not find numberical id from this link:", video['link'])
			continue
		else:
			tiktok_id = tiktok_id[0]


		count = count + 1
		print(list_type[0], "Working on",count,'/',len(user_data['Activity'][list_type[0]][list_type[1]]),f'https://www.tiktokv.com/share/video/{tiktok_id}')


		if list_type[0] == 'Like List':
			dl_path = "data/videos/likes/"
		else:
			dl_path = "data/videos/favorites/"


		video_path = f"{dl_path}{tiktok_id}.mp4"
		cover_path = f"{dl_path}{tiktok_id}.jpg"	
		meta_csv_path = f"{dl_path}{tiktok_id}.csv"
		meta_json_path = f"{dl_path}{tiktok_id}.json"

		if tiktok_id in skip_cache:
			print("Failed to download this video before:", skip_cache[tiktok_id], 'skipping. Delete skip_cache.json file and run again if you want to try this post again.' )
			continue

		# does the file exist already
		if os.path.isfile(video_path) == True:
			continue
		else:
			try:
				pyk.save_tiktok(f'https://www.tiktokv.com/share/video/{tiktok_id}?is_copy_url=1&is_from_webapp=v1',
				True,
				meta_csv_path,
				USE_BROWSER)
			except requests.exceptions.MissingSchema:

				# this is if it hits a photo post
				print("Can't download", f'https://www.tiktokv.com/share/video/{tiktok_id}','it is a photo post')
				skip_cache[tiktok_id] = "Can't download", f'https://www.tiktokv.com/share/video/{tiktok_id}','it is a photo post'
				json.dump(skip_cache,open('skip_cache.json','w'))
				continue				
			except KeyError:
				print("This video is likely 'Video currently unavailable'")
				skip_cache[tiktok_id] = 'Video currently unavailable'
				json.dump(skip_cache,open('skip_cache.json','w'))
				continue
			except requests.exceptions.ReadTimeout:
				print("Got a timeout, sleeping for 30 seconds")
				time.sleep(30)
				# try again
				try:
					pyk.save_tiktok(f'https://www.tiktokv.com/share/video/{tiktok_id}?is_copy_url=1&is_from_webapp=v1',
					True,
					meta_csv_path,
					USE_BROWSER)
				except:
					time.sleep(30)
					pyk.save_tiktok(f'https://www.tiktokv.com/share/video/{tiktok_id}?is_copy_url=1&is_from_webapp=v1',
					True,
					meta_csv_path,
					USE_BROWSER)					

			except requests.exceptions.ConnectionError:
				print("Got a ConnectionError, sleeping for 30 seconds")
				time.sleep(30)
				# try again
				pyk.save_tiktok(f'https://www.tiktokv.com/share/video/{tiktok_id}?is_copy_url=1&is_from_webapp=v1',
				True,
				meta_csv_path,
				USE_BROWSER)	
			except requests.exceptions.SSLError:
				print("Got a SSLError, sleeping for 30 seconds")
				time.sleep(30)
				# try again
				pyk.save_tiktok(f'https://www.tiktokv.com/share/video/{tiktok_id}?is_copy_url=1&is_from_webapp=v1',
				True,
				meta_csv_path,
				USE_BROWSER)	
			except TypeError:
				print("Got a TypeError, sleeping for 30 seconds")
				time.sleep(30)
				# try again
				pyk.save_tiktok(f'https://www.tiktokv.com/share/video/{tiktok_id}?is_copy_url=1&is_from_webapp=v1',
				True,
				meta_csv_path,
				USE_BROWSER)	



			if os.path.isfile(f"share_video_{tiktok_id}.mp4") == True:
				shutil.move(f"share_video_{tiktok_id}.mp4", video_path)
			else:
				print("Error downloading file", tiktok_id)
				break


		if os.path.isfile(meta_json_path) == True:
			continue
		else:
			try:
				tt_json = pyk.alt_get_tiktok_json(f'https://www.tiktokv.com/share/video/{tiktok_id}?is_copy_url=1&is_from_webapp=v1')
			except requests.exceptions.SSLError:
				time.sleep(30)
				tt_json = pyk.alt_get_tiktok_json(f'https://www.tiktokv.com/share/video/{tiktok_id}?is_copy_url=1&is_from_webapp=v1')

			except requests.exceptions.ReadTimeout:
				time.sleep(30)
				tt_json = pyk.alt_get_tiktok_json(f'https://www.tiktokv.com/share/video/{tiktok_id}?is_copy_url=1&is_from_webapp=v1')
			except requests.exceptions.ConnectionError:
				time.sleep(30)
				tt_json = pyk.alt_get_tiktok_json(f'https://www.tiktokv.com/share/video/{tiktok_id}?is_copy_url=1&is_from_webapp=v1')


			if tt_json == None:
				print("Error downloading JSON, sleeping 30 seconds")
				time.sleep(30)
				tt_json = pyk.alt_get_tiktok_json(f'https://www.tiktokv.com/share/video/{tiktok_id}?is_copy_url=1&is_from_webapp=v1')



			json.dump(tt_json,open(meta_json_path,'w'),indent=2)			
			if '__DEFAULT_SCOPE__' in tt_json:
				if 'webapp.video-detail' in tt_json['__DEFAULT_SCOPE__']:
					cover = tt_json['__DEFAULT_SCOPE__']['webapp.video-detail']['itemInfo']['itemStruct']['video']['cover']
					if cover != '':
						with requests.get(cover, stream=True) as r:
							with open(cover_path, 'wb') as f:
								shutil.copyfileobj(r.raw, f)
					else:
						print("No cover for this one", tiktok_id)

				else:
					print("meta json not in expected format (webapp.video-detail)")
					continue			
			else:
				print("meta json not in expected format (__DEFAULT_SCOPE__)")
				continue




		time.sleep(TIME_TO_WAIT)


