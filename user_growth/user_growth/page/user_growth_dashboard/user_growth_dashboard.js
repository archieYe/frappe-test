frappe.pages["user-growth-dashboard"].on_page_load = function(wrapper) {
  const page = frappe.ui.make_app_page({
    parent: wrapper,
    title: "用户增长大屏",
    single_column: true
  });

  const $body = $(frappe.render_template("user_growth_dashboard", {}));
  $(page.body).append($body);

  const state = {
    from_date: frappe.datetime.add_months(frappe.datetime.get_today(), -6),
    to_date: frappe.datetime.get_today()
  };

  const refreshAll = () => {
    renderKpi(state);
    renderDistribution(state);
    renderTrend(state);
  };

  refreshAll();
  setInterval(refreshAll, 60000);
};

function renderKpi(state) {
  frappe.call({
    method: "user_growth.user_growth.page.user_growth_dashboard.user_growth_dashboard.get_kpis",
    args: state,
    callback: (r) => {
      const d = r.message || {};
      const cards = [
        ["开通数", d.activations || 0, "#22c55e"],
        ["流失数", d.churns || 0, "#ef4444"],
        ["净增长", d.net_growth || 0, "#3b82f6"]
      ];
      const html = cards.map(([label, value, color]) => `
        <div style="flex: 1; background: #fff; border-radius: 8px; padding: 14px; border-left: 4px solid ${color};">
          <div style="font-size: 13px; color: #6b7280;">${label}</div>
          <div style="font-size: 28px; font-weight: 700; margin-top: 6px;">${value}</div>
        </div>
      `).join("");
      $("#ugd-kpi").html(html);
    }
  });
}

function renderDistribution(state) {
  frappe.call({
    method: "user_growth.user_growth.page.user_growth_dashboard.user_growth_dashboard.get_distribution",
    args: state,
    callback: (r) => {
      const data = r.message || { labels: [], values: [] };
      $("#ugd-distribution").empty();
      new frappe.Chart("#ugd-distribution", {
        title: "区域用户分布",
        data: {
          labels: data.labels,
          datasets: [{ values: data.values }]
        },
        type: "donut",
        height: 320,
        colors: ["#60a5fa", "#34d399", "#fbbf24", "#f87171"]
      });
    }
  });
}

function renderTrend(state) {
  frappe.call({
    method: "user_growth.user_growth.page.user_growth_dashboard.user_growth_dashboard.get_trend",
    args: state,
    callback: (r) => {
      const data = r.message || { labels: [], activations: [], churns: [], net_growth: [] };
      $("#ugd-trend").empty();
      new frappe.Chart("#ugd-trend", {
        title: "开通与流失趋势",
        data: {
          labels: data.labels,
          datasets: [
            { name: "开通数", values: data.activations, chartType: "bar" },
            { name: "流失数", values: data.churns, chartType: "bar" },
            { name: "净增长", values: data.net_growth, chartType: "line" }
          ]
        },
        type: "axis-mixed",
        height: 320,
        colors: ["#22c55e", "#ef4444", "#3b82f6"]
      });
    }
  });
}
