# FastTrack

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
git clone https://github.com/Jacob-Chamney/FastTrack
cd FastTrack
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
## Roadmap

### Done
- [x] Task groups as tabs
- [x] Add / check off / delete tasks
- [x] Per-group progress bar
- [x] Task notes with edit/save
- [x] Delete groups (when empty or fully complete)
- [x] Save / Save As / Open projects (JSON)
- [x] Refactor into a class and split into modules

### Up next
- [ ] `TaskRow` widget class (`widgets.py`)
- [ ] `GroupPage` widget class to replace the per-group dicts
- [ ] Save As button
- [ ] Show current file name in the window title
- [ ] Warn about unsaved changes before closing / opening

### Planned features
- [ ] **Task priority**: low / medium / high, shown on each row and sortable
- [ ] **Due dates & time frames**: due date per task, start–end ranges, overdue highlighting
- [ ] **Theme customization**: light / dark / system toggle plus custom color themes

### Styling
- [ ] File / Edit / View menu bar
- [ ] Keyboard shortcuts (Ctrl+S, Ctrl+O, …)
- [ ] Fonts and spacing pass
- [ ] Hand-drawn "sketch" style borders

### Ideas
- [ ] Rename groups and tasks
- [ ] Drag to reorder tasks
