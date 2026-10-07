"""pawpal_system.py

Core backend data models and scheduling logic skeleton for PawPal+.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class CareTask:
    """Represents a single pet care task."""

    title: str
    duration_minutes: int
    priority: str = "medium"  # 'high', 'medium', or 'low'
    is_completed: bool = False
    pet_name: Optional[str] = None

    def mark_complete(self) -> None:
        """Mark this task as finished."""
        pass

    def is_high_priority(self) -> bool:
        """Return True if this task is marked as high priority."""
        pass


@dataclass
class Pet:
    """Represents a pet belonging to an owner."""

    name: str
    species: str = "dog"
    tasks: List[CareTask] = field(default_factory=list)

    def add_task(self, task: CareTask) -> None:
        """Add a care task to this pet's task list."""
        pass

    def get_pending_tasks(self) -> List[CareTask]:
        """Return all tasks that are not yet marked as completed."""
        pass


@dataclass
class Owner:
    """Represents the pet owner and their daily availability."""

    name: str
    available_time_minutes: int = 60
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's care list."""
        pass

    def get_all_tasks(self) -> List[CareTask]:
        """Gather all tasks across every pet belonging to the owner."""
        pass


class DailyScheduler:
    """Builds a daily plan for pet care tasks within time constraints."""

    def __init__(self, time_limit_minutes: int = 60):
        self.time_limit_minutes = time_limit_minutes
        self.scheduled_tasks: List[CareTask] = []
        self.skipped_tasks: List[CareTask] = []
        self.reasoning: List[str] = []

    def generate_plan(self, tasks: List[CareTask], time_limit_minutes: Optional[int] = None) -> List[CareTask]:
        """Select and order tasks based on priority and available time."""
        pass

    def get_summary(self) -> str:
        """Return a readable text explanation of the scheduled plan."""
        pass
