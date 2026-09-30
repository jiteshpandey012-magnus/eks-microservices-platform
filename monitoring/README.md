# Kubernetes Monitoring

## Components
- Prometheus: collects application and Kubernetes metrics.
- Grafana: visualizes metrics.
- Alertmanager: handles alert notifications.
- kube-state-metrics and Node Exporter: provide Kubernetes and node metrics.

## Installed Helm Release
- Release: monitoring
- Namespace: monitoring
- Chart: kube-prometheus-stack 91.8.2
- Application version: v0.94.1
- Prometheus retention: 24 hours
- Scrape interval: 30 seconds

## User Service Monitoring
The user-service-servicemonitor.yaml file configures scraping of the User Service.
- Target namespace: default
- Service label: app=user-service
- Service port name: http
- Metrics path: /metrics
- Scrape interval: 30 seconds

## Verify the Installation
```bash
helm list -n monitoring
kubectl get pods -n monitoring
kubectl get prometheus -n monitoring
kubectl get servicemonitor -n monitoring user-service
```

## Access Prometheus
```bash
kubectl port-forward -n monitoring service/monitoring-kube-prometheus-prometheus 9090:9090
```
Open http://localhost:9090 where the port-forward is accessible.

## Access Grafana
```bash
kubectl port-forward -n monitoring service/monitoring-grafana 3000:80
```
Open http://localhost:3000. For a remote cluster, use an SSH tunnel.

## Example PromQL
```promql
sum(rate(user_service_http_requests_total[5m]))
```
```promql
histogram_quantile(0.95, sum by (le) (rate(user_service_http_request_duration_seconds_bucket[5m])))
```

## Security and Storage Notes
- Never commit real Grafana passwords or credentials to Git.
- Review values.yaml against the installed Helm values before applying it; Grafana configuration differs between the local file and the inspected release.
- Grafana persistence is disabled in the inspected configuration.
- Review retention, backups, and resource limits before production use.
