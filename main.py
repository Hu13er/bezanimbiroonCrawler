# -*- coding: UTF-8 -*-
import re
import httplib
import os

robots_txt = """User-agent: *Disallow: /resources/
		Disallow: /_resources/
		Disallow: /hamdb/
		Disallow: /watermarks/
		Disallow: /_includes/
		"""


def main():
	""" the Program starts Here. . ."""
	if False:
		html = """
<ul style="left: 0px; top: 0px;">
																							
												<li oncontextmenu="return false;" class="gallerypic group1 cboxElement" style="width: 256.667px; height: 170px;" href="/_uploads/Gallery/gallery_3491/20150117200018_7.jpg" title=""><img src="/_uploads/Gallery/gallery_3491/20150117200018_7.jpg" alt="دخمه سنگی کافر کلی" oncontextmenu="return false;"></li>
																							
												<li oncontextmenu="return false;" class="gallerypic group1 cboxElement" style="width: 256.667px; height: 170px;" href="/_uploads/Gallery/gallery_3491/20150117200018_6.jpg" title=""><img src="/_uploads/Gallery/gallery_3491/20150117200018_6.jpg" alt="دخمه سنگی کافر کلی" oncontextmenu="return false;"></li>
																							
												<li oncontextmenu="return false;" class="gallerypic group1 cboxElement" style="width: 256.667px; height: 170px;" href="/_uploads/Gallery/gallery_3491/20150117200018_5.jpg" title=""><img src="/_uploads/Gallery/gallery_3491/20150117200018_5.jpg" alt="دخمه سنگی کافر کلی" oncontextmenu="return false;"></li>
																							
												<li oncontextmenu="return false;" class="gallerypic group1 cboxElement" style="width: 256.667px; height: 170px;" href="/_uploads/Gallery/gallery_3491/20150117200019_4.jpg" title=""><img src="/_uploads/Gallery/gallery_3491/20150117200019_4.jpg" alt="دخمه سنگی کافر کلی" oncontextmenu="return false;"></li>
																							
												<li oncontextmenu="return false;" class="gallerypic group1 cboxElement" style="width: 256.667px; height: 170px;" href="/_uploads/Gallery/gallery_3491/20150117200019_3.jpg" title=""><img src="/_uploads/Gallery/gallery_3491/20150117200019_3.jpg" alt="دخمه سنگی کافر کلی" oncontextmenu="return false;"></li>
																							
												<li oncontextmenu="return false;" class="gallerypic group1 cboxElement" style="width: 256.667px; height: 170px;" href="/_uploads/Gallery/gallery_3491/20150117200019_2.jpg" title=""><img src="/_uploads/Gallery/gallery_3491/20150117200019_2.jpg" alt="دخمه سنگی کافر کلی" oncontextmenu="return false;"></li>
																							
												<li oncontextmenu="return false;" class="gallerypic group1 cboxElement" style="width: 256.667px; height: 170px;" href="/_uploads/Gallery/gallery_3491/20150117200019_1.jpg" title=""><img src="/_uploads/Gallery/gallery_3491/20150117200019_1.jpg" alt="دخمه سنگی کافر کلی" oncontextmenu="return false;"></li>
																						</ul>
		"""
		html = whiteSpaceDel(html)
		regImg = r'<li.*?class="gallerypic group1 cboxElement".*?>.*?<img.*?src="(.*?)".*?>.*?</li>'
		c = 0
		for match in re.finditer(regImg, html):
			src = match.group(1)
			log("[*]Downloading %s..." % src )
		return 0;


	#xmlData = request("http://www.bezanimbiroon.ir", "DataBase")
	log("[*] Starting....")

	xmlData = getData("""http://www.bezanimbiroon.ir/place/%D8%AF%D8%AE%D9%85%D9%87-%D8%B3%D9%86%DA%AF%DB%8C-%DA%A9%D8%A7%D9%81%D8%B1-%DA%A9%D9%84%DB%8C/8874""" , "DataBase")

	
	log("[*]Writing Data.xml file...")
	f = file("Data.xml", 'wb')
	f.write(xmlData)
	f.close();

	
	log("[+]Finish...")
	log("[+] :)-|<")
	log("[*] Closeing logs.txt...")
	log.FILE.close()

	return 0;

def log(text, distance=0):
	""" Print and save Log file """
	print '%s%s' % ('\t'*distance , text)
	log.FILE.write('%s%s\n' % ('\t'*distance , text))
#log File static Variable:
log.FILE = file('logs.txt', 'wb')

def getRelativeAddress(address):
	""" convert raw address to Replative address... """
	match = re.match(r"^(?:(?:http://)?www.bezanimbiroon.ir)?/?(.*)", address)
	match = match.group(1)
	if len(match) > 0 and match[0] != '/':
		match = '/' + match
	if match.find('#') > -1:
		match = match[:match.find('#')]
	return match

