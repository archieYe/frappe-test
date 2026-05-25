import frappe


@frappe.whitelist()
def get_kpis(from_date=None, to_date=None):
    conditions, values = _build_conditions(from_date, to_date)
    result = frappe.db.sql(
        f"""
        select
            sum(case when event_type = '开通' then 1 else 0 end) as activations,
            sum(case when event_type = '流失' then 1 else 0 end) as churns,
            sum(case when event_type = '开通' then 1 else -1 end) as net_growth
        from `tabUser Service Event`
        where docstatus < 2 {conditions}
        """,
        values=values,
        as_dict=True,
    )[0]
    return result


@frappe.whitelist()
def get_distribution(from_date=None, to_date=None):
    conditions, values = _build_conditions(from_date, to_date)
    rows = frappe.db.sql(
        f"""
        select region, count(*) as total
        from `tabUser Service Event`
        where docstatus < 2 {conditions}
        group by region
        order by total desc
        """,
        values=values,
        as_dict=True,
    )
    return {
        "labels": [r.region for r in rows],
        "values": [r.total for r in rows],
    }


@frappe.whitelist()
def get_trend(from_date=None, to_date=None):
    conditions, values = _build_conditions(from_date, to_date)
    rows = frappe.db.sql(
        f"""
        select
            date(event_date) as period,
            sum(case when event_type = '开通' then 1 else 0 end) as activations,
            sum(case when event_type = '流失' then 1 else 0 end) as churns,
            sum(case when event_type = '开通' then 1 else -1 end) as net_growth
        from `tabUser Service Event`
        where docstatus < 2 {conditions}
        group by date(event_date)
        order by period asc
        """,
        values=values,
        as_dict=True,
    )
    return {
        "labels": [str(r.period) for r in rows],
        "activations": [r.activations or 0 for r in rows],
        "churns": [r.churns or 0 for r in rows],
        "net_growth": [r.net_growth or 0 for r in rows],
    }


def _build_conditions(from_date=None, to_date=None):
    conditions = []
    values = {}

    if from_date:
        conditions.append("and event_date >= %(from_date)s")
        values["from_date"] = from_date
    if to_date:
        conditions.append("and event_date <= %(to_date)s")
        values["to_date"] = to_date

    return (" " + " ".join(conditions)) if conditions else "", values
