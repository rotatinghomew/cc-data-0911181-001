from .storage import DataError


def accept(store,journal,payload):
    with journal.transaction():
        row=journal.get('invitation',payload['request'])
        other=[item for item in journal.all('invitation') if item['learner']==row['learner']
               and item['request']!=row['request'] and item['status']=='accepted']
        if row['status'] not in ('offered','accepted') or other:
            raise DataError('invitation cannot be accepted')
        row['status']='accepted'
        journal.put('invitation',row['request'],row)
        for pending in journal.all('invitation'):
            if pending['learner']==row['learner'] and pending['request']!=row['request'] and pending['status']=='offered':
                pending['status']='released'
                journal.put('invitation',pending['request'],pending)
        return row
