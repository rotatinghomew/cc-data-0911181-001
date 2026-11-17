from .domain import grade_attempt
from .storage import mean, single


def scores(store, query):
    selected = single(query, 'learner')
    rows = [grade_attempt(store, attempt) for attempt in store.table('attempts')
            if selected is None or attempt['learner'] == selected]
    return {'scores': rows, 'comparison': 'raw_within_form_only'}


def classes(store, query):
    rows = scores(store, query)['scores']
    summaries = []
    for form in store.table('forms'):
        group = [row for row in rows if row['form'] == form['form']]
        summaries.append({'form': form['form'], 'attempts': len(group),
                          'mean_raw_fraction': mean(row['raw_fraction'] for row in group),
                          'learners': len({row['learner'] for row in group})})
    return {'forms': summaries}


ROUTES = {'/api/scores': scores, '/api/classes': classes}
