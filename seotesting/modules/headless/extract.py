#!/usr/bin/env python
# coding: utf-8
#
# Copyright (c) 2020 JR Oakes
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


EXTRACTIONS = {
    'title':                    "() => [...document.querySelectorAll('title')].map( el => {return {'xpath':xpath(el), 'content': el.textContent};})",
    'description':              "() => [...document.querySelectorAll('meta[name=description]')].map( el => {return {'xpath':xpath(el), 'content': el.content};})",
    'h1':                       "() => [...document.querySelectorAll('h1')].map( el => {return {'xpath':xpath(el), 'content': el.textContent};})",
    'h2':                       "() => [...document.querySelectorAll('h2')].map( el => {return {'xpath':xpath(el), 'content': el.textContent};})",
    'links':                    "() => [...document.querySelectorAll('a')].map( el => {return {'xpath':xpath(el), 'content': {'href': el.href, 'text': el.textContent, 'rel':el.rel}};})",
    'images':                   "() => [...document.querySelectorAll('img')].map( el => {return {'xpath':xpath(el), 'content': {'src': el.src, 'alt': el.alt}};})",
    'canonical':                "() => [...document.querySelectorAll('link[rel=canonical]')].map( el => {return {'xpath':xpath(el), 'content': el.href};})",
    'robots':                   "() => [...document.querySelectorAll('meta[name=robots]')].map( el => {return {'xpath':xpath(el), 'content': el.content};})"
}


DOCUMENT_SCRIPTS = """() => {

 window.xpath = (elt) => {
        var path = "" ,
    		getElementIdx = function(elt) {
    	    	var before = 1 ,
    				after = 0 ;
    	    	for (var sib = elt.previousSibling; sib ; sib = sib.previousSibling) {
    		        if(sib.nodeType == 1 && sib.tagName == elt.tagName)	before++
       			}
    	    	for (var sib = elt.nextSibling; sib ; sib = sib.nextSibling) {
    		        if(sib.nodeType == 1 && sib.tagName == elt.tagName)	after++
       			}
    	    	if( before == 1 && after == 0 )
    				return 0 ;
    			else
    				return before ;
    		} ;

        for (; elt && elt.nodeType == 1; elt = elt.parentNode) {
    	   	idx = getElementIdx(elt);
    		xname = elt.tagName;
    		if (idx > 0) xname += "[" + idx + "]";
    		path = "/" + xname + path;
        }

        return path.toLowerCase() ;
    }


    // Calculate LCP
    window.largestContentfulPaint = 0;

    const observer1 = new PerformanceObserver((entryList) => {
        const entries = entryList.getEntries();
        const lastEntry = entries[entries.length - 1];
        window.largestContentfulPaint = lastEntry.renderTime || lastEntry.loadTime;
    });

    observer1.observe({type: 'largest-contentful-paint', buffered: true});


    // Calculate CLS
    window.cumulativeLayoutShiftScore = 0;

    const observer2 = new PerformanceObserver((entryList) => {
        const entries = entryList.getEntries();
        for (const entry of entries) {
            window.cumulativeLayoutShiftScore += entry.value;
        }
    });

    observer2.observe({type: 'layout-shift', buffered: true});


    // All Observers
    document.addEventListener('visibilitychange', () => {
        if (document.visibilityState === 'hidden') {
          observer1.takeRecords();
          observer1.disconnect();
          observer2.takeRecords();
          observer2.disconnect();
        }
    });

}
"""
