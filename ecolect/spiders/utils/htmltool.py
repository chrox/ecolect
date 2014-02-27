#!/usr/bin/python 
# -*- coding: utf-8 -*-

import re
import HTMLParser

class HtmlTool(object):
    """
    Algorithms to process HTML.
    """
    #Regular expressions to recognize different parts of HTML. 
    #Internal style sheets or JavaScript 
    script_sheet = re.compile(r"<(script|style).*?>.*?(</\1>)", 
        re.IGNORECASE | re.DOTALL)
    #HTML comments - can contain ">"
    comment = re.compile(r"<!--(.*?)-->", re.DOTALL) 
    #HTML tags: <any-text>
    tag = re.compile(r"<.*?>", re.DOTALL)
    #Consecutive whitespace characters
    nwhites = re.compile(r"[\s]+")
    #<p>, <div>, <br> tags and associated closing tags
    p_div = re.compile(r"</?(p|div|br).*?>", 
        re.IGNORECASE | re.DOTALL)
    #Consecutive whitespace, but no newlines
    nspace = re.compile("[^\S\n]+", re.UNICODE)
    #At least two consecutive newlines
    n2ret = re.compile("\n\n+")
    #A return followed by a space
    retspace = re.compile("(\n )")

    #For converting HTML entities to unicode
    html_parser = HTMLParser.HTMLParser()

    @staticmethod
    def text(html):
        """Remove all HTML tags, but produce a nicely formatted text."""
        if html is None:
            return u""
        text = html
        text = HtmlTool.script_sheet.sub("", text)
        text = HtmlTool.comment.sub("", text)
        text = HtmlTool.nwhites.sub(" ", text)
        text = HtmlTool.p_div.sub("\n", text) #convert <p>, <div>, <br> to "\n"
        text = HtmlTool.tag.sub("", text)     #remove all tags
        text = HtmlTool.html_parser.unescape(text)
        #Get whitespace right
        text = HtmlTool.nspace.sub(" ", text)
        text = HtmlTool.retspace.sub("\n", text)
        text = HtmlTool.n2ret.sub("\n\n", text)
        text = text.strip()
        return text
