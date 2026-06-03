// Copyright (c) 2025, Nesscale Solutions Pvt Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('WB Task', {
	refresh(frm) {
		frm.trigger('add_action_buttons');
	},
	add_action_buttons(frm) {
		if (frm.is_new()) return;

		const current_user = frappe.session.user;
		const is_assignee = current_user === frm.doc.assign_to;
		const is_assigner = current_user === frm.doc.assign_from;
		const is_admin = current_user === 'Administrator';

		frappe.call({
			method: 'workboard.utils.get_workboard_settings',
			callback: (r) => {
				const settings = r.message || {};
				const admin_role = settings.workboard_admin_role;
				const has_admin_role = admin_role && frappe.user_roles.includes(admin_role);
				const only_assignee_can_complete = settings.only_assignee_can_complete;

				// Mark Done is the assignee's action on a Manual task that is still Open/Overdue
				if (frm.doc.task_type === 'Manual' && ['Open', 'Overdue'].includes(frm.doc.status)) {
					if (is_assignee || is_admin || has_admin_role) {
						frm.add_custom_button(__('Mark Done'), () => {
							frm.call({
								method: 'mark_done',
								doc: frm.doc,
								freeze: true,
								freeze_message: __('Marking as Done...'),
								callback: () => frm.reload_doc()
							});
						}).addClass('btn-primary');
					}
				}

				if (frm.doc.task_type === 'Manual' && frm.doc.status === 'Done') {
					// Settings decide whether the assignee or the assigner approves completion
					const can_mark_complete = only_assignee_can_complete
						? is_assignee || is_admin || has_admin_role
						: is_assigner || is_admin || has_admin_role;

					if (can_mark_complete) {
						frm.add_custom_button(__('Mark Completed'), () => {
							frm.call({
								method: 'mark_completed',
								doc: frm.doc,
								freeze: true,
								freeze_message: __('Marking as Completed...'),
								callback: () => frm.reload_doc()
							});
						}).addClass('btn-success');
					}
				} else if (frm.doc.task_type === 'Auto' && ['Open', 'Overdue'].includes(frm.doc.status)) {
					// Auto tasks complete directly, without the Done step
					frm.add_custom_button(__('Mark Completed'), () => {
						frm.call({
							method: 'mark_completed',
							doc: frm.doc,
							freeze: true,
							freeze_message: __('Marking as Completed...'),
							callback: () => frm.reload_doc()
						});
					}).addClass('btn-primary');
				}
			}
		});
	},
	checklist_template(frm) {
		frm.trigger('fetch_checklist');
	},
	fetch_checklist(frm) {
		frm.call({
			method: 'fetch_checklist',
			doc: frm.doc,
			freeze: true
		});
	}
});
