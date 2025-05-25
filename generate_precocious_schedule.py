import json


def add_entry(schedule, week, drill, item="None", notes="", food=None):
    """Helper to append a weekly schedule entry."""
    entry = {
        "week": week,
        "drill": drill,
        "item": item,
        "notes": notes,
    }
    if food:
        entry["food"] = food
    schedule.append(entry)


def generate_schedule():
    schedule = []
    week = 1

    # Stages 1 & 2: focus on INT with SKILL support for the first 8 months
    for month in range(8):
        add_entry(schedule, week, "Study", notes="loyalty build", food="Cup Jelly")
        add_entry(schedule, week + 1, "Shoot")
        item = "Nuts Oil" if month % 2 == 0 else "Mint Leaf"
        add_entry(schedule, week + 2, "Meditate", item)
        add_entry(schedule, week + 3, "Rest")
        week += 4

    # Stage 3: ramp up with heavy INT drills (weeks 33-64)
    for month in range(8):
        add_entry(schedule, week, "Meditate", "Nuts Oil", "heavy INT", food="Cup Jelly")
        add_entry(schedule, week + 1, "Shoot", "Mint Leaf", "stress relief from heavy work")
        add_entry(schedule, week + 2, "Study")
        add_entry(schedule, week + 3, "Rest")
        week += 4

    # Stages 4-6: prime heavy INT training for 17 months (weeks 65-132)
    for month in range(17):
        add_entry(schedule, week, "Meditate", "Nuts Oil", "prime heavy", food="Cup Jelly")
        add_entry(schedule, week + 1, "Shoot", "Mint Leaf", "stress relief after heavy work")
        add_entry(schedule, week + 2, "Study")
        add_entry(schedule, week + 3, "Rest")
        week += 4

    # Stage 7+: taper with light maintenance focused on INT and SKILL
    while week <= 340:
        add_entry(schedule, week, "Study", notes="maintenance", food="Cup Jelly")
        if week + 1 <= 340:
            add_entry(schedule, week + 1, "Shoot")
        if week + 2 <= 340:
            add_entry(schedule, week + 2, "Meditate")
        if week + 3 <= 340:
            add_entry(schedule, week + 3, "Rest")
        week += 4

    return schedule


if __name__ == "__main__":
    schedule = generate_schedule()
    with open("planner_schedule_full.json", "w") as f:
        json.dump({"schedule": schedule}, f, indent=2)
