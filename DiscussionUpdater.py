# Written by /u/masteroftime666 of reddit
import praw
import re

"""Sets up reddit useragent and login"""
def setup(useragent, username, password):	
	r = praw.Reddit(user_agent=useragent)
	r.login(username, password)
	return r

"""Gets the latest revision of the manga_discussion wiki and writes it into a file"""
def getMangawiki(r):
	MangaWiki = r.get_wiki_page("onepiece","manga_discussion").content_md
	f = open('manga_discussion', 'w')
  	f.write("%s\n" % MangaWiki)

"""Gets the latest revision of the anime_discussion wiki and writes it into a file"""
def getAnimewiki(r):
	AnimeWiki = r.get_wiki_page("onepiece","anime_discussion").content_md
	f = open('anime_discussion', 'w')
  	f.write("%s\n" % AnimeWiki)

"""returns an int of the latest episode/chapter number linked discussion for anime/manga"""
def LastLinkedDiscussion(MorA):
	CoE = []  
	with open(MorA) as f:
    		for line in f:
			CoE = CoE + re.findall(r" [\s0-9]+", line)
	CoE = [ int(x) for x in CoE ]
	return (max(CoE))

"""Checks if a newer  anime discussion has been posted, if true than it calls a function which rewrites the wiki"""
def CheckNewerPostedA(r, Enum):
	phrase = "one piece " + str(Enum) + " flair:CurrentEpisode"
	submissions = r.search(phrase, subreddit="onepiece")
	try:
		Submissionobject = submissions.next()
		Title = Submissionobject.title
		Number = re.findall(r" [\s0-9]+", Title)
		if int(Number[0]) == Enum:
			Link = Submissionobject.short_link
			stringtoadd = "[Episode " + str(Enum) + "](" +  Link[14:] +")"
			AddToWiki(stringtoadd, Enum, "anime_discussion")
			WriteToWiki(r, "anime_discussion")
	except StopIteration:
		return

"""Checks if a newer  manga discussion has been posted, if true than it calls a function which rewrites the wiki"""
def CheckNewerPostedM(r, Cnum):
	phrase = "one piece " + str(Cnum) + " flair:CurrentChapter"
	submissions = r.search(phrase, subreddit="onepiece")
	try:
		Submissionobject = submissions.next()
		Title = Submissionobject.title
		Number = re.findall(r" [\s0-9]+", Title)
		if int(Number[0]) == Cnum:
			Link = Submissionobject.short_link
			stringtoadd = "[Chapter " + str(Cnum) + "](" +  Link[14:] +")"
			AddToWiki(stringtoadd, Cnum, "manga_discussion")
			WriteToWiki(r, "manga_discussion")	
	except StopIteration:
		return

"""This function addeds the new link to wiki file locally"""
def AddToWiki(stringtoadd, Number, wikiname):
	f = open(wikiname, "r")
	contents = f.readlines()
	f.close()
	if ((Number%100) == 0): #this if statment assumes that there is only three lines before it starts linking.
		contents.insert(3, "####"+str(Number)+"s")
		contents.insert(4, "|||||||||||")
		contents.insert(5, "|-|-|-|-|-|-|-|-|-|-|")
		contents.insert(6, str(stringtoadd))
		contents.insert(7, "\r\n")
	if((Number%10) ==0):
		index = (i for i,val in enumerate(contents) if re.findall(str(Number-1), val)).next()
		contents.insert(index+1, str(stringtoadd)+"\r\n")
	else:
		index = (i for i,val in enumerate(contents) if re.findall(str(Number-1), val)).next()
		contents[index] = contents[index][:-2] + "|" + stringtoadd + "\r\n"
	f = open(wikiname, "w")
	contents = "".join(contents)
	f.write(contents)
	f.close()

"""Function write the file to the passed wiki"""
def WriteToWiki(r, wikiname):
	f = open(wikiname, "r")
	contents = f.readlines()
	f.close()
	final =''.join(contents)
	x = r.edit_wiki_page("onepiece",wikiname,final)
	

if __name__ == "__main__":
	r = setup("insert_fancy_user_agent_here", "fancy_user_name_here", "fancy_password_to_fancy_user_name_here")
	getMangawiki(r)
	getAnimewiki(r)
	LatestE = LastLinkedDiscussion('anime_discussion')
	LatestC = LastLinkedDiscussion('manga_discussion')
	CheckNewerPostedA(r, LatestE+1)
	CheckNewerPostedM(r, LatestC+1)
