# External Telemetry API v1 — Client Guide

NetX uses [stats.netx.as](https://stats.netx.as) as its cloud statistics platform. It collects telemetry from NetX routers and makes organization-specific metrics and logs available for monitoring and integration.

The platform is under active development. Additional router telemetry and API capabilities will become available over time.

This API provides read-only, organization-scoped access to metrics and logs. It is intended for server-to-server integrations. The organization is taken from the API key; clients never send an organization, account, project, or tenant ID.

## Documentation endpoints

| Resource | URL |
|---|---|
| Swagger UI | `/api/v1/docs` |
| This client guide | `/api/v1/client-guide.md` |
| OpenAPI 3.0 YAML | `/api/v1/openapi.yaml` |
| Capabilities and effective limits | `/api/v1/capabilities` |

The OpenAPI document can be imported into Swagger UI, Postman, Insomnia, or an OpenAPI client generator. The hosted Swagger UI supports live requests with the **Authorize** button and does not persist the API key.

## Authentication

Send the assigned key in the `X-API-Key` header:

```http
X-API-Key: sak_your_key
```

Keys are restricted to one or both read scopes:

- `metrics:read` permits metrics query and discovery operations.
- `logs:read` permits logs search, aggregation, and discovery operations.

Do not put API keys in URLs, application logs, source control, or browser storage. API keys expire; clients should surface `401 invalid_api_key` so an operator can rotate the key.

## Quick start

Set these variables for the examples:

```bash
export STATS_API_URL='https://stats.netx.as'
export STATS_API_KEY='sak_your_key'
```

Start by reading the capabilities visible to the key:

```bash
curl --fail-with-body --silent --show-error \
  "$STATS_API_URL/api/v1/capabilities" \
  -H "X-API-Key: $STATS_API_KEY" \
  -H 'Accept: application/json'
```

The response reports enabled providers, operations, effective limits, and the earliest externally available metrics timestamp:

```json
{
  "data": {
    "providers": [
      {
        "provider": "victoria_metrics",
        "operations": ["query", "query-range", "names", "labels", "label-values"],
        "data_available_from": "2026-07-13T00:00:00Z",
        "limits": {
          "range_days": 31,
          "series": 1000,
          "points_per_series": 11000,
          "total_points": 100000
        }
      }
    ]
  },
  "meta": {
    "request_id": "req_01JZ6FQ4CV2JYJYNJ9E3PG7A7P",
    "organization_id": 42,
    "source": "stats_api",
    "limits": {
      "global": {"request_body_bytes": 65536, "route_deadline_seconds": 20},
      "metrics": {"range_days": 31, "series": 1000, "total_points": 100000}
    },
    "truncated": false,
    "data_available_from": "2026-07-13T00:00:00Z"
  }
}
```

Clients should treat the returned capabilities and limits as authoritative for that deployment.

## Common request and response rules

- POST bodies must use `Content-Type: application/json`.
- Unknown request fields are rejected.
- Times use RFC3339, for example `2026-07-13T10:00:00Z`.
- Response timestamps are UTC RFC3339Nano strings.
- Successful responses are `{ "data": ..., "meta": ... }`.
- Errors are `{ "error": { "code", "message", "details", "request_id" } }`.
- Responses use `Cache-Control: no-store` and must not be cached.
- A request may cover at most 31 days by default.
- Streaming and bulk export are not available in v1.

The `meta.request_id` value should be included in support requests. `meta.organization_id` confirms the organization selected by the key. Clients must not expect or attempt to override it.

## Metrics

Metrics endpoints require `metrics:read`. Expressions use MetricsQL. The service adds the organization filter itself, and `organization_id` is reserved and removed from returned labels.

### Concrete example: get `pkts_down` for a prefix

The traffic metrics are stored with the labels `customer_id`, `shaper_id`, `grp`, and `prefix`. To get the downstream packet count for `192.168.1.1` at a specific time, select `pkts_down` with an exact `prefix` matcher:

```bash
curl --fail-with-body --silent --show-error \
  "$STATS_API_URL/api/v1/metrics/query" \
  -H "X-API-Key: $STATS_API_KEY" \
  -H 'Content-Type: application/json' \
  --data '{
    "expression": "pkts_down{prefix=\"192.168.1.1\"}",
    "time": "2026-07-13T11:00:00Z"
  }'
```

Example normalized result:

```json
{
  "data": {
    "result_type": "vector",
    "series": [
      {
        "labels": {
          "__name__": "pkts_down",
          "customer_id": "customer-42",
          "shaper_id": "edge-01",
          "grp": "default",
          "prefix": "192.168.1.1"
        },
        "samples": [
          {"timestamp": "2026-07-13T11:00:00Z", "value": "18432"}
        ]
      }
    ]
  },
  "meta": {
    "request_id": "req_01JZ6FQ4CV2JYJYNJ9E3PG7A7P",
    "organization_id": 42,
    "source": "victoria_metrics",
    "limits": {
      "series": 1000,
      "points_per_series": 11000,
      "total_points": 100000
    },
    "truncated": false,
    "data_available_from": "2026-07-13T00:00:00Z"
  }
}
```

The value is a string in the API response even though `pkts_down` is written to VictoriaMetrics as an integer. The API key supplies the organization scope, so do not add an `organization_id` matcher. The `prefix` value must exactly match the value written by the shaper; for example, use `192.168.1.1/32` instead if that is how the prefix is stored. An empty `series` array means no matching sample was found at that time.

Omit `time` to evaluate at the current server time.

### Range query

To retrieve the `pkts_down` samples for the same prefix over one hour:

```bash
curl --fail-with-body --silent --show-error \
  "$STATS_API_URL/api/v1/metrics/query-range" \
  -H "X-API-Key: $STATS_API_KEY" \
  -H 'Content-Type: application/json' \
  --data '{
    "expression": "pkts_down{prefix=\"192.168.1.1\"}",
    "start": "2026-07-13T10:00:00Z",
    "end": "2026-07-13T11:00:00Z",
    "step_seconds": 60
  }'
```

Example normalized result:

```json
{
  "data": {
    "result_type": "matrix",
    "series": [
      {
        "labels": {
          "__name__": "pkts_down",
          "customer_id": "customer-42",
          "shaper_id": "edge-01",
          "grp": "default",
          "prefix": "192.168.1.1"
        },
        "samples": [
          {"timestamp": "2026-07-13T10:00:00Z", "value": "17201"},
          {"timestamp": "2026-07-13T10:01:00Z", "value": "17248"}
        ]
      }
    ]
  },
  "meta": {
    "request_id": "req_01JZ6FQ4CV2JYJYNJ9E3PG7A7P",
    "organization_id": 42,
    "source": "victoria_metrics",
    "limits": {
      "series": 1000,
      "points_per_series": 11000,
      "total_points": 100000
    },
    "truncated": false,
    "data_available_from": "2026-07-13T00:00:00Z"
  }
}
```

Metric values are strings so `NaN`, `+Inf`, and `-Inf` remain lossless. Query results are never silently truncated. A query exceeding a series or point limit returns `422 result_too_large`; reduce its range, increase its step, or make the expression more selective.

The following MetricsQL inputs are rejected:

- Matchers on the reserved `organization_id` label.
- `@` modifiers.
- Lookbehind, offset, or subquery windows exceeding 31 days.
- Queries whose effective time is before `data_available_from`.

### Metrics discovery

| Operation | Endpoint | Required fields |
|---|---|---|
| Metric names | `/api/v1/metrics/names` | `start`, `end` |
| Label names | `/api/v1/metrics/labels` | `start`, `end`; optional `matchers` |
| Label values | `/api/v1/metrics/label-values` | `label`, `start`, `end`; optional `matchers` |

All discovery bodies accept an optional `limit`, normally from 1 to 1,000. Example:

```bash
curl --fail-with-body --silent --show-error \
  "$STATS_API_URL/api/v1/metrics/label-values" \
  -H "X-API-Key: $STATS_API_KEY" \
  -H 'Content-Type: application/json' \
  --data '{
    "label": "status",
    "matchers": ["{__name__=~\"http_.*\",job=\"api\"}"],
    "start": "2026-07-13T10:00:00Z",
    "end": "2026-07-13T11:00:00Z",
    "limit": 100
  }'
```

For bounded discovery results, check `meta.truncated`. If it is `true`, refine the matcher or time range; discovery has no offset pagination.

## Logs

Logs endpoints require `logs:read`. Queries use LogsQL. The server always enforces the time range and organization selected by the API key.

### Search and pagination

```bash
curl --fail-with-body --silent --show-error \
  "$STATS_API_URL/api/v1/logs/search" \
  -H "X-API-Key: $STATS_API_KEY" \
  -H 'Content-Type: application/json' \
  --data '{
    "query": "_stream:{service_name=\"payments\"} AND error",
    "start": "2026-07-13T10:00:00Z",
    "end": "2026-07-13T11:00:00Z",
    "limit": 200,
    "offset": 0
  }'
```

`data.records` preserves all log fields and upstream order. The response includes the applied offset and limit:

```json
{
  "data": {
    "records": [
      {
        "_time": "2026-07-13T10:15:30.123456789Z",
        "service_name": "payments",
        "level": "error",
        "message": "payment provider timed out"
      }
    ]
  },
  "meta": {
    "request_id": "req_01JZ6FQ4CV2JYJYNJ9E3PG7A7P",
    "organization_id": 42,
    "source": "victoria_logs",
    "limits": {"search_default": 200, "search_max": 1000, "search_offset_max": 10000},
    "pagination": {"offset": 0, "limit": 200},
    "truncated": false
  }
}
```

When a full page is returned, `meta.pagination.next_offset` is present. Request the next page using that value. Stop when `next_offset` is absent. The default maximum offset is 10,000; use a narrower time range or more selective LogsQL query for deeper retrieval.

### Log aggregation and discovery

| Operation | Endpoint | Optional controls |
|---|---|---|
| Histogram | `/api/v1/logs/histogram` | `step_seconds`, `group_by` |
| Facets | `/api/v1/logs/facets` | `limit_per_field` |
| Field names | `/api/v1/logs/fields` | `filter`, `limit` |
| Field values | `/api/v1/logs/field-values` | `filter`, `limit` |

Histogram example:

```bash
curl --fail-with-body --silent --show-error \
  "$STATS_API_URL/api/v1/logs/histogram" \
  -H "X-API-Key: $STATS_API_KEY" \
  -H 'Content-Type: application/json' \
  --data '{
    "query": "_stream:{service_name=\"payments\"}",
    "start": "2026-07-13T10:00:00Z",
    "end": "2026-07-13T11:00:00Z",
    "step_seconds": 300,
    "group_by": ["level"]
  }'
```

## Error handling

Example error:

```json
{
  "error": {
    "code": "range_not_available",
    "message": "The requested metrics range predates externally available data.",
    "details": {"data_available_from": "2026-07-13T00:00:00Z"},
    "request_id": "req_01JZ6FQ4CV2JYJYNJ9E3PG7A7P"
  }
}
```

Handle the HTTP status first and use `error.code` for more specific behavior:

| Status | Recommended client behavior |
|---:|---|
| `400` | Fix the request. Check JSON fields, timestamps, and query syntax. |
| `401` | Replace or rotate the API key; do not retry repeatedly. |
| `403` | Request the required read scope from an administrator. |
| `413` | Reduce the request body or query size. |
| `422` | Respect the metrics cutover or reduce the query result size. |
| `429` | Wait for the `Retry-After` duration, then retry with jitter. |
| `502` | Retry cautiously with exponential backoff; the provider response failed. |
| `503` | Retry cautiously; the service or provider is unavailable. |
| `504` | Reduce query cost or retry once with backoff. |

Do not retry `400`, `401`, `403`, `413`, or `422` without changing the request or credentials. All requests should have a client-side timeout slightly above the route deadline reported by `/capabilities`.

## JavaScript example

Use this from a server-side JavaScript runtime. API keys should not be shipped to public browser applications.

```javascript
const baseUrl = process.env.STATS_API_URL;
const apiKey = process.env.STATS_API_KEY;

async function statsRequest(path, body) {
  const response = await fetch(`${baseUrl}${path}`, {
    method: body === undefined ? "GET" : "POST",
    headers: {
      "Accept": "application/json",
      "X-API-Key": apiKey,
      ...(body === undefined ? {} : {"Content-Type": "application/json"})
    },
    body: body === undefined ? undefined : JSON.stringify(body),
    signal: AbortSignal.timeout(25_000),
    cache: "no-store"
  });

  const payload = await response.json();
  if (!response.ok) {
    const error = new Error(payload.error?.message ?? `HTTP ${response.status}`);
    error.status = response.status;
    error.code = payload.error?.code;
    error.requestId = payload.error?.request_id;
    error.retryAfter = response.headers.get("retry-after");
    throw error;
  }
  return payload;
}

const result = await statsRequest("/api/v1/metrics/query", {
  expression: "up",
  time: new Date().toISOString()
});
console.log(result.data.series);
```

## Python example

```python
import os
import requests

BASE_URL = os.environ["STATS_API_URL"]
API_KEY = os.environ["STATS_API_KEY"]

response = requests.post(
    f"{BASE_URL}/api/v1/logs/search",
    headers={"X-API-Key": API_KEY, "Accept": "application/json"},
    json={
        "query": '*',
        "start": "2026-07-13T10:00:00Z",
        "end": "2026-07-13T11:00:00Z",
        "limit": 200,
        "offset": 0,
    },
    timeout=25,
)

payload = response.json()
if not response.ok:
    error = payload.get("error", {})
    raise RuntimeError(
        f"stats API {response.status_code} {error.get('code')}: "
        f"{error.get('message')} request_id={error.get('request_id')}"
    )

for record in payload["data"]["records"]:
    print(record)
```

## Integration checklist

- Store the API key in a secret manager and rotate it before expiration.
- Call `/api/v1/capabilities` during startup or configuration validation.
- Keep request ranges and result sizes below the advertised limits.
- Set a client timeout and implement bounded retry with jitter only for `429` and transient `5xx` responses.
- Record `request_id`, status, and `error.code`, but never record the API key or full sensitive queries.
- Validate the integration with data belonging only to the assigned organization.
