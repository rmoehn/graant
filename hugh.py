# -*- coding: utf-8 -*-

# Usage:
#
#     hugh <Redmine URL> <API key> <name of file with time entries>
#
#
# Format of file with time entries:
#
#     # <comment>
#     <issue #> <yyyy-mm-dd> <hours> <activity ID> <comment …>
#
#
# Example:
#
#     # Activities (redmine.#######.com):
#     # 9  - Implementation
#     # 12 - Project Organization/Mgmt
#     # 13 - Documentation
#     # 19 - Test
#
#     1317 2015-10-21 2.5 3 Watched Back to the Future.
#
#
# Dependencies:
#
#     python-redmine
#     certifi

from __future__ import unicode_literals

import codecs
import re
import sys

from redmine import Redmine
from redmine.packages.requests.exceptions import SSLError

if not isinstance(sys.stdout, codecs.StreamWriter):
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)


def match(regex, s):
    return re.match(regex, s, re.X | re.M | re.S)


def line_to_time_entry(l):
    (iss_id, date, hours, act_id, comment) = re.split(r"\s+", l, maxsplit=4)

    return dict(issue_id=iss_id,
                spent_on=date,
                hours=float(hours), # though API says int
                activity_id=act_id,
                comments=comment)


def string_to_time_entries(s):
    lines = [l for l in s.splitlines()
               if not (match(r"\A \s* \# .* \Z", l)
                       or match(r"\A \s* \Z", l))]

    return [line_to_time_entry(l) for l in lines]


def submit_to_redmine(redmine_url, api_key, fnm):
    with codecs.open(fnm, 'r', 'utf-8') as f:
        contents = f.read()

    redmine = Redmine(redmine_url, key=api_key)

    try:
        for ted in string_to_time_entries(contents):
            redmine.time_entry.create(**ted)
    except SSLError:
        # Because redmine.elegosoft.com is missing an intermediate
        # certificate:
        # https://www.sslshopper.com/ssl-checker.html#hostname=redmine.elegosoft.com
        redmine = Redmine(redmine_url,
                          key=api_key,
                          requests={'verify': False})

        for ted in string_to_time_entries(contents):
            redmine.time_entry.create(**ted)


if __name__ == "__main__":
    (url, api_key, times_fnm) = sys.argv[1:]
    submit_to_redmine(url, api_key, times_fnm)
