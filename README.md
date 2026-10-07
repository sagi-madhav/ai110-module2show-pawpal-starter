# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🛠️ Implementation Summary

PawPal+ is organized into four core classes that collaborate to manage pet tasks and build daily schedules:

- **`Task`**: Represents an individual activity (title, duration in minutes, priority, frequency, and completion status). When added to a pet, it stores the pet's name for clarity.
- **`Pet`**: Represents an individual pet (name, species) and maintains a collection of assigned tasks.
- **`Owner`**: Represents the user, their daily time budget, and their pets. Its `get_all_tasks()` method aggregates pending tasks across all pets.
- **`Scheduler`**: The planning engine. It retrieves all tasks from the owner, ranks them by priority and duration, fits them into the owner's time constraint, and produces a transparent daily schedule with reasoning for each decision.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```text
=== Today's Pet Care Schedule ===
Available Time Budget: 60 minutes
Total Scheduled Time: 60 minutes

Warnings & Detected Conflicts:
  [!] Time conflict at 08:00: 'Morning Walk' (Milo), 'Breakfast & Meds' (Luna) are scheduled at the same time.

Scheduled Tasks:
  1. Breakfast & Meds (Luna) at 08:00 - 15 mins [High priority]
  2. Morning Walk (Milo) at 08:00 - 25 mins [High priority]
  3. Evening Walk (Milo) at 18:30 - 20 mins [Medium priority]

Skipped Tasks (Exceeded Time Budget):
  1. Playtime (Luna) at 13:00 - 15 mins [Low priority]

Why This Plan Was Chosen:
  - Scheduled 'Breakfast & Meds' for Luna at 08:00 (15 min, high priority) - fits within time budget (15/60 min used).
  - Scheduled 'Morning Walk' for Milo at 08:00 (25 min, high priority) - fits within time budget (40/60 min used).
  - Scheduled 'Evening Walk' for Milo at 18:30 (20 min, medium priority) - fits within time budget (60/60 min used).
  - Skipped 'Playtime' for Luna at 13:00 (15 min, low priority) - needs 15 min, but only 0 min remain.
```

## 🧪 Testing PawPal+

Run the automated test suite from the project root using:

```bash
python -m pytest
```

### What the Tests Cover
Our test suite includes 11 automated test cases verifying both standard workflows and edge cases:
- **Task Management**: Validates `mark_complete()` state changes, pet-to-task association, and multi-pet aggregation under an owner.
- **Sorting Correctness**: Checks that `sort_by_time()` returns tasks in chronological order while handling tasks without a set time.
- **Filtering Logic**: Confirms filtering by pet name, completion status, and combined criteria.
- **Recurrence Logic**: Verifies that completing daily (+1 day) and weekly (+7 days) tasks automatically enqueues the next occurrence with the correct `due_date`.
- **Conflict Detection**: Checks that overlapping start times across pets produce clear warning messages, while unique times produce none.
- **Edge Cases & Budget Limits**: Ensures the scheduler handles empty task lists without crashing and correctly skips tasks that exceed available time limits.

### Sample Test Output

```text
============================= test session starts =============================
platform win32 -- Python 3.12.4, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\Code\CodePath\ai110-module2show-pawpal-starter
plugins: anyio-4.15.1
collected 11 items

tests\test_pawpal.py ...........                                         [100%]

============================= 11 passed in 0.02s ==============================
```

**Confidence Level:** ⭐⭐⭐⭐⭐ (5/5 stars)
The test suite validates every core requirement, edge case, and boundary condition with fast and reliable test execution.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` & `Scheduler.generate_plan()` | Chronological sorting by "HH:MM" string, plus priority and duration weighting |
| Filtering | `Scheduler.filter_tasks()` | Filters tasks by completion status (`is_completed`) and/or `pet_name` |
| Conflict handling | `Scheduler.detect_conflicts()` | Identifies shared time slots across pets and outputs non-fatal warnings |
| Recurring tasks | `Task.mark_complete()` & `Pet.mark_task_complete()` | Calculates next due date with `timedelta` for daily (+1 day) and weekly (+7 days) tasks |

### Features Overview
- **Sorting Behavior (`Scheduler.sort_by_time`)**: Arranges tasks chronologically by their "HH:MM" start time using Python's `sorted()` function with a lambda key. During plan generation, tasks are prioritized by urgency and duration.
- **Filtering Behavior (`Scheduler.filter_tasks`)**: Enables owners to filter tasks by completion state (`is_completed`) or specific pet name (`pet_name`), making it easy to focus on what still needs to be done.
- **Conflict Detection Logic (`Scheduler.detect_conflicts`)**: Scans scheduled times across all pets and flags instances where multiple tasks share the same time slot, outputting friendly warning alerts.
- **Recurring Task Logic (`Task.mark_complete` / `Pet.mark_task_complete`)**: Automatically schedules the next occurrence for daily (+1 day) or weekly (+7 days) tasks using Python's `timedelta`.

