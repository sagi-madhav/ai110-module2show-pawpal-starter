# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Core user actions:
  1. Add and manage pet profiles by providing details like the pet's name and species.
  2. Create and customize care tasks, setting an estimated duration in minutes and a priority level (high, medium, or low).
  3. Generate a daily plan that fits within the owner's time constraints, showing a clear schedule and the reasoning behind each choice.

- Initial design and classes:
  - `Owner`: Holds owner details, available time for the day, and manages their list of pets.
  - `Pet`: Holds the pet's name and species, and keeps track of all tasks assigned to that pet.
  - `CareTask`: Represents a single activity (such as a walk or feeding) with its duration, priority level, and completion status.
  - `DailyScheduler`: Collects pending tasks, organizes them by priority to fit within available time, and records explanations for which tasks are scheduled or deferred.

**b. Design changes**

- Did your design change during implementation?
  Yes, while reviewing the initial class skeleton, we made a couple of adjustments to prevent confusion and bottlenecks:
  1. We added an optional `pet_name` attribute to `CareTask`. Originally, only `Pet` held the task list. But when `DailyScheduler` collects tasks from multiple pets into a single daily plan, having each task know which pet it belongs to makes the final schedule much clearer to the user.
  2. We noted that priority strings ('high', 'medium', 'low') should map to clear ranking values rather than relying on alphabetical order, ensuring top-priority items are always scheduled first.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- The scheduler considers total available time (in minutes), priority levels (high, medium, low), scheduled time slots ("HH:MM"), and task durations.
- High priority matters most because essential pet health and care tasks (like medication and core feeding) cannot be skipped. Within the same priority tier, shorter tasks are scheduled first to maximize the number of completed activities within the owner's available time.

**b. Tradeoffs**

- Tradeoff: The conflict detection algorithm checks for exact start-time matches (such as two tasks starting at 08:00) rather than calculating full overlapping duration intervals. Furthermore, when conflicts occur, the scheduler generates a warning message instead of crashing or automatically canceling a task.
- Why it is reasonable: Checking exact start times keeps the algorithm lightweight, performant, and simple to understand without requiring complex datetime interval math. Raising a visible warning rather than failing or dropping tasks gives owners flexibility, since an owner can often multitask (like feeding both pets together) or ask a family member for assistance.

---

## 3. AI Collaboration

**a. How you used AI**

- I used AI tools to brainstorm the initial class structure from the project requirements, convert our UML ideas into clean Python dataclasses, and set up boilerplate tests.
- Prompts that were specific and architectural were most helpful—for example, asking how the Scheduler should communicate with the Owner to gather tasks across multiple pets, and asking for a clean, human-readable terminal output format.

**b. Judgment and verification**

- During the skeleton phase, the initial design had tasks isolated inside pets without tracking which pet they belonged to once aggregated, and priority sorting was just using string values. I did not accept that as-is; instead, I ensured tasks retain their associated pet's name when added to a pet, and implemented explicit numeric priority rankings (high = 3, medium = 2, low = 1) so high-priority tasks always come first.
- I verified this by running `python main.py` with multi-pet scenarios to inspect the printed plan, and by executing automated unit tests with `pytest` to confirm task completion and pet task tracking work as expected.

---

## 4. Testing and Verification

**a. What you tested**

- Behaviors tested:
  1. Task completion state changes (`mark_complete`).
  2. Associating tasks with pets and verifying task count increases.
  3. Gathering all tasks across multiple pets via the owner.
  4. Chronological sorting by time strings, including tasks without a time.
  5. Filtering tasks by pet name and completion status.
  6. Recurring task scheduling for daily (+1 day) and weekly (+7 days) intervals using `timedelta`.
  7. Conflict detection when two tasks share the same time slot, and ensuring no false warnings occur for unique times.
  8. Time budget limits and handling empty task lists without crashing.
- Why these tests were important:
  They ensure that the scheduling engine behaves predictably, never crashes on unexpected or empty inputs, and reliably prioritizes pet well-being within the owner's daily constraints.

**b. Confidence**

- Confidence level: Very high (5/5 stars). All 11 automated unit tests run and pass cleanly in a fraction of a second, covering both happy paths and edge cases.
- Edge cases to test next:
  Given more time, I would test tasks that cross midnight, invalid time formats (like non-digit strings), negative task durations, and multi-day lookaheads.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
