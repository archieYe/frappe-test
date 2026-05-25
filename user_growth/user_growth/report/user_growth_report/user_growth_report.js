frappe.query_reports["User Growth Report"] = {
  filters: [
    {
      fieldname: "from_date",
      label: "开始日期",
      fieldtype: "Date",
      reqd: 1,
      default: frappe.datetime.add_months(frappe.datetime.get_today(), -6)
    },
    {
      fieldname: "to_date",
      label: "结束日期",
      fieldtype: "Date",
      reqd: 1,
      default: frappe.datetime.get_today()
    },
    {
      fieldname: "service_name",
      label: "服务名称",
      fieldtype: "Select",
      options: "\n标准版\n成长版\n企业版"
    },
    {
      fieldname: "region",
      label: "区域",
      fieldtype: "Select",
      options: "\n华北\n华南\n华东\n西部"
    },
    {
      fieldname: "plan_tier",
      label: "套餐层级",
      fieldtype: "Select",
      options: "\n免费\n基础\n专业\n企业"
    }
  ]
};
