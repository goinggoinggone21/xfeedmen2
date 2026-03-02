import requests
import datetime
import random
import requests, traceback, json, io, os, urllib.request, sys
#import moviepy
from moviepy.editor import VideoFileClip
import yt_dlp

#sys.stdout.reconfigure(encoding='utf-8')

imojis_list = ['🤍','💟','❤️','😍','🤩','🫣','🥵','🥹','❤️‍🔥','🫶','🫦','🔥','✨','💖','💦','⭐',
    '👑','🤤','💋','😈','🌟','💘','❣️','💕','💓','💗','👀','👌','😵','😵‍💫','🤯','👏',
    '😋','🤪','😳','🫠']

def has_audio(filepath):
    """
    Checks if an MP4 file has an audio track.

    Args:
        filepath (str): The path to the MP4 file.

    Returns:
        bool: True if the file has an audio track, False otherwise.
              Returns None if the file is not found or an error occurs.
    """
    if not os.path.exists(filepath):
        print(f"helper.has_audio Error: File not found at '{filepath}'")
        return None

    try:
        # Load the video clip
        clip = VideoFileClip(filepath)

        # Check if the audio attribute is not None
        if clip.audio is not None:
            clip.close() # Close the clip to release resources
            return True
        else:
            clip.close() # Close the clip
            return False
    except Exception as e:
        print(f"helper.has_audio An error occurred while processing '{filepath}': {e}")
        return None


def get_redgifs_embedded_video_url_old(redgifs_url, output_fn):
    API_URL_REDGIFS = 'https://api.redgifs.com/v2/gifs/'
    r = requests.get('https://api.redgifs.com/v2/auth/temporary')
    token = r.json()['token']

    headers={"Authorization": "Bearer "+token}
    try:
        print("redgifs_url = {}".format(redgifs_url))

        #Get RedGifs video ID
        redgifs_ID = redgifs_url.split('/watch/', 1)
        redgifs_ID = redgifs_ID[1]
        print("redgifs_ID = {}".format(redgifs_ID))
        
        sess = requests.Session()
        
        #Get RedGifs Video Meta
        # request = requests.get(API_URL_REDGIFS + redgifs_ID)
        request = sess.get(API_URL_REDGIFS + redgifs_ID, headers=headers)
        print(request)
        
        if request is None:
            return
        else:
            rawData = request.json()
            #print(rawData)
            #print("rawData = {}".format(rawData))

            #Get HD video url
            hd_video_url = rawData['gif']['urls']['hd']
            #print("hd_video_url = {}".format(hd_video_url))
            
            with sess.get(hd_video_url, stream=True) as r:
                with open(output_fn, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192): 
                        # If you have chunk encoded response uncomment 
                        # if and set chunk_size parameter to None.
                        # if chunk: 
                        f.write(chunk)
            return hd_video_url
    except Exception:
        traceback.print_exc()
        return

def get_redgifs_embedded_video_url(redgifs_url, output_fn):
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json'
    }
    
    API_URL_REDGIFS = 'https://api.redgifs.com/v2/gifs/'
    
    try:
        # 1. Get Token
        r = requests.get('https://api.redgifs.com/v2/auth/temporary', headers=HEADERS)
        r.raise_for_status()
        token = r.json().get('token')
        
        if not token:
            print("Failed to retrieve token.")
            return

        auth_headers = {**HEADERS, "Authorization": f"Bearer {token}"}
        print("auth_headers: ",str(auth_headers))

        # 2. Extract ID (Robust method)
        # Removes query params first, then splits by slashes and grabs the last non-empty part
        clean_url = redgifs_url.split('?')[0]
        redgifs_ID = [p for p in clean_url.split('/') if p][-1].lower()

        print('Trying redgifs_ID: ', str(redgifs_ID))
        print('Full request url: ',f"{API_URL_REDGIFS}{redgifs_ID}")
        
        # 3. Get Metadata
        sess = requests.Session()
        meta_req = sess.get(f"{API_URL_REDGIFS}{redgifs_ID}", headers=auth_headers)
        meta_req.raise_for_status()
        
        video_data = meta_req.json()
        hd_url = video_data.get('gif', {}).get('urls', {}).get('hd')
        print('hd_url: ', str(hd_url))

        if not hd_url:
            print("HD URL not found in response.")
            return

        # 4. Download (Cleaned of hidden characters)
        print(f"Downloading from: {hd_url}")
        # Note: We use the session to maintain cookies/headers
        response = sess.get(hd_url, headers=auth_headers, stream=True)
        response.raise_for_status()

        with open(output_fn, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024 * 1024): # 1MB chunks
                if chunk:
                    f.write(chunk)
        
        print(f"Successfully saved to {output_fn}")
        return hd_url

    except Exception as e:
        print(f"An error occurred: {e}")
        # traceback.print_exc() # Uncomment if you need the full stack trace
        return None

