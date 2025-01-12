import glob
import os.path
import csv
import json
from dateutil import parser


def compile_data(path):

	# we need the video and the csv
	csv_file = path.replace(".mp4",'.csv')
	if os.path.isfile(csv_file) != True:
		print("No CSV for this one",path)
		return None
	meta = {}
	with open(csv_file) as csv_in:
		reader = csv.DictReader(csv_in)
		for row in reader:
			meta = row
			break


	meta['video_duration'] = int(meta['video_duration'])
	meta['video_diggcount'] = int(meta['video_diggcount'])
	meta['video_sharecount'] = int(meta['video_sharecount'])
	meta['video_commentcount'] = int(meta['video_commentcount'])
	meta['video_playcount'] = int(meta['video_playcount'])
	meta['author_followercount'] = int(meta['author_followercount'])
	meta['author_followingcount'] = int(meta['author_followingcount'])
	meta['author_heartcount'] = int(meta['author_heartcount'])
	meta['author_videocount'] = int(meta['author_videocount'])
	meta['author_diggcount'] = int(meta['author_diggcount'])
	meta['timestamp'] = int(parser.parse(meta['video_timestamp']).timestamp())


	return meta
		




likes = []
favs = []

for file in glob.glob('data/videos/likes/*.mp4'):	
	add = compile_data(file)
	if add != None:
		likes.append(add)

for file in glob.glob('data/videos/favorites/*.mp4'):	
	add = compile_data(file)
	if add != None:
		favs.append(add)

json.dump({'likes':likes,'favorites':favs},open('data/meta.json','w'),indent=2)