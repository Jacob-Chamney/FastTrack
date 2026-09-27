# Progress Tracker

A simple desktop to-do app built with **CustomTkinter**. Organize tasks into groups,
track progress per group, and keep notes on each task.

## Features

- Task groups as tabs
- Per-group progress bar
- Notes for each task, with edit/save
- Save and open projects as `.json` files

## Requirements

- Python 3.10+
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)

## Getting started

```bash
git clone <your repo URL>
cd ProgressTracker
pip install -r requirements.txt
python main.py
```

## Project structure

```
main.py      # entry point
app.py       # main App window and logic
storage.py   # JSON save/load
widgets.py   # custom widgets (WIP)
```
