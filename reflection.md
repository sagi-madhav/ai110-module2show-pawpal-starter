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

- Most effective AI features: Using the assistant to rapidly convert UML concepts into clean Python dataclasses, implement algorithmic methods (like sorting and filtering), and draft comprehensive unit test suites.
- Helpful prompts: Prompts focused on system structure—such as asking how the Scheduler should retrieve tasks across multiple pets through the Owner, and asking for a clean, human-readable terminal schedule format.
- Phased organization: Separating the project into distinct phases (UML architecture, backend implementation, smarter algorithms, automated testing, and UI integration) kept the work modular and ensured each component was fully verified before moving forward.

**b. Judgment and verification**

- Modified / rejected suggestions: During conflict detection, an overly complex interval math algorithm was considered. I chose a simpler, lightweight check on start times that issues non-blocking warnings instead of crashing. Additionally, I modified the initial task skeleton to explicitly store the pet's name on each task so schedules remain clear when multiple pets are involved.
- Verification: I verified all logic through hands-on testing in `main.py` and a suite of 11 passing `pytest` unit tests.
- Being the lead architect: Collaborating with AI highlighted that the developer must define the design boundaries and requirements. While AI excels at generating syntax and boilerplate quickly, the human architect must guide the system decisions and verify correctness.

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

- I am most satisfied with how cleanly the multi-pet aggregation works. Having the `Owner` manage multiple `Pet` objects and pass them seamlessly into the `Scheduler` created a system that feels natural and scalable. The automated test suite gave immediate confidence that every feature worked as expected.

**b. What you would improve**

- In a future iteration, I would add full time-slot interval arithmetic (detecting when an 8:00 AM 45-minute task overlaps with an 8:30 AM task), add task editing and deletion in the Streamlit UI, and support a multi-day weekly calendar view.

**c. Key takeaway**

- Designing the system architecture first—mapping out classes, attributes, and responsibilities—makes implementation and AI collaboration dramatically smoother. When you know exactly what each class should do, writing, testing, and debugging become straightforward.
