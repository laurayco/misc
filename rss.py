import xml.etree.ElementTree as ET
from email.utils import parsedate as parsedate_
from time import mktime
import datetime

def parsedate(d):return datetime.datetime.fromtimestamp(mktime(parsedate_(d)))

def element_value(el,default):
	return ((el.text + el.tail) if el is not None else "").strip()

def date_value(dv):
	return parsedate(dv) if isinstance(dv,str) else dv

def repeat_value(val):
	while True: yield val

class Item:
	def __init__(self, title, link, description, pubdate, guid):
		self.title = title
		self.link = link
		self.description = description
		self.published = date_value(pubdate)
		self.guid = guid

class Feed:
	def __init__(self,title,description,link,language,copyright,editor,master,version,items):
		self.title = title
		self.description = description
		self.link = link
		self.language = language
		self.copyright = copyright
		self.editor = editor
		self.webmaster = master
		self.version = version
		self.items = items
	@classmethod
	def create(cls,data):
		tree = ET.fromstring(data)
		return {
			"0.91": cls.parse_91,
			"0.90": cls.parse_90,
			"2.0": cls.parse_20
		}[tree.get("version","2.0")](tree.find("channel"))
	@classmethod
	def parse_91(cls,tree):
		version = tree.get("version","0.91")
		title = element_value(tree.find("title"),"unknown")
		link = element_value(tree.find("link"),"")
		description = element_value(tree.find("description"),"unknown")
		language = element_value(tree.find("language"),"en-us")
		copyright = element_value(tree.find("copyright"),"unknown")
		editor = element_value(tree.find("managingEditor"),"unknown")
		master = element_value(tree.find("webMaster"),"unknown")
		items = map(cls.parse_item,tree.iter("item"),repeat_value(version))
		return cls(title,description,link,language,copyright,editor,master,version,list(items))
	@classmethod
	def parse_90(cls,tree):
		version = tree.get("version","0.90")
		title = element_value(tree.find("title"),"unknown")
		link = element_value(tree.find("link"),"")
		description = element_value(tree.find("description"),"unknown")
		language = element_value(tree.find("language"),"en-us")
		copyright = element_value(tree.find("copyright"),"unknown")
		editor = element_value(tree.find("managingEditor"),"unknown")
		master = element_value(tree.find("webMaster"),"unknown")
		items = map(cls.parse_item,tree.iter("item"),repeat_value(version))
		return cls(title,description,link,language,copyright,editor,master,version,list(items))
	@classmethod
	def parse_20(cls,tree):
		version = tree.get("version","2.0")
		title = element_value(tree.find("title"),"unknown")
		link = element_value(tree.find("link"),"")
		description = element_value(tree.find("description"),"unknown")
		language = element_value(tree.find("language"),"en-us")
		copyright = element_value(tree.find("copyright"),"unknown")
		editor = element_value(tree.find("managingEditor"),"unknown")
		master = element_value(tree.find("webMaster"),"unknown")
		items = map(cls.parse_item,tree.iter("item"),repeat_value(version))
		return cls(title,description,link,language,copyright,editor,master,version,list(items))
	@classmethod
	def parse_item(cls,node,version="2.0"):
		title = element_value(node.find("title"),"unknown")
		link = element_value(node.find("link"),"")
		description = element_value(node.find("description"),"unknown")
		pubdate = element_value(node.find("pubDate"),"unknown")
		guid = element_value(node.find("guid"),"unknown")
		return Item(title,link,description,pubdate,guid)
	def updates(self,since):
		include = lambda x: x.date >= since
		return filter(include,self.items)

sample =  """<?xml version="1.0"?>
<rss version="2.0">
   <channel>
      <title>Liftoff News</title>
      <link>http://liftoff.msfc.nasa.gov/</link>
      <description>Liftoff to Space Exploration.</description>
      <language>en-us</language>
      <pubDate>Tue, 10 Jun 2003 04:00:00 GMT</pubDate>
      <lastBuildDate>Tue, 10 Jun 2003 09:41:01 GMT</lastBuildDate>
      <docs>http://blogs.law.harvard.edu/tech/rss</docs>
      <generator>Weblog Editor 2.0</generator>
      <managingEditor>editor@example.com</managingEditor>
      <webMaster>webmaster@example.com</webMaster>
      <item>
         <title>Star City</title>
         <link>http://liftoff.msfc.nasa.gov/news/2003/news-starcity.asp</link>
         <description>How do Americans get ready to work with Russians aboard the International Space Station? They take a crash course in culture, language and protocol at Russia's &lt;a href="http://howe.iki.rssi.ru/GCTC/gctc_e.htm"&gt;Star City&lt;/a&gt;.</description>
         <pubDate>Tue, 03 Jun 2003 09:39:21 GMT</pubDate>
         <guid>http://liftoff.msfc.nasa.gov/2003/06/03.html#item573</guid>
      </item>
      <item>
         <description>Sky watchers in Europe, Asia, and parts of Alaska and Canada will experience a &lt;a href="http://science.nasa.gov/headlines/y2003/30may_solareclipse.htm"&gt;partial eclipse of the Sun&lt;/a&gt; on Saturday, May 31st.</description>
         <pubDate>Fri, 30 May 2003 11:06:42 GMT</pubDate>
         <guid>http://liftoff.msfc.nasa.gov/2003/05/30.html#item572</guid>
      </item>
      <item>
         <title>The Engine That Does More</title>
         <link>http://liftoff.msfc.nasa.gov/news/2003/news-VASIMR.asp</link>
         <description>Before man travels to Mars, NASA hopes to design new engines that will let us fly through the Solar System more quickly.  The proposed VASIMR engine would do that.</description>
         <pubDate>Tue, 27 May 2003 08:37:32 GMT</pubDate>
         <guid>http://liftoff.msfc.nasa.gov/2003/05/27.html#item571</guid>
      </item>
      <item>
         <title>Astronauts' Dirty Laundry</title>
         <link>http://liftoff.msfc.nasa.gov/news/2003/news-laundry.asp</link>
         <description>Compared to earlier spacecraft, the International Space Station has many luxuries, but laundry facilities are not one of them.  Instead, astronauts have other options.</description>
         <pubDate>Tue, 20 May 2003 08:56:02 GMT</pubDate>
         <guid>http://liftoff.msfc.nasa.gov/2003/05/20.html#item570</guid>
      </item>
   </channel>
</rss>
"""

feed = Feed.create(sample)
print(feed.title)
print(feed.description)
for item in feed.items:
	print(item.title)
	print(item.description)
	print(item.link)
	print(item.published.day,item.published.month,item.published.year)
	print()