def convert_hastag_to_at(tweet_title_):
    #if '#AngelWicky' in   tweet_title_:
    #   return  tweet_title_.replace('#AngelWicky','@Angel_Wicky_II')
    if '#SukiSin' in tweet_title_:
        return tweet_title_.replace('#SukiSin','@sukisinxx')
    elif '#liz_103' in tweet_title_:
        return tweet_title_.replace('#liz_103','@LilyLouOfficial')
    elif '#JosephineJackson' in tweet_title_:
        return tweet_title_.replace('#JosephineJackson','@josephinejxxx')
    elif '#SophiaLocke' in tweet_title_:
        return tweet_title_.replace('#SophiaLocke','@_SophiaLocke_')
    elif '#ArabelleRaphael' in tweet_title_:
        return tweet_title_.replace('#ArabelleRaphael','@MommyArabelle')
    elif '#VeronicaLeal' in tweet_title_:
        return tweet_title_.replace('#VeronicaLeal','@VeronicaLealoff')
    elif '#ValericaSteele' in tweet_title_:
        return tweet_title_.replace('#ValericaSteele','@VALERiCAx')
    elif '#AnnaDeVille' in tweet_title_:
        return tweet_title_.replace('#AnnaDeVille','@AnnadeVilleXXX')
    elif '#VioletMyers' in tweet_title_:
        return tweet_title_.replace('#VioletMyers','@violetsaucy')
    elif '#KiannaDior' in tweet_title_:
        return tweet_title_.replace('#KiannaDior','@Kianna_Dior')
    elif '#AvaDevine' in tweet_title_:
        return tweet_title_.replace('#AvaDevine','@1avadevine')
    elif '#RemyLaCroix' in tweet_title_:
        return tweet_title_.replace('#RemyLaCroix','@RemyLaCroixxxxx')
    #elif '#StephanieMichelle' in tweet_title_:
    #   return tweet_title_.replace('#StephanieMichelle','@omystephanie')
    elif '#MandyMuse' in tweet_title_:
        return tweet_title_.replace('#MandyMuse','@mandymusemedia')
    elif '#KendraLust' in tweet_title_:
        return tweet_title_.replace('#KendraLust','@KendraLust')
    elif '#SyrenDeMer' in tweet_title_:
        return tweet_title_.replace('#SyrenDeMer','@SyrenDeMerXXX')
    elif '#AshleyAdams' in tweet_title_:
        return tweet_title_.replace('#AshleyAdams','@xoxoashleyadams')
    elif '#KristyBlack' in tweet_title_:
        return tweet_title_.replace('#KristyBlack','@KristyBlack_new')
    elif '#ConniePerignon' in tweet_title_:
        return tweet_title_.replace('#ConniePerignon','@connperignon')
    elif '#MikeAdriano' in tweet_title_:
        return tweet_title_.replace('#MikeAdriano','@MikeAdrianoFeed')
    elif '#evaangelina' in tweet_title_:
        return tweet_title_.replace('#evaangelina','@onlyevaangelina')  
    elif '#NatashaNice' in tweet_title_:
        return tweet_title_.replace('#NatashaNice','@BeNiceNatasha')# \n \n https://onlyfans.com/benicenatasha')
    else:
        return tweet_title_