## 📸 Demo Walkthrough

Follow these steps to explore all features of PawPal+ either via the interactive Streamlit UI or the command-line demo script:

### Main Features & Actions
- **Owner & Time Settings**: Customize the owner's name and set a daily pet care time budget (e.g., 60 minutes).
- **Pet Registration**: Add multiple pets with distinct names and species (e.g., dogs, cats, birds).
- **Task Management**: Create care tasks with specific durations, priorities (high/medium/low), frequencies (daily/weekly/once), and optional scheduled times ("HH:MM").
- **Live Filtering & Sorting**: Filter tasks by a specific pet and view tasks sorted chronologically by time.
- **Smart Schedule Generation**: Click **Generate Schedule** to let the scheduler prioritize urgent tasks, pack them into the available time budget, flag any time conflicts, and provide clear explanations.

### Example Workflow
1. **Launch the App**: Run `streamlit run app.py` and set your daily available time budget to 60 minutes.
2. **Register Your Pets**: Add `Milo` (dog) and `Luna` (cat) in the Owner & Pet Settings section.
3. **Add Tasks**:
   - Add *Morning Walk* for Milo (25 min, High priority, 08:00, daily).
   - Add *Breakfast & Meds* for Luna (15 min, High priority, 08:00, daily).
   - Add *Evening Walk* for Milo (20 min, Medium priority, 18:30, daily).
   - Add *Playtime* for Luna (15 min, Low priority, 13:00, once).
4. **Inspect Tasks**: Toggle the "Filter by Pet" dropdown or check "Sort Chronologically" to see the organized task overview.
5. **Generate the Schedule**: Click **Generate Schedule**.
   - The scheduler flags a time conflict alert because both Milo's walk and Luna's meds are set for 08:00.
   - The scheduler schedules the 3 highest-priority tasks (totaling 60 minutes).
   - Low-priority *Playtime* is deferred because the 60-minute time budget was fully utilized.
   - An explanation block details each decision.

### Sample CLI Demo Output (`python main.py`)

```text
========================================
        PawPal+ Demo Walkthrough        
========================================

--- 1. Chronological Sorting (sort_by_time) ---
  [08:00] Morning Walk (Milo) - 25 min
  [08:00] Breakfast & Meds (Luna) - 15 min
  [13:00] Playtime (Luna) - 15 min
  [18:30] Evening Walk (Milo) - 20 min

--- 2. Filtering Tasks (Luna's tasks only) ---
  Breakfast & Meds for Luna [Completed: False]
  Playtime for Luna [Completed: False]

--- 3. Recurring Task Automation ---
Completing task: 'Evening Walk' on 2026-10-07...
  Old task is_completed: True
  Next occurrence created: 'Evening Walk' due on 2026-10-08
  Milo's current pending tasks: ['Morning Walk', 'Evening Walk']

--- 4. Today's Generated Schedule & Conflict Warning ---
=== Today's Pet Care Schedule ===
Available Time Budget: 60 minutes
Total Scheduled Time: 60 minutes

Warnings & Detected Conflicts:
  [!] Time conflict at 08:00: 'Morning Walk' (Milo), 'Breakfast & Meds' (Luna) are scheduled at the same time.

Scheduled Tasks:
  1. Breakfast & Meds (Luna) at 08:00 - 15 mins [High priority]
  2. Morning Walk (Milo) at 08:00 - 25 mins [High priority]
  3. Evening Walk (Milo) at 18:30 - 20 mins [Medium priority]

Skipped Tasks (Exceeded Time Budget):
  1. Playtime (Luna) at 13:00 - 15 mins [Low priority]

Why This Plan Was Chosen:
  - Scheduled 'Breakfast & Meds' for Luna at 08:00 (15 min, high priority) - fits within time budget (15/60 min used).
  - Scheduled 'Morning Walk' for Milo at 08:00 (25 min, high priority) - fits within time budget (40/60 min used).
  - Scheduled 'Evening Walk' for Milo at 18:30 (20 min, medium priority) - fits within time budget (60/60 min used).
  - Skipped 'Playtime' for Luna at 13:00 (15 min, low priority) - needs 15 min, but only 0 min remain.
```
