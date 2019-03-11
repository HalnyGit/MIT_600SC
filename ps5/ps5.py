# 6.00 Problem Set 5
# RSS Feed Filter

import feedparser
import string
import time
from project_util import translate_html
from news_gui import Popup

#-----------------------------------------------------------------------
#
# Problem Set 5

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        summary = translate_html(entry.summary)
        try:
            subject = translate_html(entry.tags[0]['term'])
        except AttributeError:
            subject = ""
        newsStory = NewsStory(guid, title, subject, summary, link)
        ret.append(newsStory)
    return ret

#======================
# Part 1
# Data structure design
#======================

# Problem 1

# TODO: NewsStory
class NewsStory(object):

    def __init__(self, guid, title, subject, summary, link):
        self.guid = guid
        self.title = title
        self.subject = subject
        self.summary = summary
        self.link = link
	
    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_subject(self):
        return self.subject

    def get_summary(self):
        return self.summary

    def get_link(self):
        return self.link
		

#======================
# Part 2
# Triggers
#======================

class Trigger(object):

    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        raise NotImplementedError

# Whole Word Triggers
# Problems 2-5

# TODO: WordTrigger
class WordTrigger(Trigger):

    def __init__(self, word):
        self.word = word

    ### this works but way too ugly!
    # def word_treat(self, word):
        # word = word.lower()
        # word = word.strip(string.punctuation)
        # for mark in string.punctuation:
            # word = word.replace(mark, ' ')
        # return word

    # def string_treat(self, text):
        # words = text.split()
        # temp = [self.word_treat(word) for word in words]
        # treated_string = ' '.join(temp)
        # return treated_string

    # def is_word_in(self, text):
        # return self.word in self.string_treat(text).split()
    ###

    def is_word_in(self, text):
        word = self.word.lower()
        text = text.lower()

        for mark in string.punctuation:
            text = text.replace(mark, ' ')
            splittext = text.split()
        return word in splittext

# TODO: TitleTrigger
class  TitleTrigger(WordTrigger):

    def __init__(self, word):
        WordTrigger.__init__(self, word)

    def evaluate(self, other):
        # return WordTrigger.is_word_in(self, other.get_title())
        return self.is_word_in(other.get_title()) 

# TODO: SubjectTrigger
class  SubjectTrigger(WordTrigger):

    def __init__(self, word):
        WordTrigger.__init__(self, word)

    def evaluate(self, other):
        return self.is_word_in(other.get_subject()) 

# TODO: SummaryTrigger
class  SummaryTrigger(WordTrigger):

    def __init__(self, word):
        WordTrigger.__init__(self, word)

    def evaluate(self, other):
        return self.is_word_in(other.get_summary())

# Composite Triggers
# Problems 6-8

# TODO: NotTrigger
class NotTrigger(Trigger):

    def __init__(self, trigger):
        self.t = trigger

    def evaluate(self, story):
        return not self.t.evaluate(story)

# TODO: AndTrigger
class AndTrigger(Trigger):

    def __init__(self, trigger_1, trigger_2):
        self.t1 = trigger_1
        self.t2 = trigger_2
	
    def evaluate(self, story):
        return self.t1.evaluate(story) and self.t2.evaluate(story)

# TODO: OrTrigger
class OrTrigger(Trigger):

    def __init__(self, trigger_1, trigger_2):
        self.t1 = trigger_1
        self.t2 = trigger_2
	
    def evaluate(self, story):
        return self.t1.evaluate(story) or self.t2.evaluate(story)

# Phrase Trigger
# Question 9

# TODO: PhraseTrigger
class PhraseTrigger(Trigger):

    def __init__(self, phrase):
        self.phrase = phrase

    def evaluate(self, story):
        if self.phrase in story.get_title():
            return True
        elif self.phrase in story.get_subject():
            return True
        elif self.phrase in story.get_summary():
            return True		
        else:
            return False
	

#======================
# Part 3
# Filtering
#======================

def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory-s.
    Returns only those stories for whom
    a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    res = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                res.append(story)
    return res

#======================
# Part 4
# User-Specified Triggers
#======================

def readTriggerConfig(filename):
    """
    Returns a list of trigger objects
    that correspond to the rules set
    in the file filename
    """
    # Here's some code that we give you
    # to read in the file and eliminate
    # blank lines and comments
    triggerfile = open(filename, "r")
    all = [ line.rstrip() for line in triggerfile.readlines() ]
    
    lines = []
    for line in all:
        if len(line) != 0 and line[0] != '#':
            lines.append(line.split())

    # TODO: Problem 11
    # 'lines' has a list of lines you need to parse
    # Build a set of triggers from it and
    # return the appropriate ones

    # lines is a list of elem, where each elem is a list of trigger name and its attributes
    # e.g. [['t1', 'TITLE', 'nfl'], ['t3', 'PHRASE', 'Supreme', 'Court'], ['t4', 'AND', 't2', 't3'], [ADD', 't1', 't4']]
	# creating dictionary of trigger objects
    triggers_map = {}
	
    for elem in lines:
        if elem[1] == 'TITLE':
            triggers_map[elem[0]] = TitleTrigger(elem[2])
        elif elem[1] == 'SUBJECT':
            triggers_map[elem[0]] = SubjectTrigger(elem[2])
        elif elem[1] == 'SUMMARY':
            triggers_map[elem[0]] = SummaryTrigger(elem[2])
        elif elem[1] == 'PHRASE':
            words = [word for word in elem[2:]]
            triggers_map[elem[0]] = PhraseTrigger(" ".join(words))

    for elem in lines:
        if elem[1] == 'NOT':
            triggers_map[elem[0]] = NotTrigger(triggers_map[elem[2]])
        elif elem[1] == 'AND':
            triggers_map[elem[0]] = AndTrigger(triggers_map[elem[2]], triggers_map[elem[3]])
        elif elem[1] == 'OR':
            triggers_map[elem[0]] = OrTrigger(triggers_map[elem[2]], triggers_map[elem[3]])

    for elem in lines:
        if elem[0] == 'ADD':
            triggers =[triggers_map[trigger] for trigger in elem[1:]]
    
    return triggers

	
import thread

def main_thread(p):
    # A sample trigger list - you'll replace
    # this with something more configurable in Problem 11
    t1 = SubjectTrigger("Trump")
    t2 = SummaryTrigger("Trump")
    t3 = PhraseTrigger("Pushes Team")
    t4 = OrTrigger(t2, t3)
    triggerlist = [t1, t4]
    
    # TODO: Problem 11
    # After implementing readTriggerConfig, uncomment this line 
    triggerlist = readTriggerConfig("triggers.txt")

    guidShown = []
    
    while True:
        print "Polling..."

        # Get stories from Google's Top Stories RSS news feed
        stories = process("http://news.google.com/?output=rss")
        # Get stories from Yahoo's Top Stories RSS news feed
        stories.extend(process("http://rss.news.yahoo.com/rss/topstories"))

        # Only select stories we're interested in
        stories = filter_stories(stories, triggerlist)
    
        # Don't print a story if we have already printed it before
        newstories = []
        for story in stories:
            if story.get_guid() not in guidShown:
                newstories.append(story)
        
        for story in newstories:
            guidShown.append(story.get_guid())
            p.newWindow(story)

        print "Sleeping..."
        time.sleep(SLEEPTIME)

SLEEPTIME = 60 #seconds -- how often we poll
if __name__ == '__main__':
    p = Popup()
    thread.start_new_thread(main_thread, (p,))
    p.start()

