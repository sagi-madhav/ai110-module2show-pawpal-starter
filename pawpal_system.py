"""pawpal_system.py

Core backend logic for PawPal+.
Includes models for tasks, pets, owners, and scheduling across multiple pets.
Supports chronological sorting, filtering, recurring tasks, and conflict detection.
"""

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Dict, List, Optional


@dataclass
class Task:
    """Represents a single pet care activity."""

    title: str
    duration_minutes: int
    priority: str = "medium"  # 'high', 'medium', 'low'
    frequency: str = "once"  # 'once', 'daily', 'weekly'
    time: Optional[str] = None  # e.g., '08:00', '14:30' (HH:MM format)
    due_date: Optional[date] = None
    is_completed: bool = False
    pet_name: Optional[str] = None

    def mark_complete(self, current_date: Optional[date] = None) -> Optional["Task"]:
        """Mark completed and return the next recurring task instance if applicable."""
        self.is_completed = True
        today = current_date or self.due_date or date.today()
        freq = (self.frequency or "").lower()

        if freq == "daily":
            return Task(
                title=self.title,
                duration_minutes=self.duration_minutes,
                priority=self.priority,
                frequency=self.frequency,
                time=self.time,
                due_date=today + timedelta(days=1),
                is_completed=False,
                pet_name=self.pet_name,
            )
        elif freq == "weekly":
            return Task(
                title=self.title,
                duration_minutes=self.duration_minutes,
                priority=self.priority,
                frequency=self.frequency,
                time=self.time,
                due_date=today + timedelta(days=7),
                is_completed=False,
                pet_name=self.pet_name,
            )
        return None

    def is_high_priority(self) -> bool:
        """Check if this task has high priority."""
        return self.priority.lower() == "high"


# Alias to support previous skeletons and UML drafts
CareTask = Task


@dataclass
class Pet:
    """Stores pet details and an associated list of care tasks."""

    name: str
    species: str = "dog"
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet's task list."""
        if task.pet_name is None:
            task.pet_name = self.name
        self.tasks.append(task)

    def mark_task_complete(
        self, task: Task, current_date: Optional[date] = None
    ) -> Optional[Task]:
        """Mark task as complete and automatically enqueue next recurrence if recurring."""
        next_task = task.mark_complete(current_date=current_date)
        if next_task is not None:
            self.add_task(next_task)
        return next_task

    def get_pending_tasks(self) -> List[Task]:
        """Return tasks that have not yet been completed."""
        return [task for task in self.tasks if not task.is_completed]


@dataclass
class Owner:
    """Manages multiple pets and provides access to all their tasks."""

    name: str
    available_time_minutes: int = 60
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's care list."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Return all pending tasks from every pet managed by this owner."""
        all_tasks: List[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.get_pending_tasks())
        return all_tasks


