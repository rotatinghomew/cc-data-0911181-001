from .storage import DataError


def invite(store,journal,payload):
    with journal.transaction():
        row=journal.get('placement',payload['request'])
        offer=store.find('class_offers',offer=row['offer'])
        held=[item for item in journal.all('invitation') if item['offer']==row['offer']
              and item['status'] in ('offered','accepted')]
        if any(item['request']==row['request'] for item in held):
            return next(item for item in held if item['request']==row['request'])
        if row['status']!='qualified' or len(held)>=offer['seats']:
            raise DataError('entry not qualified or no seats')
        invitation=dict(request=row['request'],learner=row['learner'],offer=row['offer'],status='offered')
        return journal.put('invitation',row['request'],invitation)
