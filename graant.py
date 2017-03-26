#!/usr/bin/env python2.7
# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

import ast
import codecs
import collections
from datetime import datetime
import sys

import unicodecsv as csv

import graant_redmine

csv.register_dialect('hledger', delimiter=b',', quoting=csv.QUOTE_ALL)


def read_config(path):
    with codecs.open(path, 'r', 'utf-8') as f:
        return ast.literal_eval(f.read())


def split_account(a):
    return a.split(":")


LogEntry = collections.namedtuple('LogEntry', ['date', 'is_uploaded',
                'account', 'account_path', 'hours', 'comment'])


def log_entry(row_dict):
    return LogEntry(date=datetime.strptime(row_dict['date'], "%Y/%m/%d").date(),
                    is_uploaded=(row_dict['status'] == '*'),
                    account=row_dict['account'],
                    account_path=row_dict['account'].split(':'),
                    hours=row_dict['amount'],
                    comment=row_dict['posting-comment'])


processor_for = {'redmine': graant_redmine.make_processor,
                 'nop': lambda _: (lambda _: None),}


def init_processors(config):
    return {top_account: processor_for[proc_config['type']](proc_config)
            for top_account, proc_config in config.items()}


def process(processors, the_log_entry):
    processors[the_log_entry.account_path[0]](the_log_entry)


def process_journal(config_path, journal_path):
    config      = read_config(config_path)
    exclusions  = {e for c in config.values() for e in c.get('exclude', [])}
    processors  = init_processors(config)

    with open(journal_path) as journal_f:
        reader = csv.DictReader(journal_f, dialect='hledger')
        for row_dict in reader:
            if row_dict['account'] in exclusions:
                continue

            the_log_entry = log_entry(row_dict)
            process(processors, the_log_entry)


if __name__ == '__main__':
    (config_p, journal_p) = sys.argv[1:]
    process_journal(config_p, journal_p)
