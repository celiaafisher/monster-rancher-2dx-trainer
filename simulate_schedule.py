import json

# Load data
with open('curated_data.json') as f:
    data = json.load(f)

with open('planner_schedule.json') as f:
    schedule_data = json.load(f)

# Monster base stats
stats = {entry['stat'].upper(): entry['base'] for entry in data['monsters']}

# Starting values
loyalty = 50
fatigue = 0
stress = 0.0
lifespan_used = 0

NAT_FATIGUE_RECOVER = 10
NAT_STRESS_RECOVER = 5

# Map drills to info
drill_info = {d['drill']: d for d in data['drills']}

# Item effects mapping
item_effects = {
    'Nuts Oil': {'fatigue': -28, 'stress_mult': 0.8, 'loyalty': 1},
    'Mint Leaf': {'fatigue': 0, 'stress_mult': 0.5, 'loyalty': -1},
    'Candy': {'fatigue': 0, 'stress_delta': -2, 'loyalty': 1},
    'Mango': {'fatigue': -10, 'stress_delta': 0, 'loyalty': 1},
}

def apply_item(item, fatigue, stress, loyalty):
    eff = item_effects.get(item, {})
    fatigue += eff.get('fatigue', 0)
    if 'stress_mult' in eff:
        stress *= eff['stress_mult']
    stress += eff.get('stress_delta', 0)
    loyalty += eff.get('loyalty', 0)
    if fatigue < 0:
        fatigue = 0
    if stress < 0:
        stress = 0
    return fatigue, stress, loyalty

run_log = []

for week_entry in schedule_data['schedule']:
    week = week_entry['week']
    drill = week_entry['drill']
    item = week_entry['item']

    # natural recovery at start of week (except week 1)
    if week > 1:
        fatigue = max(0, fatigue - NAT_FATIGUE_RECOVER)
        stress = max(0, stress - NAT_STRESS_RECOVER)

    if drill == 'Rest':
        # additional recovery when resting
        fatigue = max(0, fatigue - 20)
        stress = max(0, stress - 10)
    else:
        d = drill_info[drill]
        heavy = d['type'] == 'Heavy'

        # apply drill stats
        main_stat = d['main+'].upper()
        sub_stat = d.get('sub+')
        drop_stat = d.get('drop-')

        stats[main_stat] = stats.get(main_stat, 0) + (12 if heavy else 4)
        if sub_stat:
            stats[sub_stat.upper()] = stats.get(sub_stat.upper(), 0) + (4 if heavy else 0)
        if drop_stat:
            stats[drop_stat.upper()] = stats.get(drop_stat.upper(), 0) - (4 if heavy else 0)

        stress += d['stresschange']
        fatigue += d['fatiguechange']

        # praise after drill
        loyalty += 1

    # apply item
    fatigue, stress, loyalty = apply_item(item, fatigue, stress, loyalty)

    # track lifespan
    lifespan_used += 1

    run_log.append({
        'week': week,
        'stats': {k: int(v) for k, v in stats.items()},
        'fatigue': round(fatigue, 2),
        'stress': round(stress, 2),
        'loyalty': loyalty
    })

final_stats = {k: int(v) for k, v in stats.items()}
final_stats['loyalty'] = loyalty

breaches = []
for entry in run_log:
    if entry['fatigue'] > 40:
        breaches.append({'week': entry['week'], 'type': 'fatigue', 'value': entry['fatigue']})
    if entry['stress'] > 30:
        breaches.append({'week': entry['week'], 'type': 'stress', 'value': entry['stress']})

sim_notes = f"Simulated {len(run_log)} weeks. Lifespan used: {lifespan_used}."

output = {
    'run_log': run_log,
    'final_stats': final_stats,
    'breaches': breaches,
    'sim_notes': sim_notes
}

print(json.dumps(output, indent=2))