def convert_name_to_at(tweet_title_):
    if 'Valerica Steele' in tweet_title_:
        tweet_title_submit =  tweet_title_.replace('Valerica Steele','@VALERiCAx')
    if 'Kendra Lust' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('Kendra Lust','@KendraLust')
    if 'Sage Hunter' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('Sage Hunter','@sagexxxhunter')
    if 'Hailey Rose' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('Hailey Rose','@HaileyRoseFucks')
    if 'Alexa Chains' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('Alexa Chains','@ChainsAlexxxa')
    if 'Aria Sloane' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('Aria Sloane','@theariasloane')
    if 'Raven Lane' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('Raven Lane','@ravenlaneXX')
    if 'Rissa May' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('Rissa May','@_RissaMay_XO')
    if 'Scarlett Rosewood' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('Scarlett Rosewood','@ScarlettRose__2')
    if 'River Lynn' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('River Lynn','@riverlynnxxx')
    if 'Addison Vodka' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('Addison Vodka','@addisonv0dka')
    if 'Scarlett Hampton' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('Scarlett Hampton','@scarletthampt0n')
    if 'Dixie Lynn' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('Dixie Lynn','@Xxxdixielynn')
    if 'Mia Kay' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('Mia Kay','@MissMiaKayXXX')
    if 'Nicole Nichols' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('Nicole Nichols','@NicoleNicholss')
    if 'Luna Lovely' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('Luna Lovely','@lunalovelyx')
    if 'Jewelz Blu' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('Jewelz Blu','@jewelz_blu')
    if 'Gia Derza' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('Gia Derza','@giaderza69')
    if 'Sophia Burns' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('Sophia Burns','@sophiaburnsx')
    if 'Rebel Rhyder' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('Rebel Rhyder','@RebelRhyderXXX')
    if 'Jasmine Sherni' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('Jasmine Sherni','@jasminesherni_')
    if 'Hazel Heart' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('Hazel Heart','@HazelHeartxxx')
    if 'Brianna Arson' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('Brianna Arson','@thebriannaarson')
    if 'Emily Jade' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('Emily Jade','@xoemilyjade')
    if 'Willow Ryder' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('Willow Ryder','@willowryder')
    if 'Lily Lou' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('Lily Lou','@LilyLouOfficial')
    if 'Kay Lovely' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('Kay Lovely','@TheKayLovely')
    if 'Sadie Summers' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('Sadie Summers','@originalsadie')
    if 'Romi Rain' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('Romi Rain','@Romi_Rain')
    if 'Tommy King' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('Tommy King','@TommyKingXXX')
    if 'Jennifer White' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('Jennifer White','@jenwhitexxx')
    if 'Harley King' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('Harley King','@HarleyKingxx')
    if 'Violet Myers' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('Violet Myers','@violetsaucy')
    if 'Iris Leon' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('Iris Leon','@irisplayswellxo')
    if 'Mia River' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('Mia River','@MiaRiverXXX')
    if 'Harley Love' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('Harley Love','@harlleylovee')
    if 'Samantha Reigns' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('Samantha Reigns','@SamReignsxo')
    if 'Lola Valentine' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('Lola Valentine','@LolaValentine23')
    if 'Alex Coal' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('Alex Coal','@AlexxxCoal')
    if 'Julia James' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('Julia James','@juliajador')
    if 'Linda Lan' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('Linda Lan','@ms_lindalan')
    if 'Gypsy Rose' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('Gypsy Rose','@gypsyrose5star')
    if 'Cheerleader Kait' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('Cheerleader Kait','@cheerleaderkait')
    if 'Isabel Love' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('Isabel Love','@Isabellovemodel')
    if 'Ashli Orion' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('Ashli Orion','@AshliOrion')
    if 'Myra Moans' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('Myra Moans','@MyraMoans')
    if 'Khloe Kingsley' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('Khloe Kingsley','@KhloeKingsleyxo')
    if 'Ashley Lane' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('Ashley Lane','@AshleyLaneXXX')
    if 'Kylie Le Beau' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('Kylie Le Beau','@kylielebeau')
    if 'Erin Everheart' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('Erin Everheart','@ErinEverheart')
    if 'Chloe Amour' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('Chloe Amour','@REALCHLOEAMOUR')
    if '&Amp' in tweet_title_:
        tweet_title_submit = tweet_title_.replace('&Amp','&')
        

    if 'tweet_title_submit' not in locals():
        tweet_title_submit = tweet_title_
    if tweet_title_submit[0] == '@':
        tweet_title_submit = tweet_title_submit[-1] + ' ' + tweet_title_submit
    return tweet_title_submit

