from redmine import Redmine

def split_account(a):
    return a.split(":")

def make_processor(config):
    redmine = Redmine(config['redmine_url'], key=config['api_key'])

    def process(log_entry):
        if log_entry.is_uploaded:
            return

        activity_id = config['act_name2act_id'][log_entry.account_path[2]]
        redmine.time_entry.create(**{'issue_id':      log_entry.account_path[1],
                                     'activity_id':   activity_id,
                                     'spent_on':      log_entry.date,
                                     'hours':         float(log_entry.hours),
                                     'comments':      log_entry.comment})

    return process
