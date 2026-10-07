"""tests/test_pawpal.py

Unit tests for PawPal+ core classes.
Tests task management, multi-pet scheduling, sorting, filtering, recurring tasks, and conflict detection.
"""

from datetime import date, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler


def test_task_completion():
    """Verify that calling mark_complete() changes the task's completion status."""
    task = Task(title="Evening walk", duration_minutes=20, priority="medium")
    assert task.is_completed is False

    task.mark_complete()
    assert task.is_completed is True


def test_task_addition():
    """Verify that adding a task to a Pet increases the pet's task count."""
    pet = Pet(name="Milo", species="dog")
    assert len(pet.tasks) == 0

    task = Task(title="Morning feeding", duration_minutes=10, priority="high")
    pet.add_task(task)

    assert len(pet.tasks) == 1
    assert pet.tasks[0].title == "Morning feeding"
    assert pet.tasks[0].pet_name == "Milo"


def test_sort_by_time():
    """Verify that Scheduler sorts tasks chronologically by their time string."""
    scheduler = Scheduler()
    t1 = Task(title="Dinner", duration_minutes=10, time="18:00")
    t2 = Task(title="Breakfast", duration_minutes=10, time="08:00")
    t3 = Task(title="Lunch", duration_minutes=10, time="12:30")

    sorted_tasks = scheduler.sort_by_time([t1, t2, t3])
    assert [t.time for t in sorted_tasks] == ["08:00", "12:30", "18:00"]


def test_filter_tasks():
    """Verify filtering by pet name and completion status."""
    scheduler = Scheduler()
    t1 = Task(title="Walk", duration_minutes=20, pet_name="Milo", is_completed=False)
    t2 = Task(title="Meds", duration_minutes=5, pet_name="Luna", is_completed=True)
    t3 = Task(title="Brush", duration_minutes=10, pet_name="Luna", is_completed=False)

    all_tasks = [t1, t2, t3]

    # Filter by pet
    luna_tasks = scheduler.filter_tasks(all_tasks, pet_name="Luna")
    assert len(luna_tasks) == 2

    # Filter by completion
    pending = scheduler.filter_tasks(all_tasks, completed=False)
    assert len(pending) == 2

    # Filter by both
    luna_pending = scheduler.filter_tasks(all_tasks, pet_name="Luna", completed=False)
    assert len(luna_pending) == 1
    assert luna_pending[0].title == "Brush"


def test_recurring_daily_task():
    """Verify that daily recurring tasks produce a new occurrence for the next day."""
    pet = Pet(name="Milo")
    today = date(2026, 10, 7)
    task = Task(title="Walk", duration_minutes=30, frequency="daily", due_date=today)
    pet.add_task(task)

    next_task = pet.mark_task_complete(task, current_date=today)
    assert task.is_completed is True
    assert next_task is not None
    assert next_task.due_date == today + timedelta(days=1)
    assert next_task.is_completed is False
    assert len(pet.tasks) == 2


def test_conflict_detection():
    """Verify that scheduler detects when two tasks share the same time slot."""
    scheduler = Scheduler()
    t1 = Task(title="Walk", duration_minutes=30, time="09:00", pet_name="Milo")
    t2 = Task(title="Vet visit", duration_minutes=45, time="09:00", pet_name="Luna")
    t3 = Task(title="Dinner", duration_minutes=10, time="18:00", pet_name="Milo")

    warnings = scheduler.detect_conflicts([t1, t2, t3])
    assert len(warnings) == 1
    assert "09:00" in warnings[0]
