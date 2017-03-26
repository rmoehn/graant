#!/usr/bin/env python2.7
# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

import unicodecsv as csv

csv.register_dialect('hledger', delimiter=',', quoting=csv.QUOTE_ALL)

def read_txs_from_csv(path):
    pass


def read_config(path):
    pass


def split_account(s):
    pass


processor_for = {'redmine': RedmineProcessor,
                 'nop': lambda _: (lambda x: x),}


def init_processors(config):
    return {top_account: processor_for[proc_config['type']](proc_config)
            for top_account, proc_config in config.items()}

#    for
#        if proc_config['type'] == 'redmine':
#            processors[top_account] = RedmineProcessor(proc_config)
#        elif proc_config['type'] == 'nop':
#            processors[top_account] = lambda x: x



def process_journal(config_path, journal_path):
    config      = read_config(config_path)
    processors  = init_processors(config)

    with open(journal_path) as journal_f:
        reader = csv.DictReader(journal_f, dialect='hledger')
        for row_dict in reader:
            the_log_dict = log_dict(row_dict)
            process(processors, the_log_dict)
