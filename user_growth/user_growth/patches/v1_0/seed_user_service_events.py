from datetime import timedelta
import frappe
from frappe.utils import add_days, flt, today


SERVICES = ["标准版", "成长版", "企业版"]
REGIONS = ["华北", "华南", "华东", "西部"]
PLANS = ["免费", "基础", "专业", "企业"]


def execute():
    if frappe.db.exists("User Service Event", {"is_mock": 1}):
        return

    base_date = today()
    rows = []

    for month_index in range(12):
        anchor = add_days(base_date, -(month_index * 30))

        for offset in range(1, 9):
            rows.append(_build_row(month_index, offset, anchor, "开通"))

        for offset in range(1, 4):
            rows.append(_build_row(month_index, offset, anchor, "流失"))

    for row in reversed(rows):
        doc = frappe.get_doc({"doctype": "User Service Event", **row})
        doc.insert(ignore_permissions=True)


def _build_row(month_index, offset, anchor, event_type):
    event_date = add_days(anchor, -offset * 2)
    service_name = SERVICES[(month_index + offset) % len(SERVICES)]
    region = REGIONS[(month_index + offset) % len(REGIONS)]
    plan_tier = PLANS[(month_index + offset) % len(PLANS)]
    delta = 199 + (month_index * 5) + (offset * 10)
    if event_type == "流失":
        delta = -flt(delta / 2)

    return {
        "user_id": f"USER-{month_index:02d}-{offset:03d}-{event_type[:1]}",
        "event_type": event_type,
        "event_date": event_date,
        "service_name": service_name,
        "region": region,
        "plan_tier": plan_tier,
        "mrr_delta": delta,
        "is_mock": 1,
        "notes": "系统预置模拟数据"
    }