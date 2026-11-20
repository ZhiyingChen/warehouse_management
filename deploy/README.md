# Server deployment

The application runs as one independent service and does not modify the existing applications or Caddy configuration.

- Directory: `/opt/warehouse_management_app`
- Service: `warehouse-app.service`
- Web and API port: `8090`
- API endpoint: `/api/run`

FastAPI serves the static frontend and optimization API from the same process. GitHub Pages can also call the API when its origin is listed in `ALLOWED_ORIGINS`.
