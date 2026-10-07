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

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
