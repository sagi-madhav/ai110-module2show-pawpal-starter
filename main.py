"""main.py

Demo script for PawPal+ to verify the logic layer in the terminal.
Demonstrates multi-pet support, priority-based scheduling, and clear explanations.
"""

from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    # 1. Create an owner with a daily time budget of 60 minutes
    owner = Owner(name="Alex", available_time_minutes=60)

    # 2. Create at least two pets
    dog = Pet(name="Milo", species="dog")
    cat = Pet(name="Luna", species="cat")

    # 3. Add at least three tasks with different durations to the pets
    dog.add_task(Task(title="Morning Walk", duration_minutes=30, priority="high"))
    dog.add_task(Task(title="Brush Fur", duration_minutes=15, priority="low"))

    cat.add_task(Task(title="Give Medication", duration_minutes=10, priority="high"))
    cat.add_task(Task(title="Interactive Playtime", duration_minutes=20, priority="medium"))

    # Register pets with owner
    owner.add_pet(dog)
    owner.add_pet(cat)

    # 4. Schedule tasks using the Scheduler reading from the Owner
    scheduler = Scheduler()
    scheduler.schedule_for_owner(owner)

    # 5. Print today's schedule to the terminal
    print(scheduler.get_summary())


if __name__ == "__main__":
    main()
