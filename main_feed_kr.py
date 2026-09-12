import sys
#import helper
import traceback
from pytwitter import Api
#import math
import praw #for reddit
#import requests
import datetime
import random
import os
import time
import pickle
import helper

#sleep_time = random.choice(range(7000))
#print('sleep time: ', sleep_time, flush=True)
#time.sleep(sleep_time)

def get_tweet_title(reddit_title):
	try:
		#reddit_title_clean = reddit_title.replace('[Discussion]','').replace('[Pick]','')
		#print('reddit_title_clean ', reddit_title_clean)
		#brackets = reddit_title_clean.split('[')[1].split(']')[0]
		#print('brackets ',brackets)
		#final_twitter_title = brackets.title() + ' ' + random.choice(helper.imojis_list)
		#print(final_twitter_title)
		my_list = ["my", "I", "me", "her", "she", "they", "mine","us","we"]

		# Check if any element from my_list is a substring in my_string
		if (not (any(element in reddit_title for element in my_list)) & (len(reddit_title) < 20) & (random.choice([1,2,3])==1)):
			print('reddit_title within get_tweet_title: ', reddit_title)
			return reddit_title
		else:
			return random.choice(helper.imojis_list)*3
		#return final_twitter_title
	except:
		print('Error in title')
		final_twitter_title = random.choice(helper.imojis_list)*3
		#print(final_twitter_title)
		return final_twitter_title
		pass


#print('num of arguments: ', len(sys.argv))
#print(sys.argv)

input_args = sys.argv

#reddit = praw.Reddit(client_id=str(input_args[1]), #REDDIT_CLIENT_ID
#						client_secret=str(input_args[2]),#REDDIT_CLIENT_SECRET
#						password=str(input_args[3]), #REDDIT_PASSWORD
#						user_agent=str(input_args[4]), #REDDIT_USER_AGENT
#						username=str(input_args[5]) #REDDIT_USER_NAME
#						)
twitter_api_authorized = Api(
		access_token=input_args[6], #TWITTER_ACCESS_TOKEN,
		access_secret=input_args[7], #TWITTER_ACCESS_TOKEN_SECRET
		client_id = '1969937231256408064',
		consumer_key = input_args[8], #TWITTER_CONSUMER_KEY
		consumer_secret = input_args[9], #TWITTER_CONSUMER_SECRET
	oauth_flow=True
	)

#Load all list to remove duplicates
all_urls_fn = 'all_kr_feed_urls_ever.ob'
try:
	with open (all_urls_fn, 'rb') as fp:
		all_urls_ever = pickle.load(fp)
		#print(todays_alreadysent_list)
except:
	print("Didn't find historical urls pickle")
	all_urls_ever = []

bad_urls_fn = 'bad_urls_kr.ob'
try:
	with open (bad_urls_fn, 'rb') as fp:
		bad_urls = pickle.load(fp)
		#print(todays_alreadysent_list)
except:
	bad_urls = []


#Load Reddits
reddits_with_redgif, all_urls_ever = helper.load_reddits(subreddit_input='KenzieReeves', 
	all_urls_ever_input=all_urls_ever, bad_urls_input=bad_urls)

filename = 'to_upload_kr.mp4'
if os.path.exists(filename):
				os.remove(filename)

try:
	#Pick Reddit
	for reddit_submission in reddits_with_redgif:
		random_index_selection = random.randint(0,len(reddits_with_redgif)-1)
		submission_url = reddits_with_redgif[random_index_selection]['video_url']
		submission_title = reddits_with_redgif[random_index_selection]['title']
		if (str(submission_url) not in all_urls_ever):
			break
		else:
			continue
	tweet_title_final = helper.create_caption_non_MA(long_name='Kenzie Reeves',short_name='Kenzie') #random.choice(helper.imojis_list)*3 
	print('submission_url: ', submission_url)
	print('submission_title: ', submission_title)
	print('tweet_title_final: ', tweet_title_final)

	#Check File
	#while (not os.path.isfile(filename)) & (str(submission_url) not in all_urls_ever):
	video_url = helper.get_redgifs_embedded_video_url(redgifs_url=submission_url, output_fn=filename)
	file_has_audio = helper.has_audio(filename)   
	if not file_has_audio:
		print('no audio in file')
		if os.path.exists(filename):
			os.remove(filename)
	if not os.path.exists(filename): #if url is bad or has no audio, add it to bad list
		print('file is bad; adding to bad list')
		bad_urls.append(submission_url)
		with open(bad_urls_fn, 'wb') as fp:
			#pickle.dump([], fp)
			pickle.dump(bad_urls, fp)

	#Make Post
	total_bytes = os.path.getsize(filename)
	print('total_bytes: ', total_bytes)
	if int(total_bytes) < 1000000:
					print('File Size Too Small')
					with open('all_urls_ever.ob', 'wb') as fp:
									#pickle.dump([], fp)
									pickle.dump(all_urls_ever, fp)
					#continue
	resp = twitter_api_authorized.upload_media_chunked_init(
					total_bytes=total_bytes,
					media_type="video/mp4",
	)
	media_id = resp.media_id_string
	#print(media_id)

	segment_id = 0
	bytes_sent = 0
	file = open(filename, 'rb')
	idx=0
	while bytes_sent < total_bytes:
					chunk = file.read(4*1024*1024)
					status = twitter_api_authorized.upload_media_chunked_append(
													media_id=media_id,
													media=chunk,
													segment_index=idx
									)
					idx = idx+1

					bytes_sent = file.tell()
					#print(idx, media_id, status, bytes_sent)

	resp = twitter_api_authorized.upload_media_chunked_finalize(media_id=media_id)
	print(resp)


	time.sleep(30)
	resp = twitter_api_authorized.upload_media_chunked_status(media_id=media_id)
	print(resp)

	twitter_api_authorized.create_tweet(
					media_media_ids=[media_id], 
					text=tweet_title_final
	)

	os.remove(filename)

	all_urls_ever.append(submission_url)
	with open(all_urls_fn, 'wb') as fp:
					#pickle.dump([], fp)
					pickle.dump(all_urls_ever, fp)
	if os.path.exists(filename):
					os.remove(filename)
	#print('pausing')
	#time.sleep(600) #random.choice(range(7000))
except Exception:
	print('error in flow')
	print(traceback.format_exc())
	pass
	#continue


		
		
