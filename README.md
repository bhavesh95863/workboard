

<p align="center">
  <a href="https://github.com/bhavesh95863/workboard">
    <img width="200" height="200" alt="workboard" src="https://github.com/user-attachments/assets/49621c70-d619-48bb-9f0f-f8ab2b1c9af9" />
  </a>
</p>

<p align="center">
  Internal Work Management System for the Frappe Framework
  <br />
  <a href="https://github.com/bhavesh95863/workboard/issues">Issues</a>
  <a href="https://frappe.io">Community</a>
</p>

<p align="center">
  <a href="https://github.com/bhavesh95863/workboard/blob/master/LICENSE">
    <img alt="license" src="https://img.shields.io/badge/license-AGPLv3-blue">
  </a>
</p>

---

## Overview
**WorkBoard** is an internal company task management application built on the Frappe Framework. It provides a structured way to create, assign, and track manual, recurring, and event-based tasks with minimal complexity. Its design focuses on simplicity, efficiency, and real-time tracking to help teams execute work without unnecessary overhead.

---

## Key Features
Tasks in WorkBoard can be assigned from one user to another on a one-to-one basis. Each task may include an optional checklist, ensuring that completion is only possible once all checklist items are marked as done. Timeliness is automatically tracked, classifying completed tasks as either "On Time" or "Late."

For recurring work, **WB Task Rules** allow the creation of daily, weekly, monthly, or yearly tasks. Rules can also be configured to trigger based on system events—such as the creation of a new User—using conditional logic powered by Frappe’s `safe_eval`.

The included **WorkBoard Dashboard** offers at-a-glance visibility. Key performance indicators highlight open tasks, those due today, overdue items, and tasks completed within the day. Task lists and charts provide a historical view, such as a "Tasks Created vs Completed" trend over the past seven days. Quick access shortcuts allow navigation to both WB Task and WB Task Rule.

---

## Installation
```bash
# Get the app
bench get-app https://github.com/bhavesh95863/workboard

# Install on your site
bench --site yoursite install-app workboard
