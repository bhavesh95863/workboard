# TaskHub
> Internal Work Management System for Frappe Framework

**TaskHub** is a lightweight, internal company task management app built on the Frappe Framework.  
It lets you create, assign, and track **manual**, **recurring**, and **event-based** tasks.

---

## **Features**
- **TH Task**  
  - Create manual tasks and assign them from one person to another (one-to-one assignment).  
  - Optional checklist support — tasks auto-complete when all checklist items are done.  
  - Simple statuses: **Open**, **Completed** (with timeliness tracking: On Time / Late).  

- **TH Task Rule**  
  - Define rules for recurring tasks (Daily, Weekly, Monthly, Yearly).  
  - Define event-based tasks triggered by specific document actions (e.g., on new User creation).  
  - Condition-based creation using Frappe’s safe_eval context.  

- **Workspace: TaskHub Dashboard**  
  - KPI Cards: Open Tasks, Due Today, Overdue, Completed Today.  
  - Lists: My Open Tasks, Due Today, Overdue, Completed (last 7 days).  
  - Charts: Tasks Created vs Completed (last 7 days).  
  - Shortcuts: Quick access to TH Task and TH Task Rule.  

---

## **Installation**

```bash
# Get the app
bench get-app task_hub

# Install on your site
bench --site yoursite install-app task_hub
```

---

## **Configuration**
1. **Create Task Rules**  
   - Go to **TH Task Rule** and define recurring or event-based rules.  
   - For recurring: set frequency and due days.  
   - For event-based: set “Based On” and reference doctype.  

2. **Access Workspace**  
   - Open **TaskHub Dashboard** from the desk to see KPIs, task lists, and charts.

---
