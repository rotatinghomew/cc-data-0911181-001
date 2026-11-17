from .storage import DataError


def grade_attempt(store, attempt):
    form = store.find('forms', form=attempt['form'])
    item_map = {row['item']: row for row in store.table('items')}
    answers = {row['item']: row for row in store.select('responses', attempt=attempt['attempt'])}
    if set(answers) - set(form['items']):
        raise DataError('response outside form')
    awarded = 0
    omitted = 0
    for item in form['items']:
        answer = answers.get(item)
        if answer is None or answer['status'] == 'omitted':
            omitted += 1
            continue
        score = answer.get('score')
        if answer['status'] != 'answered' or not isinstance(score, (int, float)):
            raise DataError('invalid answer')
        if not 0 <= score <= item_map[item]['maximum']:
            raise DataError('invalid score')
        awarded += score
    possible = sum(item_map[item]['maximum'] for item in form['items'])
    return dict(attempt=attempt['attempt'], learner=attempt['learner'], form=form['form'],
                awarded=awarded, possible=possible, omitted=omitted,
                raw_fraction=awarded / possible if possible else None)
