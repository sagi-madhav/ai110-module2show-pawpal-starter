"""main.py

Terminal script for PawPal+.
Demonstrates:
- Adding tasks with times out of order
- Chronological sorting (sort_by_time)
- Filtering by pet (filter_tasks)
- Generating Today's Schedule with conflict detection
"""

from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    # 1. Setup owner and pets
    owner = Owner(name="Alex", available_time_minutes=60)
    milo = Pet(name="Milo", species="dog")
    luna = Pet(name="Luna", species="cat")

    owner.add_pet(milo)
    owner.add_pet(luna)

    # 2. Add tasks out of order (two at 08:00 to test conflict detection)
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

    # 3. Print chronologically sorted tasks
    print("Tasks Sorted Chronologically:")
    for t in scheduler.sort_by_time(all_tasks):
        print(f"[{t.time}] {t.title} ({t.pet_name}) - {t.duration_minutes} min")
    print()

    # 4. Print filtered tasks (Luna only)
    print("Filtered Tasks for Luna:")
    for t in scheduler.filter_tasks(all_tasks, pet_name="Luna"):
        print(f"{t.title} ({t.pet_name})")
    print()

    # 5. Generate and print Today's Schedule (includes conflict warning)
    scheduler.schedule_for_owner(owner)
    print(scheduler.get_summary())


if __name__ == "__main__":
    main()
