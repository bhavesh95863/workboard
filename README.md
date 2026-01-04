<p align="center">
  <a href="https://github.com/bhavesh95863/workboard">
    <img width="200" height="200" alt="WorkBoard" src="https://github.com/user-attachments/assets/49621c70-d619-48bb-9f0f-f8ab2b1c9af9" />
  </a>
</p>

<p align="center">
  <strong>WorkBoard</strong> – Internal Work Management for the Frappe Framework  
  <br />
  <a href="https://github.com/bhavesh95863/workboard/issues">Report Issues</a>
  ·
  <a href="https://frappe.io">Frappe Community</a>
</p>

<p align="center">
  <a href="https://github.com/bhavesh95863/workboard/blob/master/LICENSE">
    <img alt="License" src="https://img.shields.io/badge/license-AGPLv3-blue">
  </a>
</p>

---

## Overview

**WorkBoard** is an internal task management application built on the **Frappe Framework**.  
It provides a structured way to create, assign, and track tasks without unnecessary complexity.  
WorkBoard is designed to support both routine and event-based work, making it suitable for day-to-day operations and process automation.

---
You can refer to the following [YouTube video](https://youtu.be/_GOTp1-YgYY?si=b1uWGAWhmISpVVgh) for the quick tour of the features.

## Features

### Task Management
- **Direct Task Assignment** – Assign tasks from one user to another with clear ownership.
- **Time-Based Tasks** – Set time limits in minutes for tasks that need to be completed within hours, not days.
- **Two-Step Approval Workflow** – Tasks can be marked as "Done" by the assignee and then "Completed" by the assigner for quality control.
- **Optional Checklists** – Tasks can include checklists, ensuring they are only marked complete once all items are done.
- **Timeliness Tracking** – Automatically classify tasks as "On Time" or "Late" based on due dates or time limits.

### Automation & Rules
- **Recurring Task Rules** – Create recurring tasks with multiple frequencies:
  - Daily
  - Weekly
  - Fortnightly (bi-weekly - runs on weeks 1 and 3 of each month)
  - Monthly
  - Quarterly (runs in January, April, July, and October)
  - Yearly
- **Event-Triggered Tasks** – Generate tasks automatically based on system events using `safe_eval` conditions.
- **Automatic Administrator Assignment** – Recurring and event-based tasks automatically assign from "Administrator" for system-generated tasks.

### Permissions & Settings
- **WorkBoard Settings** – Global configuration for task completion permissions:
  - Control whether only assignees can mark tasks complete
  - Define a Workboard Admin Role that can bypass all restrictions
- **Flexible Permissions** – Assigners can optionally mark tasks complete based on settings.

### Dashboard & Insights
- **Personalized Dashboard** – Each user sees only their own tasks:
  - **My Open Tasks** – Count of tasks assigned to you that are still open
  - **My Overdue Tasks** – Tasks past their due date
  - **My Tasks Due Today** – Tasks due today
  - **My Today's Tasks** – Tasks created today
  - **My Completed Today** – Tasks you completed today
  - **Tasks Awaiting My Approval** – Manual tasks marked "Done" by assignees waiting for your approval
- **Historical Trends** – View "Tasks Created vs Completed" chart over time.
- **Quick Lists** – Direct access to:
  - Open Tasks assigned to you
  - Overdue Tasks assigned to you
  - Tasks Awaiting Approval (tasks marked "Done" by your team members)

---

## Screenshot

### WorkBoard Dashboard
<img width="1463" height="1100" alt="WorkBoard Dashboard Screenshot" src="https://github.com/user-attachments/assets/cf566868-ab17-4240-b860-25f07d891140" />

---

## Installation

```bash
# Get the app
bench get-app https://github.com/bhavesh95863/workboard

# Install on your site
bench --site yoursite install-app workboard

---

## Configuration

### WorkBoard Settings
Navigate to **WorkBoard Settings** to configure global task management behavior:

1. **Only Assignee Can Complete** – When enabled, only the person assigned to a task can mark it complete. When disabled, the assigner can also mark tasks complete.
2. **Workboard Admin Role** – Select a role (e.g., "Workboard Admin") that can bypass all completion restrictions and manage any task.

### Creating a Workboard Admin
1. Create a new role: **Workboard Admin**
2. Set this role in WorkBoard Settings
3. Assign this role to users who need full task management access

---

## Usage

### Creating Manual Tasks
1. Go to **WB Task** from the WorkBoard workspace
2. Fill in:
   - **Assign To** – User who will complete the task
   - **Assign From** – User assigning the task (defaults to you)
   - **Title** & **Description**
   - **Due Date** – When the task should be completed
   - **Depends on Time** (optional) – Enable for time-sensitive tasks:
     - Set **Time Limit in Minutes** for tasks due within hours
     - System calculates **End Datetime** automatically
   - **Checklist** (optional) – Add checklist items for multi-step tasks
3. Save to create the task

### Two-Step Approval Workflow
For tasks requiring quality control:

1. **Assignee** completes the work and clicks **Mark Done**
2. **Assigner** receives notification via "Tasks Awaiting My Approval"
3. **Assigner** reviews the work and clicks **Mark Completed**

*Note: This workflow applies to manual tasks. Configure in WorkBoard Settings.*

### Creating Recurring Tasks
1. Go to **WB Task Rule** from the WorkBoard workspace
2. Set:
   - **Task Type** = Recurring
   - **Frequency** – Daily, Weekly, Fortnightly, Monthly, Quarterly, or Yearly
   - **Title Template** – Use `{date}` placeholder for dynamic dates
   - **Assign To** – User who will receive the recurring tasks
   - **Depends on Time** (optional) – For recurring tasks with hourly deadlines
3. Enable the rule – Tasks will be created automatically by the scheduler

### Creating Event-Based Tasks
1. Go to **WB Task Rule** from the WorkBoard workspace
2. Set:
   - **Task Type** = Event
   - **Document Type** – DocType to monitor (e.g., "Sales Order")
   - **Event** – When to trigger (After Insert, On Update, etc.)
   - **Condition** – Python expression using `safe_eval` (e.g., `doc.status == "Pending"`)
   - **Offset Days** (optional) – Create task X days after the event
3. Enable the rule – Tasks will be created when events occur

### Dashboard Usage
Your personalized dashboard shows:
- **Number Cards** – Quick counts of your tasks by status
- **Tasks Awaiting My Approval** – Click to review and complete tasks marked "Done"
- **Quick Lists** – Direct access to open and overdue tasks
- **Chart** – Historical view of task creation vs completion trends

---

## License

This app is licensed under AGPLv3.
