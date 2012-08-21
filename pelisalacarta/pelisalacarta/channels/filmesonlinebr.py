# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para - Filmes Online BR
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "filmesonlinebr"
__category__ = "F"
__type__ = "generic"
__title__ = "FilmesOnlineBr"
__language__ = "PT"
__creationdate__ = "20120605"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[filmesonlinebr.py] mainlist")
    item.url="http://www.filmesonlinebr.net/";
    return novedades(item)

def novedades(item):
    logger.info("[filmesonlinebr.py] novedades")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    '''
    <div class="item">
    <div class="thumbwrap">
    <div class="thumbnail" style="background: url(http://2.bp.blogspot.com/-pdT9EL18mAk/UDLTMyo-SiI/AAAAAAAAFXE/GXGncCeLY_0/s400/7yu46het.jpg) top left no-repeat;">
    <a href="http://www.filmesonlinebr.net/o-vingador-do-futuro-dublado/" Title="Assistir O Vingador do Futuro &#8211; Dublado Online"><img class="thumbnail" src="http://2.bp.blogspot.com/-pdT9EL18mAk/UDLTMyo-SiI/AAAAAAAAFXE/GXGncCeLY_0/s400/7yu46het.jpg" alt="O Vingador do Futuro &#8211; Dublado" /></a> 
    </div>  
    </div>
    '''
    patron  = '<div class="item"[^<]+'
    patron += '<div class="thumbwrap"[^<]+'
    patron += '<div class="thumbnail" style="background\: url\(([^\)]+)\)[^<]+'
    patron += '<a href="([^"]+)"[^<]+<img class="thumbnail" src="[^"]+" alt="([^"]+)" /></a>'
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for scrapedthumbnail,scrapedurl,title in matches:
        scrapedtitle = title.replace("&#8211; ","(")+")"
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )
    
    '''
    <div id="navi"><a href="http://www.filmesonlinebr.net/page/2/" ><span class="navforward"></span></a></div>
    '''
    patron  = '<a href="([^"]+)" ><span class="navforward"></span>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = ">> Next page"
        scrapedplot = ""
        scrapedurl = urlparse.urljoin(item.url,match)
        scrapedthumbnail = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="novedades", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools
    # mainlist
    novedades_items = mainlist(Item())
    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    bien = False
    for singleitem in novedades_items:
        mirrors = servertools.find_video_items( item=singleitem )
        if len(mirrors)>0:
            bien = True
            break

    return bien