from time import sleep
def request(address, name, distance=0):
	""" Using DFS method to Explore the site..."""
	log('[+]Looking %s that named "%s"' % (address, name) , distance)
	if getRelativeAddress(address) in request.list:
		log('_[x]Repetitious... Returning.',distance)
		return ""

	request.list.append(getRelativeAddress(address))
	ret = ""
	ret += "<%s>" % name
	# Other Commands:

	# getting Html by socket request
	log('_[+]Getting Html file: "%s"' % getRelativeAddress(address), distance)

	html = ""

	conn = httplib.HTTPConnection("www.bezanimbiroon.ir")
	conn.request("GET",getRelativeAddress(address))
	response = conn.getresponse()
	log("__Connection Log: %s %s" % (response.status, response.reason) , distance)
	html = response.read()
	log("__%s" % html[:20] , distance)
	html = whiteSpaceDel(html)

	# get Links:
	for match in re.finditer(r'<a(?:.*)href="(.*?)"(?:.*)>(.*)</a>', html):
		href = match.group(1)
		inner = match.group(2) # here, Inner is Name. .. 

		log('_[+]A link found: %s' % href , distance)
		if re.match("^(?:http://)?(.*)(?:/.*)?" , href).group(1) != "www.bezanimbiroon.ir":
			# Then its out of Target
			log('__[!] Out of Target',distance)
			continue

		#sleep(0.5) # sleep for 0.5 Sec
		if re.match("^(?:http://)?www.bezanimbiroon.ir/place/.*" , href):
			# Then its a leaf!
			log('__[+]Leaf Found.',distance)
			ret += getData(href, inner , distance + 1)
		else:
			# otherwise its not a leaf -_-
			ret += request(href, inner, distance + 1)


	# Finish
	ret += "</%s>" % name
	return ret
# Setting static variable for this function
request.list = ['/', '/index.php']

def getData(address, name , distance = 0):
	""" Getting Data from a Leaf... """
	if getRelativeAddress(address) in getData.list:
		return ""

	getData.list.append(getRelativeAddress(address))


	ret = ""
	ret += "<%s>" % name
	# Other Commmands:

	#Getting Html File:
	conn = httplib.HTTPConnection("www.bezanimbiroon.ir")
	conn.request("GET",getRelativeAddress(address))
	response = conn.getresponse()
	log("__Connection Log: %s %s" % (response.status, response.reason) , distance)
	html = response.read()
	html = whiteSpaceDel(html)


	# Titr regular expression:
	regTitr = r'<div class="locIntroTextTitr">(.*?)</div>'
	match = re.search(regTitr, html)
	Title = match.group(1)
	if match:
		ret += "\n<title>%s</title>\n" % Title
	else:
		log("[!]: Can not find Title...." , distance)


	# Intro regular expressoin:
	regIntro = r'<div class="locIntroTextBody">.*?<p>(.*?)</p>.*?</div>'
	match = re.search(regIntro, html)
	if match:
		ret += "\n<Intro>\n%s\n</Intro>\n" % match.group(1)
	else:
		log("[!]: Can not find Intro text...", distance)

	p = file("h.html","wb")
	p.write(html)
	p.close()

	# Gallery regular expression:
	regImg = r'<li.*?class="gallerypic group1".*?>.*?<img.*?src="(.*?)".*?>.*?</li>'

	# setting Folder Name:
	folderName = Title;
	if folderName == "":
		folderName = name
	if folderName =="":
		folderName = "others"

	# make sure exists?
	if not os.path.exists(folderName):
		os.makedirs(folderName)

	# ... and Download imgs:
	for match in re.finditer(regImg, html):
		src = match.group(1)
		log("[*]Downloading %s..." % getRelativeAddress(src) , distance)
		imgDwConn = httplib.HTTPConnection("www.bezanimbiroon.ir")
		imgDwConn.request("GET",getRelativeAddress(src))	
		res = imgDwConn.getresponse()
		if res.status != 200:
			log("[!] Cant Download image file" , distance)
			continue
		fileName = re.match(r'(?:.*)/(.*?)$' , src).group(1)
		imgFile = res.read()
		img = file("%s/%s" % (folderName, fileName) , "wb")
		img.write(imgFile)
		img.close()
		ret += "\n<img>%s/%s</img>\n" % (folderName, fileName)
		log("[+]Downloaded Complite: %s" % src , distance)




	# Properties regular expression:
	reg11 = r'<div id=[\'\"]Ltab1[\'\"]>.*<div.*>(.*)</div>.*<div class="OtherProperties">(.*)</div>.*</div>'
	reg12 = r'<div class="OtherPropertiesRow.">(.*?)<img .*?>.*?</div>\s?<div class="OtherPropertiesRowContent">(.*?)</div>'


	match = re.search(reg11, html)
	if not match:
		log("[!]Error while matching Ltab1...", distance)
		return ret + ("</%s>" % name)
	# getting Explanation of place:
	expl = match.group(1) # getting
	ret += "\n<expl>\n%s\n</expl>\n" % expl

	# getting properties:
	prop = match.group(2)
	#log(prop,distance)
	prop = whiteSpaceDel(prop)

	for match in re.finditer(reg12, prop):
		ret += "\n<%s>\n%s\n</%s>\n" % (match.group(1).strip(), match.group(2).strip(), match.group(1).strip())



	# Feature regular expression:
	reg21 = r''

	# Images regular expression:
	reg31 = r''




	# FInish
	ret += "</%s>" % name
	return ret
# Setting static variable for this function
getData.list = []

def whiteSpaceDel(str):
	"""
	 replace '       ' to ' ' :)
	"""
	ret = ""
	back = False
	for i in str:
		if not i.isspace(): # means this char is not Space
			back = False
			ret = ret + i
		elif ( not back ) and i.isspace(): # means last char was not Space
			ret = ret + ' '
			back = True
	return ret.strip();

print "Returned: %s" % main();
