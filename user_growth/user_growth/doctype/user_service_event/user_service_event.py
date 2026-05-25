import frappe
from frappe.model.document import Document
from frappe.utils import flt


class UserServiceEvent(Document):
    def validate(self):
        if self.event_type == "开通" and flt(self.mrr_delta) < 0:
            frappe.throw("开通记录的 MRR 变动值不能为负数。")
        if self.event_type == "流失" and flt(self.mrr_delta) > 0:
            frappe.throw("流失记录的 MRR 变动值不能为正数。")