class Scheduler:
    """The brain that organizes and schedules tasks across all of an owner's pets."""

    def __init__(self, time_limit_minutes: int = 60):
        self.time_limit_minutes = time_limit_minutes
        self.scheduled_tasks: List[Task] = []
        self.skipped_tasks: List[Task] = []
        self.reasoning: List[str] = []
        self.conflict_warnings: List[str] = []

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks chronologically by their HH:MM scheduled time string."""
        return sorted(tasks, key=lambda t: t.time if t.time else "99:99")

    def filter_tasks(
        self,
        tasks: List[Task],
        completed: Optional[bool] = None,
        pet_name: Optional[str] = None,
    ) -> List[Task]:
        """Filter tasks by completion status and/or pet name."""
        filtered = tasks
        if completed is not None:
            filtered = [t for t in filtered if t.is_completed == completed]
        if pet_name is not None:
            filtered = [
                t
                for t in filtered
                if t.pet_name and t.pet_name.lower() == pet_name.lower()
            ]
        return filtered

    def detect_conflicts(self, tasks: List[Task]) -> List[str]:
        """Detect if multiple tasks are scheduled at the exact same start time."""
        warnings: List[str] = []
        time_map: Dict[str, List[Task]] = {}

        for task in tasks:
            if task.time:
                time_map.setdefault(task.time, []).append(task)

        for slot, slot_tasks in time_map.items():
            if len(slot_tasks) > 1:
                names = [
                    f"'{t.title}' ({t.pet_name or 'Unassigned'})"
                    for t in slot_tasks
                ]
                warnings.append(
                    f"Time conflict at {slot}: {', '.join(names)} are scheduled at the same time."
                )

        return warnings

    def schedule_for_owner(
        self, owner: Owner, time_limit_minutes: Optional[int] = None
    ) -> List[Task]:
        """Retrieve all tasks from the owner and build today's schedule."""
        limit = (
            time_limit_minutes
            if time_limit_minutes is not None
            else owner.available_time_minutes
        )
        return self.generate_plan(owner.get_all_tasks(), limit)

    def generate_plan(
        self, tasks: List[Task], time_limit_minutes: Optional[int] = None
    ) -> List[Task]:
        """Organize tasks by priority and time constraints while detecting conflicts."""
        if time_limit_minutes is not None:
            self.time_limit_minutes = time_limit_minutes

        self.scheduled_tasks = []
        self.skipped_tasks = []
        self.reasoning = []
        self.conflict_warnings = self.detect_conflicts(tasks)

        priority_weights = {"high": 3, "medium": 2, "low": 1}

        # Sort: highest priority first, then shorter tasks first
        sorted_tasks = sorted(
            tasks,
            key=lambda t: (
                priority_weights.get(t.priority.lower(), 1),
                -t.duration_minutes,
            ),
            reverse=True,
        )

        time_used = 0
        for task in sorted_tasks:
            pet_tag = f" for {task.pet_name}" if task.pet_name else ""
            time_tag = f" at {task.time}" if task.time else ""
            if time_used + task.duration_minutes <= self.time_limit_minutes:
                self.scheduled_tasks.append(task)
                time_used += task.duration_minutes
                self.reasoning.append(
                    f"Scheduled '{task.title}'{pet_tag}{time_tag} ({task.duration_minutes} min, {task.priority} priority) - fits within time budget ({time_used}/{self.time_limit_minutes} min used)."
                )
            else:
                self.skipped_tasks.append(task)
                remaining = self.time_limit_minutes - time_used
                self.reasoning.append(
                    f"Skipped '{task.title}'{pet_tag}{time_tag} ({task.duration_minutes} min, {task.priority} priority) - needs {task.duration_minutes} min, but only {remaining} min remain."
                )

        return self.scheduled_tasks

    def get_summary(self) -> str:
        """Return a clean, readable text summary of the generated schedule."""
        lines = []
        lines.append("=== Today's Pet Care Schedule ===")
        lines.append(f"Available Time Budget: {self.time_limit_minutes} minutes")
        total_scheduled = sum(t.duration_minutes for t in self.scheduled_tasks)
        lines.append(f"Total Scheduled Time: {total_scheduled} minutes")
        lines.append("")

        if self.conflict_warnings:
            lines.append("Warnings & Detected Conflicts:")
            for w in self.conflict_warnings:
                lines.append(f"  [!] {w}")
            lines.append("")

        if self.scheduled_tasks:
            lines.append("Scheduled Tasks:")
            for idx, task in enumerate(self.scheduled_tasks, 1):
                pet_tag = f" ({task.pet_name})" if task.pet_name else ""
                time_tag = f" at {task.time}" if task.time else ""
                lines.append(
                    f"  {idx}. {task.title}{pet_tag}{time_tag} - {task.duration_minutes} mins [{task.priority.capitalize()} priority]"
                )
        else:
            lines.append("Scheduled Tasks: None")

        if self.skipped_tasks:
            lines.append("")
            lines.append("Skipped Tasks (Exceeded Time Budget):")
            for idx, task in enumerate(self.skipped_tasks, 1):
                pet_tag = f" ({task.pet_name})" if task.pet_name else ""
                time_tag = f" at {task.time}" if task.time else ""
                lines.append(
                    f"  {idx}. {task.title}{pet_tag}{time_tag} - {task.duration_minutes} mins [{task.priority.capitalize()} priority]"
                )

        lines.append("")
        lines.append("Why This Plan Was Chosen:")
        for note in self.reasoning:
            lines.append(f"  - {note}")

        return "\n".join(lines)


# Alias to support previous skeletons and UML drafts
DailyScheduler = Scheduler
