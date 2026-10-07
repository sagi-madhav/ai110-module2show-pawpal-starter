"""main.py

Demo script for PawPal+.
Demonstrates:
- Adding tasks with times out of order
- Chronological sorting (sort_by_time)
- Filtering by pet and completion status (filter_tasks)
- Recurring tasks (daily/weekly auto-renewal)
- Conflict detection warning when two tasks share the same time slot
"""

from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    print("========================================")
    print("        PawPal+ Demo Walkthrough        ")
    print("========================================\n")

    # 1. Setup owner and pets
    owner = Owner(name="Alex", available_time_minutes=60)
    milo = Pet(name="Milo", species="dog")
    luna = Pet(name="Luna", species="cat")

    owner.add_pet(milo)
    owner.add_pet(luna)

    # 2. Add tasks out of order with scheduled times
    # Note: Both Morning Walk and Breakfast are at 08:00 to test conflict detection!
    milo.add_task(
        Task(
            title="Evening Walk",
            duration_minutes=20,
            priority="medium",
            time="18:30",
            frequency="daily",
        )
    )
    milo.add_task(
        Task(
            title="Morning Walk",
            duration_minutes=25,
            priority="high",
            time="08:00",
            frequency="daily",
        )
    )
    luna.add_task(
        Task(
            title="Breakfast & Meds",
            duration_minutes=15,
            priority="high",
            time="08:00",
            frequency="daily",
        )
    )
    luna.add_task(
        Task(
            title="Playtime",
            duration_minutes=15,
            priority="low",
            time="13:00",
            frequency="once",
        )
    )

    scheduler = Scheduler(time_limit_minutes=60)
    all_tasks = owner.get_all_tasks()

    # 3. Test Chronological Sorting
    print("--- 1. Chronological Sorting (sort_by_time) ---")
    sorted_tasks = scheduler.sort_by_time(all_tasks)
    for t in sorted_tasks:
        print(f"  [{t.time}] {t.title} ({t.pet_name}) - {t.duration_minutes} min")
    print()

    # 4. Test Filtering
    print("--- 2. Filtering Tasks (Luna's tasks only) ---")
    luna_tasks = scheduler.filter_tasks(all_tasks, pet_name="Luna")
    for t in luna_tasks:
        print(f"  {t.title} for {t.pet_name} [Completed: {t.is_completed}]")
    print()

    # 5. Test Recurring Task Completion
    print("--- 3. Recurring Task Automation ---")
    first_task = milo.tasks[0]  # Evening Walk (daily)
    print(f"Completing task: '{first_task.title}' on {date.today()}...")
    next_occurrence = milo.mark_task_complete(first_task, current_date=date.today())
    print(f"  Old task is_completed: {first_task.is_completed}")
    print(
        f"  Next occurrence created: '{next_occurrence.title}' due on {next_occurrence.due_date}"
    )
    print(f"  Milo's current pending tasks: {[t.title for t in milo.get_pending_tasks()]}\n")

    # 6. Test Scheduling and Conflict Detection
    print("--- 4. Today's Generated Schedule & Conflict Warning ---")
    scheduler.schedule_for_owner(owner)
    print(scheduler.get_summary())


if __name__ == "__main__":
    main()
