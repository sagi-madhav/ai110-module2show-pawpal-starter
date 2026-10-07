"""tests/test_pawpal.py

Unit tests for PawPal+ core classes.
"""

from pawpal_system import Pet, Task


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
