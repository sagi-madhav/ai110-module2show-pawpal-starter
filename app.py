"""app.py

Streamlit application for PawPal+.
Connects UI inputs and session state to the core backend classes.
"""

import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.caption("A smart daily planner for pet care tasks and schedules.")

# Initialize the persistent Owner instance in session state if not present
if "owner" not in st.session_state:
    initial_owner = Owner(name="Jordan", available_time_minutes=60)
    initial_owner.add_pet(Pet(name="Mochi", species="dog"))
    st.session_state.owner = initial_owner

owner: Owner = st.session_state.owner

# Section 1: Owner and Pet Management
st.subheader("1. Owner & Pet Settings")
col_owner1, col_owner2 = st.columns(2)
with col_owner1:
    owner.name = st.text_input("Owner Name", value=owner.name)
with col_owner2:
    owner.available_time_minutes = int(
        st.number_input(
            "Available Time Budget (minutes)",
            min_value=5,
            max_value=480,
            value=owner.available_time_minutes,
            step=5,
        )
    )

with st.expander("Add New Pet", expanded=False):
    with st.form("add_pet_form", clear_on_submit=True):
        pet_col1, pet_col2 = st.columns(2)
        with pet_col1:
            new_pet_name = st.text_input("Pet Name")
        with pet_col2:
            new_pet_species = st.selectbox(
                "Species", ["dog", "cat", "bird", "rabbit", "other"]
            )
        submit_pet = st.form_submit_button("Add Pet")
        if submit_pet:
            if new_pet_name.strip():
                new_pet = Pet(name=new_pet_name.strip(), species=new_pet_species)
                owner.add_pet(new_pet)
                st.success(f"Added pet '{new_pet.name}' ({new_pet.species})!")
            else:
                st.error("Please provide a pet name.")

# Display current pets
if owner.pets:
    pets_display = ", ".join([f"{p.name} ({p.species})" for p in owner.pets])
    st.info(f"**Registered Pets:** {pets_display}")
else:
    st.warning("No pets registered. Please add a pet above.")

st.divider()

# Section 2: Task Creation
st.subheader("2. Care Tasks")

if owner.pets:
    pet_names = [p.name for p in owner.pets]
    with st.form("add_task_form", clear_on_submit=True):
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            task_title = st.text_input("Task Title", value="Morning walk")
        with col2:
            assigned_pet_name = st.selectbox("Pet", pet_names)
        with col3:
            duration = st.number_input(
                "Duration (min)", min_value=5, max_value=240, value=20, step=5
            )

        col4, col5 = st.columns(2)
        with col4:
            priority = st.selectbox("Priority", ["high", "medium", "low"], index=0)
        with col5:
            task_time = st.text_input("Scheduled Time (HH:MM, e.g. 08:00)", value="08:00")

        submit_task = st.form_submit_button("Add Task")
        if submit_task:
            if task_title.strip():
                new_task = Task(
                    title=task_title.strip(),
                    duration_minutes=int(duration),
                    priority=priority,
                    time=task_time.strip() if task_time.strip() else None,
                    pet_name=assigned_pet_name,
                )
                for p in owner.pets:
                    if p.name == assigned_pet_name:
                        p.add_task(new_task)
                        break
                st.success(f"Added '{new_task.title}' for {assigned_pet_name}!")
            else:
                st.error("Please enter a task title.")

# Display all tasks from all pets
all_tasks = owner.get_all_tasks()
if all_tasks:
    st.write("**Current Pending Tasks:**")
    task_rows = [
        {
            "Task": t.title,
            "Pet": t.pet_name,
            "Time": t.time or "Anytime",
            "Duration (min)": t.duration_minutes,
            "Priority": t.priority.capitalize(),
        }
        for t in all_tasks
    ]
    st.table(task_rows)
else:
    st.info("No pending tasks added yet. Use the form above to add one.")

st.divider()

# Section 3: Generate Daily Schedule
st.subheader("3. Daily Schedule")

if st.button("Generate Schedule", type="primary"):
    if not all_tasks:
        st.warning("No tasks found to schedule. Please add tasks first.")
    else:
        scheduler = Scheduler()
        scheduler.schedule_for_owner(owner)
        st.success("Schedule generated successfully!")
        st.text(scheduler.get_summary())
