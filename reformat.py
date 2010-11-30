# RPoL Thread Reformatter
# by Ian Renton
# version 0.1-20080408
# Takes a downloaded RPoL thread, and formats it to make it suitable for
# importing into Drupal etc.

# HTML file.  Pick your RPoL thread, click "D/L" in top right corner, keep
# default options, save the resulting page (File > Save As... etc.) here.
fileToRead = 'input.html'

# Resulting text ready for importing.  Not strictly a full HTML page, hence
# ".txt".
fileToWrite = 'output.txt'

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# CODE BEGINS - No more user-configurable settings below this line
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Read the HTML file
page = file(fileToRead).read()

# Chop out headers and footers
startPosition = page.find('===========================================================')
endPosition = page.rfind('===========================================================')
page = page[startPosition:endPosition]

# Remove redundant things, replace "===="s with <hr>, replace 'red' class with
# a color statement.
page = page.replace('<br>','')
page = page.replace('&nbsp;',' ')
page = page.replace('===========================================================','<hr>\n')
page = page.replace('-----------------------------------------------------------','')
page = page.replace(' (GM)','')
page = page.replace('class="red"','color="red"')

import re

# Regexp match, remove the thread titles and 'by', just leaving the character's
# name.
while True:
    try:
        match = re.compile("<hr>\n\n[^\n]*by ").search(page)
        page = page[0:(match.start() + 6)] + '<b>' + page[match.end():]
    except AttributeError:
        break

# Regexp match, close the <b> tags around the character's name.
while True:
    try:
        match = re.compile("\n<b>[^\n<]*\n").search(page)
        page = page[0:(match.end()-1)] + '</b>' + page[(match.end()-1):]
    except AttributeError:
        break

# Regexp match, remove all "edited by the player at..." lines.
while True:
    try:
        match = re.compile("\n<p class=\"sm[^\n]*\n").search(page)
        page = page[0:match.start()] + page[(match.end()+1):]
    except AttributeError:
        break

# Regexp match, remove all "Private to:" lines.
while True:
    try:
        match = re.compile("<font class=\"private\"[^\n]*</font>").search(page)
        page = page[0:(match.start()-3)] + page[(match.end()+1):]
    except AttributeError:
        break

page = page[6:]

# Write the output file.
writeFile=open(fileToWrite, 'w')
writeFile.write(page)
writeFile.close()
