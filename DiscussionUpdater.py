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
	for x in submissions:
		Title = x.title
		Number = re.findall(r" [\s0-9]+", Title)
		isTheory1 = re.findall(r"Theories", Title) #sloppy work
		isTheory2 = re.findall(r"theories", Title)
		isTheory3 = re.findall(r"Theory", Title)
		isTheory4 = re.findall(r"theory", Title)
		if isTheory1 or isTheory2 or isTheory3 or isTheory4
			pass
		if int(Number[0]) == Enum:
			Link = x.short_link
			stringtoadd = "[Episode " + str(Enum) + "](" +  Link[14:] +")"
			AddToWiki(stringtoadd, Enum, "anime_discussion")
			WriteToWiki(r, "anime_discussion")
			return 0
	return 1


"""Checks if a newer  manga discussion has been posted, if true than it calls a function which rewrites the wiki"""
def CheckNewerPostedM(r, Cnum):
	phrase = "one piece " + str(Cnum) + " flair:CurrentChapter"
	submissions = r.search(phrase, subreddit="onepiece")
	for x in submissions:
		Title = x.title
		Number = re.findall(r" [\s0-9]+", Title)
		isTheory1 = re.findall(r"Theories", Title) #sloppy work
		isTheory2 = re.findall(r"theories", Title)
		isTheory3 = re.findall(r"Theory", Title)
		isTheory4 = re.findall(r"theory", Title)
		if isTheory1 or isTheory2 or isTheory3 or isTheory4
			pass
		if int(Number[0]) == Cnum:
			Link = x.short_link
			stringtoadd = "[Chapter " + str(Enum) + "](" +  Link[14:] +")"
			AddToWiki(stringtoadd, Enum, "manga_discussion")
			WriteToWiki(r, "manga_discussion")
			return 0
	return 1

"""This function addeds the new link to wiki file locally"""
def AddToWiki(stringtoadd, Number, wikiname):
	f = open(wikiname, "r")
	contents = f.readlines()
	f.close()
	if ((Number%100) == 0):
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

"""Runs program tell there is no more links to be updated"""
def run():
	A = 0
	M = 0
	r = setup("insert_fancy_user_agent_here", "fancy_user_name_here", "fancy_password_to_fancy_user_name_here")
	getMangawiki(r)
	getAnimewiki(r)
	LatestE = LastLinkedDiscussion('anime_discussion')
	LatestC = LastLinkedDiscussion('manga_discussion')
	while A = 0 :
		LatestE = LastLinkedDiscussion('anime_discussion')
		A = CheckNewerPostedA(r, LatestE+1)
	while M = 0 :
		LatestC = LastLinkedDiscussion('manga_discussion')
		M = CheckNewerPostedM(r, LatestC+1)

if __name__ == "__main__":
	run()
