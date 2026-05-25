import frappe


def execute(filters=None):
    filters = filters or {}
    conditions, values = _build_conditions(filters)

    rows = frappe.db.sql(
        f"""
        select
            date(event_date) as period,
            sum(case when event_type = '开通' then 1 else 0 end) as activations,
            sum(case when event_type = '流失' then 1 else 0 end) as churns,
            sum(case when event_type = '开通' then 1 else -1 end) as net_growth,
            sum(mrr_delta) as mrr_delta
        from `tabUser Service Event`
        where docstatus < 2 {conditions}
        group by date(event_date)
        order by period asc
        """,
        values=values,
        as_dict=True,
    )

    columns = [
        {"label": "日期", "fieldname": "period", "fieldtype": "Date", "width": 110},
        {"label": "开通数", "fieldname": "activations", "fieldtype": "Int", "width": 110},
        {"label": "流失数", "fieldname": "churns", "fieldtype": "Int", "width": 100},
        {"label": "净增长", "fieldname": "net_growth", "fieldtype": "Int", "width": 120},
        {"label": "MRR变动", "fieldname": "mrr_delta", "fieldtype": "Currency", "width": 120},
    ]

    total_activations = sum(d.activations or 0 for d in rows)
    total_churns = sum(d.churns or 0 for d in rows)
    total_net = sum(d.net_growth or 0 for d in rows)

    chart = {
        "data": {
            "labels": [str(d.period) for d in rows],
            "datasets": [
                {"name": "开通数", "values": [d.activations or 0 for d in rows]},
                {"name": "流失数", "values": [d.churns or 0 for d in rows]},
                {"name": "净增长", "values": [d.net_growth or 0 for d in rows]},
            ],
        },
        "type": "axis-mixed",
        "axisOptions": {"xIsSeries": 1},
        "colors": ["#22c55e", "#ef4444", "#3b82f6"],
    }

    report_summary = [
        {"value": total_activations, "label": "累计开通", "indicator": "Green"},
        {"value": total_churns, "label": "累计流失", "indicator": "Red"},
        {"value": total_net, "label": "净增长", "indicator": "Blue"},
    ]

    return columns, rows, None, chart, report_summary


def _build_conditions(filters):
    conditions = []
    values = {}

    if filters.get("from_date"):
        conditions.append("and event_date >= %(from_date)s")
        values["from_date"] = filters.get("from_date")

    if filters.get("to_date"):
        conditions.append("and event_date <= %(to_date)s")
        values["to_date"] = filters.get("to_date")

    if filters.get("service_name"):
        conditions.append("and service_name = %(service_name)s")
        values["service_name"] = filters.get("service_name")

    if filters.get("region"):
        conditions.append("and region = %(region)s")
        values["region"] = filters.get("region")

    if filters.get("plan_tier"):
        conditions.append("and plan_tier = %(plan_tier)s")
        values["plan_tier"] = filters.get("plan_tier")

    return " " + " ".join(conditions) if conditions else "", values
