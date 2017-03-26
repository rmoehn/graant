from redmine import Redmine

def split_account(a):
    return a.split(":")

def make_redmine_processor(config):
    redmine = Redmine(config['redmine_url'], key=config['api_key'])

    def process(log_entry):
        if log_entry.is_uploaded:
            return

        (_, issue_id, activity_name) = split_account(log_entry.account)
        activity_id = config['act_name2act_id'][activity_name]
        redmine.time_entry.create({'issue_id':      issue_id,
                                   'activity_id':   activity_id,
                                   'spent_on':      log_entry.date,
                                   'hours':         float(log_entry.hours),
                                   'comments':      log_entry.comment})

    return process
