# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para sockshare
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config


def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[sockshare.py] url="+page_url)
    data = scrapertools.cache_page(page_url)

    patron  = '<form method="post">[^<]+'
    patron += '<input type="hidden" value="([0-9a-f]+?)" name="([^"]+)">[^<]+'
    patron += '<input name="confirm" type="submit" value="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    if len(matches)==0: return []

    post = matches[0][1]+"="+matches[0][0]+"&confirm="+(matches[0][2].replace(" ","+"))
    headers = []
    headers.append( ['User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:10.0.2) Gecko/20100101 Firefox/10.0.2'] )
    headers.append( [ "Accept" , "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" ])
    headers.append( ['Referer',page_url] )

    data = scrapertools.cache_page( page_url , post=post, headers=headers )
    logger.info("data="+data)

    # Extrae el trozo cifrado
    patron = "playlist: '(.+?)'"
    matches = re.compile(patron,re.DOTALL).findall(data)
    #scrapertools.printMatches(matches)
    data = ""
    if len(matches)>0:
        xmlurl = urlparse.urljoin(page_url,matches[0])
        logger.info("[sockshare.py] Playlis="+xmlurl)
    else:
        logger.info("[sockshare.py] No encuentra Playlist=")

        return []
    

    logger.info("xmlurl="+xmlurl)
    data = scrapertools.downloadpageWithoutCookies(xmlurl)
    # Extrae la URL
    patron = '</link><media\:content url="(.+?)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    video_urls = []
    
    if len(matches)>0:
        video_urls.append( ["."+matches[0].rsplit('.',1)[1][0:3]+" [sockshare]",matches[0]])

    for video_url in video_urls:
        logger.info("[sockshare.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra v�deos de este servidor en el texto pasado
def find_videos(text):
    encontrados = set()
    devuelve = []

    # http://www.sockshare.com/embed/CEE0B3A7DDFED758
    patronvideos  = 'http://www.sockshare.com/(?:file|embed)/([A-Z0-9]+)'
    logger.info("[sockshare.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[sockshare]"
        url = "http://www.sockshare.com/embed/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'sockshare' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