import requests
import time

def get_reddit_redgifs_old(subreddit, limit=1000, time_period="year"):
    """
    Returns a list of dictionaries containing title, video_url, and reddit_link.
    """
    posts_data = []
    after = None
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}
    
    valid_periods = ["hour", "day", "week", "month", "year", "all"]
    if time_period not in valid_periods:
        time_period = "year"

    print(f"Fetching top RedGifs from r/{subreddit} | Period: {time_period}")

    while len(posts_data) < limit:
        url = f"https://www.reddit.com/r/{subreddit}/top.json?t={time_period}&limit=100"
        if after:
            url += f"&after={after}"
            
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"Request failed with status: {response.status_code}")
            break
            
        json_data = response.json().get('data', {})
        children = json_data.get('children', [])
        
        if not children:
            break

        for post in children:
            p = post['data']
            video_url = None
            
            # Check for RedGifs in the main URL or within a Crosspost
            sources = [p.get('url', '')]
            if p.get('crosspost_parent_list'):
                sources.append(p['crosspost_parent_list'][0].get('url', ''))
            
            for link in sources:
                if 'redgifs.com' in link:
                    video_url = link.split('?')[0] # Clean URL
                    break

            if video_url:
                posts_data.append({
                    "title": p.get('title'),
                    "video_url": video_url,
                    "reddit_link": f"https://reddit.com{p.get('permalink')}"
                })

        after = json_data.get('after')
        if not after:
            break
            
        print(f"Found {len(posts_data)} relevant posts...")
        time.sleep(1.2) # Polite delay

    return posts_data[:limit]

# --- Usage Example ---
# results = get_reddit_redgifs("AngelaWhite", limit=100, time_period="all")
# for item in results:
#     print(f"Title: {item['title']}")
#     print(f"URL: {item['video_url']}\n")

from curl_cffi import requests
import time

def get_reddit_redgifs_with_curl_cffi(subreddit, limit=1000, time_period="year"):
    posts_data = []
    after = None
    
    # We still use a realistic User-Agent, but curl_cffi handles the TLS fingerprint
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
    }
    
    valid_periods = ["hour", "day", "week", "month", "year", "all"]
    if time_period not in valid_periods:
        time_period = "year"

    print(f"Bypassing 403... Fetching r/{subreddit} ({time_period})")

    while len(posts_data) < limit:
        url = f"https://www.reddit.com/r/{subreddit}/top.json?t={time_period}&limit=100"
        if after:
            url += f"&after={after}"
            
        # The key change: 'impersonate' makes the TLS handshake look like Chrome
        response = requests.get(url, headers=headers, impersonate="chrome124")
        
        if response.status_code != 200:
            print(f"Still getting blocked? Error {response.status_code}")
            # If 403 persists, print the first 200 chars to see if it's a captcha page
            print(response.text[:200]) 
            break
            
        json_data = response.json().get('data', {})
        children = json_data.get('children', [])
        
        if not children:
            break

        for post in children:
            p = post['data']
            video_url = None
            
            # Look for RedGifs in URL or Crossposts
            sources = [p.get('url', '')]
            if p.get('crosspost_parent_list'):
                sources.append(p['crosspost_parent_list'][0].get('url', ''))
            
            for link in sources:
                if 'redgifs.com' in link:
                    video_url = link.split('?')[0]
                    break

            if video_url:
                posts_data.append({
                    "title": p.get('title'),
                    "video_url": video_url,
                    "reddit_link": f"https://reddit.com{p.get('permalink')}"
                })

        after = json_data.get('after')
        if not after:
            break
            
        print(f"Success! Found {len(posts_data)} so far...")
        time.sleep(2) # Be extra careful with timing

    return posts_data[:limit]

