import json
import random
import sys

# Load data
with open('curated_data.json') as f:
    data = json.load(f)

schedule_path = sys.argv[1] if len(sys.argv) > 1 else 'planner_schedule.json'
with open(schedule_path) as f:
    schedule_data = json.load(f)

# Monster base stats
stats = {entry['stat'].upper(): entry['base'] for entry in data['monsters']}

# Starting values
# The game derives Loyalty from two hidden stats: Fear and Spoil.
# We track them explicitly so loyalty can be computed more accurately.
fear = 0
spoil = 0
fatigue = 0
stress = 0.0
lifespan_used = 0
loyalty = int(round((fear + spoil) / 2))

NAT_FATIGUE_RECOVER = 10
NAT_STRESS_RECOVER = 5

# Training outcome chances for gating praise/scold actions
# Great and Fail events open praise or scold opportunities
# Normal weeks give no loyalty change from handling

# Max items allowed in a 4-week block
MAX_ITEMS_PER_MONTH = 2

# Map drills to info
drill_info = {d['drill']: d for d in data['drills']}

# Item effects mapping
item_effects = {
    'Nuts Oil': {'fatigue': -28, 'stress_mult': 0.8, 'loyalty': 1},
    'Mint Leaf': {'fatigue': 0, 'stress_mult': 0.5, 'loyalty': -1},
    'Candy': {'fatigue': 0, 'stress_delta': -2, 'loyalty': 1},
    'Mango': {'fatigue': -10, 'stress_delta': 0, 'loyalty': 1},
}

def clamp(value, lo=0, hi=100):
    return max(lo, min(value, hi))

def apply_item(item, fatigue, stress, fear, spoil):
    """Apply item effects including loyalty adjustments via fear/spoil."""
    eff = item_effects.get(item, {})
    fatigue += eff.get('fatigue', 0)
    if 'stress_mult' in eff:
        stress *= eff['stress_mult']
    stress += eff.get('stress_delta', 0)

    loyalty_delta = eff.get('loyalty', 0)
    if loyalty_delta:
        # Convert direct loyalty change into spoil adjustments.
        spoil += loyalty_delta * 2

    fatigue = max(0, fatigue)
    stress = max(0, stress)
    fear = clamp(fear)
    spoil = clamp(spoil)
    return fatigue, stress, fear, spoil

run_log = []
warnings = []
breaches = []
items_in_month = 0
current_month = 1
months_warned = set()

for week_entry in schedule_data['schedule']:
    week = week_entry['week']
    drill = week_entry['drill']
    item = week_entry['item']

    month = (week - 1) // 4 + 1
    if month != current_month:
        current_month = month
        items_in_month = 0

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

        notes = week_entry.get('notes', '').lower()

        # Determine training outcome
        outcome = random.choices(
            ['great', 'fail', 'cheat', 'normal'],
            weights=[0.1, 0.1, 0.05, 0.75]
        )[0]

        # adjust fear/spoil based on outcome and handling
        if outcome == 'great':
            if 'praise' in notes:
                spoil += 6
            else:
                fear += 10
                spoil -= 24
        elif outcome == 'fail':
            if 'scold' in notes:
                fear += 15
                spoil -= 15
        elif outcome == 'cheat':
            if 'scold' in notes:
                spoil -= 6

        # keep values within 0-100 bounds
        fear = clamp(fear)
        spoil = clamp(spoil)

        week_entry['outcome'] = outcome

    # apply item with monthly limit enforcement
    if item and item.lower() != 'none':
        if items_in_month >= MAX_ITEMS_PER_MONTH:
            if current_month not in months_warned:
                warnings.append(
                    f"Month {current_month} uses more than {MAX_ITEMS_PER_MONTH} items. Extras ignored."
                )
                months_warned.add(current_month)
            breaches.append({'week': week, 'type': 'item_limit', 'item': item})
            item = 'None'
        else:
            items_in_month += 1

    fatigue, stress, fear, spoil = apply_item(item, fatigue, stress, fear, spoil)

    # compute loyalty from current fear and spoil levels
    loyalty = int(round((fear + spoil) / 2))

    # track lifespan
    lifespan_used += 1

    run_log.append({
        'week': week,
        'stats': {k: int(v) for k, v in stats.items()},
        'fatigue': round(fatigue, 2),
        'stress': round(stress, 2),
        'fear': fear,
        'spoil': spoil,
        'loyalty': loyalty,
        'outcome': week_entry.get('outcome', 'normal')
    })

final_stats = {k: int(v) for k, v in stats.items()}
final_stats.update({'fear': fear, 'spoil': spoil, 'loyalty': loyalty})
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
    'sim_notes': sim_notes,
    'warnings': warnings
}

print(json.dumps(output, indent=2))

