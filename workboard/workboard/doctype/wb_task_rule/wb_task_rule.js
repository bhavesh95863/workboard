// Copyright (c) 2025, Nesscale Solutions Pvt Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('WB Task Rule', {
	setup_fieldname_select: function (frm) {
		// get the doctype to update fields
		if (!frm.doc.reference_doctype) {
			return;
		}

		frappe.model.with_doctype(frm.doc.reference_doctype, function () {
			let get_select_options = function (df, parent_field) {
				// Append parent_field name along with fieldname for child table fields
				let select_value = parent_field ? df.fieldname + ',' + parent_field : df.fieldname;

				return {
					value: select_value,
					label: df.fieldname + ' (' + __(df.label) + ')'
				};
			};
			let get_date_change_options = function() {
				let date_options = $.map(fields, function(d) {
					return d.fieldtype == 'Date' || d.fieldtype == 'Datetime'
						? get_select_options(d)
						: null;
				});
				// append creation and modified date to Date Change field
				return date_options.concat([
					{ value: 'creation', label: `creation (${__('Created On')})` },
					{ value: 'modified', label: `modified (${__('Last Modified Date')})` }
				]);
			};

			let fields = frappe.get_doc('DocType', frm.doc.reference_doctype).fields;
			let options = $.map(fields, function (d) {
				return frappe.model.no_value_type.includes(d.fieldtype)
					? null : get_select_options(d);
			});

			// set value changed options
			frm.set_df_property('value_changed', 'options', [''].concat(options));
			frm.set_df_property('reference_date', 'options', get_date_change_options());


		});
	},
	onload: function (frm) {
		frm.set_query('reference_doctype', function () {
			return {
				filters: {
					istable: 0,
                    issingle: 0
				}
			};
		});
	},
	refresh: function (frm) {
		frm.trigger('setup_fieldname_select')
	},
	reference_doctype: function (frm) {
		frm.trigger('setup_fieldname_select')
	}
});