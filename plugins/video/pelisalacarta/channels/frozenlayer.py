# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para frozenlayer
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import scrapertools
import megavideo
import servertools
import binascii
import xbmctools

CHANNELNAME = "frozenlayer"

# Esto permite su ejecuci�n en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

# Traza el inicio del canal
xbmc.output("[frozenlayer.py] init")

DEBUG = True

def mainlist(params,url,category):
	xbmc.output("[frozenlayer.py] mainlist")

	#53=wall
	#xbmc.executebuiltin("Container.SetViewMode(53)")

	if url=='':
		url = "http://www.frozen-layer.com/anime/streaming"

	# ------------------------------------------------------
	# Descarga la p�gina
	# ------------------------------------------------------
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# ------------------------------------------------------
	# Series de la p�gina
	# ------------------------------------------------------
	patron  = '<tr class="nada">[^<]+<td class="lista_titulo">[^<]+<a href="([^"]+)">([^<]+)</a>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	if DEBUG:
		scrapertools.printMatches(matches)

	for match in matches:
		scrapedtitle = match[1]
		scrapedurl = match[0]
		scrapedthumbnail = ""
		
		#http://www.frozen-layer.com/animes/2743-afro-samurai
		#http://flnimg.frozen-layer.com/images/anime/2743/portada.jpg
		patronurl = 'http\:\/\/www.frozen-layer.com\/animes\/([0-9]+)'
		matchesurl = re.compile(patronurl,re.DOTALL).findall(scrapedurl)
		scrapertools.printMatches(matchesurl)
		codigo=''
		if len(matchesurl)>0:
			codigo=matchesurl[0]
			scrapedthumbnail = 'http://flnimg.frozen-layer.com/images/anime/'+codigo+'/portada.jpg'

		# Mete el c�digo del anime en el argumento
		scrapedplot = codigo

		# Depuracion
		if DEBUG:
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)
			xbmc.output("scrapedplot="+scrapedplot)

		# A�ade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# ------------------------------------------------------
	# P�gina siguiente
	# ------------------------------------------------------
	patron = '<a href="([^"]+)" class="next_page" rel="next">Siguiente >></a>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	if DEBUG:
		scrapertools.printMatches(matches)

	for match in matches:
		scrapedtitle = "Pagina siguiente"
		scrapedurl = urlparse.urljoin(url,match)
		scrapedthumbnail = ""
		scrapeddescription = ""

		# Depuracion
		if DEBUG:
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# A�ade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "mainlist" , category , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def listvideos(params,url,category):
	xbmc.output("[frozenlayer.py] listvideos")

	#50=full list
	#xbmc.executebuiltin("Container.SetViewMode(50)")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	# Saca el c�digo del anime del argumento
	codigo = urllib.unquote_plus( params.get("plot") )
	plot = ""

	# ------------------------------------------------------
	# Descarga la p�gina de detalle
	# ------------------------------------------------------
	#http://www.frozen-layer.com/anime/1991/descargas/streaming#t
	url = 'http://www.frozen-layer.com/anime/'+codigo+'/descargas/streaming'
	data = scrapertools.cachePage(url)
	#xbmc.output(data)
	
	# ------------------------------------------------------
	# Extrae el argumento
	# ------------------------------------------------------
	patronvideos  = '<p class="desc " id="sinopsis">(.*?)</p>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	if len(matches)>0:
		plot = matches[0].strip()
	xbmc.output("[frozenlayer.py] plot=%s" % plot)
	
	# ------------------------------------------------------
	# Enlaces a los v�deos
	# ------------------------------------------------------
	patronvideos  = '<tr  class=".*?">[^<]+'
	patronvideos += '<td><a href="([^"]+)".*?'
	patronvideos += '<td class="tit streaming"><a.*?>(.*?)</td>[^<]+'
	patronvideos += '<td class="flags">(.*?)</td>[^<]+'
	patronvideos += '<td>[^<]+</td>[^<]+'
	patronvideos += '<td>.*?</td>[^<]+'
	patronvideos += '<td colspan="2">([^<]+)</td>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)		

	for match in matches:
		scrapedtitle = match[1]
		scrapedtitle = scrapedtitle.replace("</a>","")
		scrapedtitle = scrapedtitle.replace("\t"," ")
		
		scrapedurl = match[0]
		scrapedthumbnail = thumbnail
		scrapedplot = plot

		# Depuracion
		if DEBUG:
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)
			xbmc.output("scrapedplot="+scrapedplot)

		# A�ade al listado de XBMC
		server = ""
		if scrapedurl.startswith("http://www.megavideo.com"):
			server="Megavideo"
		elif scrapedurl.find("youku.com")<>-1:
			server="Youku"
		elif scrapedurl.find("tu.tv")<>-1:
			server="tu.tv"
		elif scrapedurl.find("veoh.com")<>-1:
			server="Veoh - NO SOPORTADO"
		elif scrapedurl.find("livevideo.com")<>-1:
			server="Livevideo - NO SOPORTADO"
		else:
			server="Desconocido"
		scrapedtitle = scrapedtitle + "(" + server + ")"
		
		xbmctools.addnewvideo( CHANNELNAME , "play" , category , server , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
		
	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def play(params,url,category):
	xbmc.output("[frozenlayer.py] play")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = urllib.unquote_plus( params.get("plot") )
	server = urllib.unquote_plus( params.get("server") )

	# En tu.tv, la URL es la del detalle en el servidor
	if server=="tu.tv":
		data = scrapertools.cachePage(url)
		listavideos = servertools.findvideos(data)
		if len(listavideos)>0:
			url = listavideos[0][1]

	xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)
