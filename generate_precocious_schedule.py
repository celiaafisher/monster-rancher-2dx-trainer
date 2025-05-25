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

    # Stages 1 & 2: light drills for 8 months (weeks 1-32)
    # No weekly items are used during the early "baby" stage
    for month in range(8):
        add_entry(schedule, week, "Study", notes="loyalty build", food="Cup Jelly")
        add_entry(schedule, week + 1, "Dodge")
        add_entry(schedule, week + 2, "Run")
        add_entry(schedule, week + 3, "Rest")
        week += 4

    # Stage 3: ramp up with heavy drills for 8 months (weeks 33-64)
    # Items are only supplied when the monster is working hard
    for month in range(8):
        add_entry(schedule, week, "Meditate", "Nuts Oil", "heavy training", food="Cup Jelly")
        add_entry(schedule, week + 1, "Leap", "Mint Leaf", "stress relief from heavy work")
        add_entry(schedule, week + 2, "Study")
        add_entry(schedule, week + 3, "Rest")
        week += 4

    # Stages 4-6: prime heavy training for 17 months (weeks 65-132)
    # Alternate between fatigue reduction and stress relief items
    for month in range(17):
        add_entry(schedule, week, "Meditate", "Nuts Oil", "prime heavy", food="Cup Jelly")
        drill = "Run" if month % 2 else "Leap"
        add_entry(schedule, week + 1, drill, "Mint Leaf", "stress relief after heavy work")
        add_entry(schedule, week + 2, "Dodge")
        add_entry(schedule, week + 3, "Rest")
        week += 4

    # Stage 7+: taper with light maintenance drills until week 340
    # No weekly items unless heavy work is scheduled
    while week <= 340:
        add_entry(schedule, week, "Study", notes="maintenance", food="Cup Jelly")
        if week + 1 <= 340:
            add_entry(schedule, week + 1, "Dodge")
        if week + 2 <= 340:
            add_entry(schedule, week + 2, "Run")
        if week + 3 <= 340:
            add_entry(schedule, week + 3, "Rest")
        week += 4

    return schedule


if __name__ == "__main__":
    schedule = generate_schedule()
    with open("planner_schedule_full.json", "w") as f:
        json.dump({"schedule": schedule}, f, indent=2)
