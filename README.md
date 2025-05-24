# 🐉 Monster Rancher 2 DX Trainer

An AI-powered agentic system that builds **optimal training schedules** for any monster in **Monster Rancher 2 DX**.

> ⚙️ Powered by modular agents that analyze stats, simulate outcomes, and generate complete week-by-week plans.

---

## 📦 What It Does

This tool:
- Analyzes monster growth rates, lifespan, and battle needs
- Simulates training outcomes using actual drill and item effects
- Optimizes for target stats (like INT/SPD or POW/SKI)
- Avoids fatigue/stress death and poor condition
- Outputs a clean Markdown training guide

---

## 🧠 Agents in the System

| Agent Name     | Role                                      |
|----------------|-------------------------------------------|
| `THE CURATOR`  | Parses and cleans monster, drill, item CSVs |
| `THE ANALYST`  | Profiles your monster’s growth needs      |
| `THE PLANNER`  | Builds a week-by-week drill plan          |
| `THE SIMULATOR`| Runs a virtual training sim               |
| `THE OPTIMIZER`| Fixes schedule flaws (overfatigue, etc)   |
| `THE PRESENTER`| Outputs clean, player-readable reports    |

---

## 🚀 Getting Started

### 1. Install dependencies

```bash
pip install pandas numpy orjson python-dateutil rich
```

### Rest Weeks

Add a week to your plan with `"drill": "Rest"` to skip training and recover extra
fatigue and stress. The simulator applies an additional **-20 fatigue** and
**-10 stress** on top of normal weekly recovery when it encounters a Rest entry.
