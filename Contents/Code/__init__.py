# PMS plugin framework
import re
####################################################################################################

VIDEO_PREFIX = "/video/sbsworldnews"
NAME = L('Title')
DEFAULT_CACHE_INTERVAL = 1800
OTHER_CACHE_INTERVAL = 300
ART           = 'art-default.png'
ICON          = 'icon-default.png'

####################################################################################################

def Start():    
    Plugin.AddPrefixHandler(VIDEO_PREFIX, VideoMainMenu, L('VideoTitle'), ICON, ART)
    Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
    ObjectContainer.art = R(ART)
    ObjectContainer.title1 = NAME
    DirectoryObject.thumb = R(ICON)
    #HTTP.SetCacheTime(DEFAULT_CACHE_INTERVAL)

def VideoMainMenu():
    dir = ObjectContainer(viewGroup="InfoList")
    episodes = GetContent()
    for episode in episodes : 
        if len(episode['url']) > 0: 
			Log("Episode found >> " + episode['url'])
			dir.add(VideoClipObject(url=episode['url'], title=episode['name'], thumb=episode['thumbnailURL'], summary=episode['description']))
    return dir

def GetContent():
    x = JSON.ObjectFromURL("http://www.sbs.com.au/api/video_feed/f/dYtmxB/section-programs?form=json&q=world%20news%20australia")
    episodes = []
    for entry in x['entries'] :
        episode = {}
        Log("Found episode" + entry['title'])
        maxBitrate = 0
        for k in entry['media$content']: 
            try: 
                if k['plfile$bitrate'] > maxBitrate:
                    episode['duration'] = k['plfile$duration']
                    episode['url'] = k['plfile$downloadUrl']
                    maxBitrate = k['plfile$bitrate']
            except: 
                Log("No content found")
        try:
            episode['rating'] = entry['media$ratings'][0]['rating']
        except:
            Log("Couldn't get rating")
        episode['name'] = entry['title']
        episode['description'] = entry['description']
        episode['thumbnailURL'] = entry['plmedia$defaultThumbnailUrl']
        episodes.append(episode)
    return episodes
