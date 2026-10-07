"""tests/test_pawpal.py

Comprehensive automated test suite for PawPal+.
Tests happy paths and key edge cases:
- Task completion and pet task management
- Multi-pet owner task aggregation
- Chronological sorting (including tasks without time)
- Multi-criteria filtering
- Recurring tasks (daily and weekly calculation via timedelta)
- Time conflict detection (positive and negative cases)
- Time budget constraints (budget limits and empty task lists)
"""

from datetime import date, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler


def test_task_completion():
    """Verify that calling mark_complete() updates completion status."""
    task = Task(title="Evening walk", duration_minutes=20, priority="medium")
    assert task.is_completed is False

    task.mark_complete()
    assert task.is_completed is True


def test_task_addition_and_pet_assignment():
    """Verify that adding a task to a Pet increases count and links pet name."""
    pet = Pet(name="Milo", species="dog")
    assert len(pet.tasks) == 0

    task = Task(title="Morning feeding", duration_minutes=10, priority="high")
    pet.add_task(task)

    assert len(pet.tasks) == 1
    assert pet.tasks[0].title == "Morning feeding"
    assert pet.tasks[0].pet_name == "Milo"


def test_owner_aggregates_multiple_pets():
    """Verify Owner.get_all_tasks gathers pending tasks from all pets."""
    owner = Owner(name="Alex", available_time_minutes=90)
    milo = Pet(name="Milo", species="dog")
    luna = Pet(name="Luna", species="cat")

    milo.add_task(Task(title="Dog walk", duration_minutes=30))
    luna.add_task(Task(title="Cat brushing", duration_minutes=15))

    owner.add_pet(milo)
    owner.add_pet(luna)

    all_tasks = owner.get_all_tasks()
    assert len(all_tasks) == 2
    pet_names = {t.pet_name for t in all_tasks}
    assert pet_names == {"Milo", "Luna"}


def test_sort_by_time_chronological():
    """Verify tasks are returned in chronological order based on HH:MM time."""
    scheduler = Scheduler()
    t1 = Task(title="Dinner", duration_minutes=10, time="18:00")
    t2 = Task(title="Breakfast", duration_minutes=10, time="08:00")
    t3 = Task(title="Lunch", duration_minutes=10, time="12:30")
    t4 = Task(title="Anytime task", duration_minutes=15, time=None)

    sorted_tasks = scheduler.sort_by_time([t1, t2, t3, t4])
    assert [t.title for t in sorted_tasks[:3]] == ["Breakfast", "Lunch", "Dinner"]
    assert sorted_tasks[3].title == "Anytime task"


def test_filter_tasks_by_pet_and_status():
    """Verify filtering by pet name, completion status, and combined criteria."""
    scheduler = Scheduler()
    t1 = Task(title="Walk", duration_minutes=20, pet_name="Milo", is_completed=False)
    t2 = Task(title="Meds", duration_minutes=5, pet_name="Luna", is_completed=True)
    t3 = Task(title="Brush", duration_minutes=10, pet_name="Luna", is_completed=False)

    tasks = [t1, t2, t3]

    # Filter by pet
    assert len(scheduler.filter_tasks(tasks, pet_name="Luna")) == 2

    # Filter by completion
    assert len(scheduler.filter_tasks(tasks, completed=True)) == 1
    assert scheduler.filter_tasks(tasks, completed=True)[0].title == "Meds"

    # Filter combined
    luna_pending = scheduler.filter_tasks(tasks, pet_name="Luna", completed=False)
    assert len(luna_pending) == 1
    assert luna_pending[0].title == "Brush"


def test_recurring_daily_task_due_date():
    """Verify that completing a daily task creates a next occurrence for tomorrow."""
    pet = Pet(name="Milo")
    base_date = date(2026, 10, 7)
    task = Task(title="Daily walk", duration_minutes=30, frequency="daily", due_date=base_date)
    pet.add_task(task)

    next_task = pet.mark_task_complete(task, current_date=base_date)

    assert task.is_completed is True
    assert next_task is not None
    assert next_task.due_date == base_date + timedelta(days=1)
    assert next_task.is_completed is False
    assert len(pet.tasks) == 2


def test_recurring_weekly_task_due_date():
    """Verify that completing a weekly task creates a next occurrence 7 days later."""
    pet = Pet(name="Luna")
    base_date = date(2026, 10, 7)
    task = Task(title="Weekly bath", duration_minutes=25, frequency="weekly", due_date=base_date)
    pet.add_task(task)

    next_task = pet.mark_task_complete(task, current_date=base_date)

    assert task.is_completed is True
    assert next_task is not None
    assert next_task.due_date == base_date + timedelta(days=7)
    assert len(pet.tasks) == 2


def test_conflict_detection_flags_duplicate_times():
    """Verify scheduler detects when tasks share the exact same scheduled time."""
    scheduler = Scheduler()
    t1 = Task(title="Walk", duration_minutes=30, time="09:00", pet_name="Milo")
    t2 = Task(title="Vet visit", duration_minutes=45, time="09:00", pet_name="Luna")
    t3 = Task(title="Dinner", duration_minutes=10, time="18:00", pet_name="Milo")

    warnings = scheduler.detect_conflicts([t1, t2, t3])
    assert len(warnings) == 1
    assert "09:00" in warnings[0]


def test_conflict_detection_no_warnings_for_distinct_times():
    """Verify no conflict warnings are raised when all task times are unique."""
    scheduler = Scheduler()
    t1 = Task(title="Breakfast", duration_minutes=15, time="08:00")
    t2 = Task(title="Lunch", duration_minutes=15, time="12:00")

    warnings = scheduler.detect_conflicts([t1, t2])
    assert len(warnings) == 0


def test_scheduler_handles_empty_tasks_gracefully():
    """Edge case: Scheduler safely handles an owner or pet with zero tasks."""
    scheduler = Scheduler(time_limit_minutes=60)
    plan = scheduler.generate_plan([])

    assert plan == []
    assert len(scheduler.scheduled_tasks) == 0
    assert len(scheduler.skipped_tasks) == 0
    assert "Scheduled Tasks: None" in scheduler.get_summary()


def test_scheduler_enforces_time_budget_and_skips_overflow():
    """Verify scheduler respects available time limit and records skipped tasks."""
    scheduler = Scheduler(time_limit_minutes=40)
    t1 = Task(title="Crucial Meds", duration_minutes=10, priority="high")
    t2 = Task(title="Long Hike", duration_minutes=30, priority="high")
    t3 = Task(title="Playtime", duration_minutes=15, priority="low")

    plan = scheduler.generate_plan([t1, t2, t3])

    assert len(plan) == 2
    assert t1 in plan
    assert t2 in plan
    assert len(scheduler.skipped_tasks) == 1
    assert scheduler.skipped_tasks[0].title == "Playtime"
