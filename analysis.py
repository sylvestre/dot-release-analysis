# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import json
from pprint import pprint
from datetime import date, datetime
import dateutil.parser
from dateutil.relativedelta import relativedelta
import pytz
from libmozdata.bugzilla import Bugzilla
import sys

HOW_MANY_YEARS = 1

def selectDate(releaseDate):
    releaseDate =  dateutil.parser.parse(releaseDate)
    fromWhen = pytz.utc.localize(datetime.now()  - relativedelta(years=HOW_MANY_YEARS))
    return releaseDate > fromWhen

def isFirefoxDotRelease(r):
    return r['product'] == "Firefox" and r['channel'] == "Release" and r['version'].count('.') > 1

def findVersionFromBug(table, search_bug):
    for v, bugs in table.iteritems():    # for name, age in list.items():  (for Python 3.x)
        for b in bugs:
            if str(b) == str(search_bug):
                return v



def getCommitByBugId(dotreleases):
    """Get the revisions from the hg.m.o urls in the bug comments"""
    nightly_pats = Bugzilla.get_landing_patterns(channels=['nightly'])

    def comment_handler(bug, bugid, data):
        r = Bugzilla.get_landing_comments(
            bug['comments'], [], nightly_pats)
        data[bugid]['revs'] = [i['revision'] for i in r]

    def bug_handler(bug, data):
        if 'id' in bug:
            data[str(bug['id'])]['title'] = bug['summary']

    bugids = []
    for r, bug in dotreleases.items():
        bugids += bug

    revisions = {bugid: {'revs': [],
                         'title': ''} for bugid in map(str, bugids)}

    Bugzilla(bugids=bugids,
             include_fields=['id', 'summary'],
             bughandler=bug_handler,
             bugdata=revisions,
             commenthandler=comment_handler,
             commentdata=revisions,
             comment_include_fields=['text']).get_data().wait()
    for bug, data in revisions.items():
        revs = ""
        for r in data['revs']:
            revs += "https://hg.mozilla.org/mozilla-central/rev/" + r + ";"

        print(findVersionFromBug(dotreleases, bug) + ";" + data['title'] + ";https://bugzilla.mozilla.org/" + bug + ";" + revs)

with open('notes.json') as f0:
    notesData = json.load(f0)
i = 0
t = 0
bugs={}
with open('releases.json') as f:
    releaseData = json.load(f)
    for r in releaseData:
        if selectDate(r['release_date']) and isFirefoxDotRelease(r):
            releaseId = r['url']
            for n in notesData:

                if releaseId in list(n['releases']):
                    t = t + 1
                    if n['bug'] is None:
                        if  "Reference link" not in n['note']  and "security fix" not in n['note'].lower():
                            i = i + 1
                            sys.stderr.write(str(n['id']) + " bug not set" + "\n")
                    else:
                        if r['version'] not in bugs:
                            bugs[r['version']] = ()
                        bugs[r['version']] += n['bug'],

getCommitByBugId(bugs)
sys.stderr.write("Bug not set = " + str(i) + "\n")
sys.stderr.write("Total       = " + str(t) + "\n")
