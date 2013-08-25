# PMS plugin framework
import re
####################################################################################################

VIDEO_PREFIX = "/video/sbs"
NAME = L('Title')
DEFAULT_CACHE_INTERVAL = 1800
OTHER_CACHE_INTERVAL = 300
ART           = 'art-default.png'
ICON          = 'icon-default.png'
BASE_URL = "http://www.sbs.com.au/ondemand/video/"

####################################################################################################

def Start():    
    Plugin.AddPrefixHandler(VIDEO_PREFIX, VideoMainMenu, L('VideoTitle'), ICON, ART)
    Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
    MediaContainer.art = R(ART)
    MediaContainer.title1 = NAME
    DirectoryItem.thumb = R(ICON)
    #HTTP.SetCacheTime(DEFAULT_CACHE_INTERVAL)

def VideoMainMenu():
    dir = MediaContainer(viewGroup="InfoList")
    content = GetContent()
    #Log("Content>>" + content)
    for episode in content : 
        dir.Append(WebVideoItem(episode['url'], title=episode['name'], subtitle='runtime: '+ str(int(episode['duration']/60)) +' mins.', thumb=episode['thumbnailURL'], summary=episode['description']))
    return dir

def GetContent():
    x = JSON.ObjectFromURL("http://www.sbs.com.au/api/video_feed/f/dYtmxB/section-programs?form=json&q=world%20news%20australia")
    for entry in x['entries'] :
        episode = {}
        Log("Found episode" + entry['title'])
        for k in entry['media$content']: 
            try: 
                if k['plfile$bitrate'] == 1500000:
                    episode['duration'] = k['plfile$duration']
                    episode['url'] = k['plfile$downloadUrl']
            except: 
                Log("No 1.5K bitrate found")
        try:
            episode['rating'] = entry['media$ratings'][0]['rating']
        except:
            Log("Couldn't get rating")
        episode['name'] = entry['title']
        episode['description'] = entry['description']
        episode['thumbnailURL'] = entry['plmedia$defaultThumbnailUrl']
    return episode    