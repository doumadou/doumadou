#!/usr/bin/env python
# -*- encoding: UTF-8 -*-
# @author: wilbur.ma@foxmail.com
# @date: 2013-08-23
# @license: BSD 3-Clause License
# @brief: parse h1~h6 headings and generate
#         toc of a markdwon file

from bs4 import BeautifulSoup
from pelican import signals, readers, contents
import os, sys, re, md5, markdown, logging

logger = logging.getLogger(__name__)

class Heading:
    def __init__(self, tag, value):
        self.tag = tag
        self.value = value

    def __repr__(self):
        return u"{}:{}".format(self.tag, self.value)

class HeadingParser:
    def __init__(self, slugify_func):
        self.slugify_func = slugify_func
        self.heading_ids = []
        self.headings = []
        self.toc = u""
        self.soup = None

    def gen_heading_id(self, heading_text):
        hID = unicode(self.slugify_func(heading_text, '-'))
        i = 0
        while hID in self.heading_ids:
            # duplicate heading id
            i += 1
            logger.warn(u"found duplicate heading id `{0}'=>`{1}', will try {1}_{2} instead".format(heading_text, hID, i))
            hID = u"{}_{}".format(hID, i)
        self.heading_ids.append(hID)
        return hID

    def feed(self, html_data):
        self.soup = BeautifulSoup(html_data)
        self.headings = self.soup.find_all(re.compile("^h[1-6]$"))

    def generate_headings(self):
        return [Heading(h.name, h.text) for h in self.headings]

    def generate_html(self):
        return self.soup.decode()

    def generate_toc(self, list_style, update=True):
        toc = u""
        prevHead = None
        openListSetNum = 0
        linkFormat = u"<a href='#{}'>{}</a>"
        for i in xrange(len(self.headings)):
            head = self.headings[i]
            head.parent = None
            headAnchor = self.gen_heading_id(head.text)
            if (update):
                # update heading's id attribute
                head["id"] = headAnchor
            if 0 == i:
                # first elem
                toc += (u"<li>" + linkFormat).format(headAnchor, head.text)
                continue
            prevHead = self.headings[i-1]
            if head.name > prevHead.name:
                head.parent = prevHead
                openListSetNum += 1
                toc += (u"<{}><li>" + linkFormat).format(list_style, headAnchor, head.text)
            elif head.name < prevHead.name:
                currParent = prevHead.parent
                while currParent and (head.name <= currParent.name):
                    openListSetNum -= 1
                    toc += (u"</li></{}>".format(list_style))
                    currParent = currParent.parent
                head.parent = currParent
                toc += (u"</li><li>" + linkFormat).format(headAnchor, head.text)
            else:
                head.parent = prevHead.parent
                toc += (u"</li><li>" + linkFormat).format(headAnchor, head.text)
        while openListSetNum > 0:
            toc += (u"</li></{}>".format(list_style))
            openListSetNum -= 1
        if len(self.headings) > 1:
            toc += u"</li>"
        return toc

def extract_headings(content):
    if isinstance(content, contents.Static):
        return

    list_style = content.settings.get("MY_TOC_LIST_TYPE", "ul")
    my_update_headings = content.settings.get("MY_TOC_UPDATE_CONTENT", True)
    my_slugify = content.settings.get("MY_SLUGIFY_FUNC", None)
    if my_slugify is None:
        # custom slugify function not defined
        from markdown.extensions import headerid
        my_slugify = headerid.slugify

    hParser = HeadingParser(my_slugify)
    hParser.feed(content._content)

    content.html_headings = hParser.generate_headings()
    content.html_toc = hParser.generate_toc(list_style, my_update_headings)
    if my_update_headings:
        content._content = hParser.generate_html()

def register():
    signals.content_object_init.connect(extract_headings)

if __name__ == "__main__":
    from markdown.extensions import headerid
    parser = HeadingParser(headerid.slugify)
    htmlStr = "<html><head></head><body><h1>hello</h1>\
            <h2>hi, h2</h2><h2>hi, another h2</h2></body></html>"
    parser.feed(htmlStr)
    print parser.headings
    print parser.generate_toc('ul')

