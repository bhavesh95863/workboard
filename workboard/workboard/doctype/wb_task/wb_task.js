// Copyright (c) 2025, Nesscale Solutions Pvt Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('WB Task', {
  refresh(frm) {
    frm.trigger('add_completed_button');
  },
  add_completed_button(frm) {
    if (!frm.is_new() && ['Open', 'In Progress', 'Overdue'].includes(frm.doc.status)) {
      frm.add_custom_button(__('Mark Completed'), () => {
        frm.call({
          method: 'mark_completed',
          doc: frm.doc,
          freeze: true,
          callback: () => frm.reload_doc()
        });
      }).addClass('btn-primary');
    }
  },
  checklist_template(frm){
    frm.trigger('fetch_checklist');
  },
  fetch_checklist(frm) {
    frm.call({
      method: 'fetch_checklist',
      doc: frm.doc,
      freeze: true,
      callback: (r) => {
        
      }
    });
  }
});

