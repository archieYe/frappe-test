# 用户增长 App 部署与使用说明（中文）

## 1. 交付内容
本次交付的 Frappe 自定义 App 名称：`user_growth`，包含：

1. Doctype：`User Service Event`（用户服务开通/流失数据）
2. Report：`User Growth Report`（增长与流失统计报表）
3. Page：`user-growth-dashboard`（用户增长大屏）

## 2. 本地代码目录（已同步）
- `user_growth/pyproject.toml`
- `user_growth/user_growth/hooks.py`
- `user_growth/user_growth/modules.txt`
- `user_growth/user_growth/doctype/user_service_event/*`
- `user_growth/user_growth/patches/v1_0/seed_user_service_events.py`
- `user_growth/user_growth/report/user_growth_report/*`
- `user_growth/user_growth/page/user_growth_dashboard/*`

## 3. 服务器部署关键步骤（已验证）
以下是本次实际可用流程（基于 `dev2.local`）：

1. 将 app 放入 bench：
   - `cp -r ~/frappe/user_growth ~/frappe/frappe-bench/apps/`
2. 安装 Python editable 包：
   - `cd ~/frappe/frappe-bench`
   - `./env/bin/pip install -e apps/user_growth`
3. 确保 `sites/apps.txt` 内容正确（两行）：
   - `frappe`
   - `user_growth`
4. 安装 app 并迁移：
   - `bench --site dev2.local install-app user_growth`
   - `bench --site dev2.local migrate`
5. 指定默认站点并启动：
   - `bench use dev2.local`
   - `bench start`

## 4. 访问与登录
- 访问地址：`http://10.1.1.11:8000`
- 管理员账号：`Administrator`
- 管理员密码：建站时设置值（若忘记可用 `bench --site dev2.local set-admin-password <new_password>` 重置）

## 5. 功能验收入口
- Doctype：`/app/user-service-event`
- Report：`/app/query-report/User%20Growth%20Report`
- Page：`/app/user-growth-dashboard`

## 6. 常见问题与处理

### 6.1 `No module named 'frappeuser_growth'`
原因：`sites/apps.txt` 被写坏（`frappe` 与 `user_growth` 粘成一行）。
处理：
- 重写 `sites/apps.txt` 为两行：
  - `frappe`
  - `user_growth`

### 6.2 `No module named 'user_growth.user_growth'` 或 page 方法路径找不到
原因：模块路径/目录层级与方法字符串不一致。
处理：
- 保持 page JS 中方法路径与当前目录结构一致；
- 变更后执行：
  - `bench --site dev2.local clear-cache`
  - `bench --site dev2.local clear-website-cache`
  - `bench build --force`
  - 重启 `bench start`

### 6.3 `Address already in use`（11000/13000）
原因：旧 bench 进程未退出。
处理：
- 先清理旧进程再启动：
  - `pkill -f "redis-server.*11000" || true`
  - `pkill -f "redis-server.*13000" || true`
  - `pkill -f "frappe-bench" || true`
  - `bench start`

### 6.4 浏览器能打开但报旧方法路径
原因：前端缓存/旧构建。
处理：
- `bench build --force` 后使用无痕窗口或 `Ctrl+F5` 强刷。

## 7. 安全建议（上线前）
- 修改弱密码（数据库用户、Administrator）
- 最小权限化数据库账号
- 使用反向代理与 HTTPS
- 生产环境不要直接用 `bench start`