# --- Run Test ---
# results = get_reddit_redgifs_stealth("AngelaWhite", limit=50, time_period="all")

from curl_cffi import requests
import time

def get_reddit_redgifs(subreddit, limit=1000, time_period="year"):#, proxy_url="socks5://127.0.0.1:9050"):
    """
    proxy_url example: "http://username:password@ip:port" 
    or just "http://ip:port" if no auth is needed.
    """
    posts_data = []
    after = None
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.reddit.com/", # VERY IMPORTANT
        "Origin": "https://www.reddit.com",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
    }
    
    # Configure proxy dictionary if provided
    #proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
    proxies = {
    "http": "socks5h://127.0.0.1:9050",
    "https": "socks5h://127.0.0.1:9050"}

    #print(f"Bypassing 403 with Proxy: {proxy_url if proxy_url else 'None'}")

    # Use a Session for cookie persistence
    session = requests.Session()

    while len(posts_data) < limit:
        url = f"https://www.reddit.com/r/{subreddit}/top.json?t={time_period}&limit=100"
        if after:
            url += f"&after={after}"
            
        try:
            response = session.get( #requests.get(
                url, 
                headers=headers, 
                impersonate="chrome124", 
                proxies=proxies,
                timeout=30 # Stop waiting if proxy is dead
            )
            
            if response.status_code == 403:
                print("Error 403: Still forbidden. The proxy might be flagged or your headers are inconsistent.")
                break
            elif response.status_code != 200:
                print(f"Error {response.status_code}")
                break
                
            json_data = response.json().get('data', {})
            children = json_data.get('children', [])
            
            if not children:
                break

            for post in children:
                p = post['data']
                sources = [p.get('url', '')]
                if p.get('crosspost_parent_list'):
                    sources.append(p['crosspost_parent_list'][0].get('url', ''))
                
                for link in sources:
                    if 'redgifs.com' in link:
                        posts_data.append({
                            "title": p.get('title'),
                            "video_url": link.split('?')[0],
                            "reddit_link": f"https://reddit.com{p.get('permalink')}"
                        })

            after = json_data.get('after')
            if not after:
                break
                
            print(f"Collected {len(posts_data)} URLs...")
            time.sleep(random.uniform(5, 10)) #time.sleep(2) 

        except Exception as e:
            print(f"Connection Error: {e}")
            break

    return posts_data[:limit]

# --- How to Run with a Proxy ---
# my_proxy = "http://123.456.78.91:8080" # Replace with a real proxy
# results = get_reddit_redgifs_stealth("AngelaWhite", limit=50, proxy_url=my_proxy)

import socket
import time

