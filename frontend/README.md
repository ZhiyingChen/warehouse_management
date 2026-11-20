# Warehouse Network Studio Frontend

这是仓储选址项目的独立静态前端，可部署到 GitHub Pages、Cloudflare Pages 或任意静态服务器。

## 本地预览

在项目根目录执行：

```powershell
python -m http.server 5173 --directory frontend
```

然后打开 `http://127.0.0.1:5173`。

## 连接后端

页面左下角点击 `API 未连接`，填写 FastAPI 服务根地址，例如：

```text
http://127.0.0.1:8000
```

前端会向 `{API地址}/api/run` 提交现有四张输入表。

后端部署到其他域名或端口时，需要在 FastAPI 中启用 CORS，并允许当前前端站点来源。

## GitHub Pages

将 `frontend` 目录作为静态站点构建产物发布即可。该前端没有 Node.js 运行依赖和构建步骤。
