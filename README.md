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

## Features

- **Direct Task Assignment** – Assign tasks from one user to another.
- **Optional Checklists** – Tasks can include checklists, ensuring they are only marked complete once all items are done.
- **Timeliness Tracking** – Automatically classify tasks as "On Time" or "Late".
- **Recurring Task Rules** – Create daily, weekly, monthly, or yearly recurring tasks.
- **Event-Triggered Tasks** – Generate tasks automatically based on system events using `safe_eval` conditions.
- **Dashboard Insights** – View open, due today, overdue, and completed tasks, along with historical trends such as "Tasks Created vs Completed".
- **Quick Access** – Navigate directly to WB Task and WB Task Rule from the dashboard.

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