def renew_tor_ip():
    """Signals Tor to get a new identity (new IP)."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("127.0.0.1", 9051))
            # We use an empty password because we didn't set HashedControlPassword
            s.send(b'AUTHENTICATE ""\r\nSIGNAL NEWNYM\r\nQUIT\r\n')
            print("Successfully signaled Tor for a new IP.")
        time.sleep(5)  # Give Tor a few seconds to build the new circuit
        return True
    except Exception as e:
        print(f"Failed to renew Tor IP: {e}")
        return False

def load_reddits(subreddit_input, bad_urls_input, all_urls_ever_input):
    reddits_with_redgif_ = get_reddit_redgifs(subreddit_input, time_period='month')
    reddits_with_redgif_ = reddits_with_redgif_ + get_reddit_redgifs(subreddit_input, time_period='year')
    reddits_with_redgif_ = reddits_with_redgif_ + get_reddit_redgifs(subreddit_input, time_period='all')
    print('population before removing duplicates: ', len(reddits_with_redgif_))
    print('num of deuplicates saved: ', len(all_urls_ever_input))
    reddits_with_redgif_deduped = [dict(t) for t in {tuple(sorted(d.items())) for d in reddits_with_redgif_}]
    print('population deduped: ', len(reddits_with_redgif_deduped))
    reddits_with_redgif_without_bads = [x for x in reddits_with_redgif_deduped if str(x['video_url']) not in bad_urls_input]
    print('population without bads: ', len(reddits_with_redgif_without_bads))
    print('num of bads: ', len(bad_urls_input))
    reddits_with_redgif_without_alreadydones = [x for x in reddits_with_redgif_without_bads if str(x['video_url']) not in all_urls_ever_input]
    print('population without already dones: ', len(reddits_with_redgif_without_alreadydones))
    all_urls_ever_output = all_urls_ever_input

    if (len(reddits_with_redgif_without_alreadydones) < 5) & (len(reddits_with_redgif_deduped) > 1):
        reddits_with_redgif_ = get_reddit_redgifs(subreddit_input, time_period='month')
        reddits_with_redgif_ = reddits_with_redgif_ + get_reddit_redgifs(subreddit_input, time_period='year')
        reddits_with_redgif_ = reddits_with_redgif_ + get_reddit_redgifs(subreddit_input, time_period='all')
        reddits_with_redgif_ = [x for x in reddits_with_redgif_ if str(x['video_url']) not in bad_urls_input]
        all_urls_ever_output = []
        print('Ressting all_urls_ever')

    if len(reddits_with_redgif_deduped)==0:
        renew_tor_ip()

    return reddits_with_redgif_, all_urls_ever_output

def create_caption_non_MA(long_name, short_name):
    potential_caps = ['just {} doing {} things'.format(short_name, short_name), '{} being {}'.format(short_name, short_name), 
            'This is your signal to {} for {}'.format(random.choice(['GOON','PUMP','EDGE','LEAK','RUB']),long_name),
            'Pump, Edge, Leak, Repeat! '*random.choice([1,2,3,4,5,6,7,8,9,10]),
            "Stop {} and {} {}".format(random.choice(['scrolling', "what you're doing", 'everything']), random.choice(['stare at', 'pump to', 'rub for', 'edge for', 'leak to', 'get dumb to']), long_name), 
            "{} needs some {}".format(short_name, random.choice(['attention','edges','screen time'])), 
            "What's your favorite {} {}?".format(long_name, random.choice(['scene','move','expression','outfit'])), 
            'All {} all the time!'.format(random.choice([short_name, long_name])), 
            '{}'.format(random.choice(['Pump ', 'Edge ', 'Leak ', 'GOON ']))*random.choice([3,4,5,6,7,8,9,10,11,12,13,14,15]),
            "Go {} one of {}'s posts".format(random.choice(['like','retweet','share','comment on']), short_name), 
            '{} is encouraged'.format(random.choice(['Addiction','Obsession','Gooning','Edging','Falling in love'])),'Wataa','Chudai']
    rchoice = random.choice([1,2,3,4,5,6,7,8])
    print(rchoice)
    if (rchoice==1):
        post_cap = random.choice(potential_caps) + ' ' + random.choice(imojis_list)
        #print('potential_cap: ', random.choice(potential_caps) + ' ' + random.choice(imojis_list))
        #post_cap = random.choice(imojis_list)*3 #get_tweet_title(submission_title) 
    else:
        post_cap = random.choice(imojis_list)*3 #get_tweet_title(submission_title)
        #print('potential_cap: ', random.choice(potential_caps) + ' ' + random.choice(imojis_list)) 

    return post_cap

def get_tiktok_video_urls(username, all_urls_ever_input, bad_urls_input):
    # Strip '@' if the user included it
    username = username.lstrip('@')
    profile_url = f"https://www.tiktok.com/@{username}"
    
    # Options for yt-dlp
    ydl_opts = {
        'extract_flat': True,    # Do not download, just extract the list
        'force_generic_extractor': False,
        'quiet': True,           # Keep the console clean
        'no_warnings': True,
    }

    video_urls = []

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # This returns a dictionary of the profile metadata
            info = ydl.extract_info(profile_url, download=False)
            
            if 'entries' in info:
                for entry in info['entries']:
                    # Build the full URL from the video ID
                    video_id = entry.get('id')
                    if video_id:
                        video_urls.append(f"https://www.tiktok.com/@{username}/video/{video_id}")

            print('population before removing duplicates: ', len(video_urls))
            print('num of deuplicates saved: ', len(all_urls_ever_input))
            tiktoks_deduped = list(set(video_urls))
            print('population deduped: ', len(tiktoks_deduped))
            tiktoks_without_bads = [x for x in tiktoks_deduped if str(x) not in bad_urls_input]
            print('population without bads: ', len(tiktoks_without_bads))
            print('num of bads: ', len(bad_urls_input))
            tiktoks_without_alreadydones = [x for x in tiktoks_without_bads if str(x) not in all_urls_ever_input]
            print('population without already dones: ', len(tiktoks_without_alreadydones))
            all_urls_ever_output = all_urls_ever_input

            if (len(tiktoks_without_alreadydones) < 5) & (len(tiktoks_deduped) > 1):
                tiktoks_without_alreadydones = tiktoks_deduped
                all_urls_ever_output = []
                print('Ressting all_urls_ever')

            if len(tiktoks_deduped)==0:
                renew_tor_ip()

            return tiktoks_without_alreadydones, all_urls_ever_output


        except Exception as e:
            print(f"An error occurred: {e}")
            return []

def download_tiktok_video(video_url_, output_fn="%(title)s.%(ext)s"):
    """
    Downloads a TikTok video as an MP4.
    
    :param video_url: The full URL of the TikTok video.
    :param output_fn: The filename template (defaults to video title).
    """
    ydl_opts = {
        # Format 'bestvideo+bestaudio/best' ensures high quality MP4
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': output_fn,  # How to name the file
        'quiet': False,          # Set to True to hide the progress bar
        'no_warnings': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            print(f"Starting download: {video_url_}")
            ydl.download([video_url_])
            print("Download complete!")
            return True
        except Exception as e:
            print(f"Error downloading video: {e}")
            return False

def create_caption_tt(long_name, short_name):
    potential_caps = ['just {} doing {} things'.format(short_name, short_name), '{} being {}'.format(short_name, short_name), 
            "Stop {} and {} {}".format(random.choice(['scrolling', "what you're doing", 'everything']), random.choice(['stare at', 'appreciate', 'admire']), long_name), 
            "{} needs some {}".format(short_name, random.choice(['attention','edges','screen time'])), 
            "What's your favorite {} {}?".format(long_name, random.choice(['move','expression','outfit'])), 
            'All {} all the time!'.format(random.choice([short_name, long_name])), 
            "Go {} one of {}'s posts".format(random.choice(['like','retweet','share','comment on']), short_name), 
            '{} is encouraged'.format(random.choice(['Addiction','Obsession','Falling in love'])),'Wataa','Chudai',
            "{} or {}".format(random.choice([short_name, long_name]), random.choice(['2 million dollars','gta6','ps6','1 billion dollars']))]
    rchoice = random.choice([1,2,3,4,5,6,7,8])
    print(rchoice)
    if (rchoice==1):
        post_cap = random.choice(potential_caps) + ' ' + random.choice(imojis_list)
        #print('potential_cap: ', random.choice(potential_caps) + ' ' + random.choice(imojis_list))
        #post_cap = random.choice(imojis_list)*3 #get_tweet_title(submission_title) 
    else:
        post_cap = random.choice(imojis_list)*3 #get_tweet_title(submission_title)
        #print('potential_cap: ', random.choice(potential_caps) + ' ' + random.choice(imojis_list)) 

    return post_cap


