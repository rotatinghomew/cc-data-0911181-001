from .domain import grade_attempt
from .storage import DataError


def request(store,journal,payload):
    attempt=store.find('attempts',attempt=payload['attempt'])
    grade=grade_attempt(store,attempt)
    target=store.find('class_offers',offer=payload['offer'])
    if grade['raw_fraction'] is None or grade['raw_fraction']<target['minimum_raw_fraction']:
        raise DataError('raw score does not meet current entry rule')
    row=dict(request=payload['request'],learner=attempt['learner'],attempt=attempt['attempt'],
             offer=target['offer'],basis=grade,status='qualified')
    with journal.transaction():
        existing=[item for item in journal.all('placement') if item['request']==row['request']]
        if existing:
            return existing[0]
        return journal.put('placement',row['request'],row)
