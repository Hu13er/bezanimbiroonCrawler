# -*- coding: UTF-8 -*-
import re
import httplib

robots_txt = """User-agent: *Disallow: /resources/
		Disallow: /_resources/
		Disallow: /hamdb/
		Disallow: /watermarks/
		Disallow: /_includes/
		"""


def main():
	""" the Program starts Here. . ."""
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
