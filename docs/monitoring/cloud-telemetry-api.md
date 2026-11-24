# External Telemetry API v1 — Client Guide

NetX uses [stats.netx.as](https://stats.netx.as) as its cloud statistics platform. It collects telemetry from NetX routers, including per-prefix traffic counters from the shapers, and makes organization-specific traffic statistics, metrics and logs available for monitoring, reporting and integration.

The platform is under active development. Additional router telemetry and API capabilities will become available over time.

This API provides read-only, organization-scoped access to metrics, logs and per-prefix traffic. It is intended for server-to-server integrations. The organization is taken from the API key; clients never send an organization, account, project, or tenant ID.

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

Keys are restricted to one or more of these read scopes:

- `metrics:read` permits metrics query and discovery operations.
- `logs:read` permits logs search, aggregation, and discovery operations.
- `traffic:read` permits the curated traffic endpoints (`/api/v1/traffic/*`) only. Those endpoints also accept `metrics:read`. A traffic-only key can call `/api/v1/capabilities` (it sees only the `traffic` provider) but gets `403 insufficient_scope` from raw metrics and logs endpoints.

Do not put API keys in URLs, application logs, source control, or browser storage. Keys may be configured with or without expiration; clients should surface `401 invalid_api_key` so an operator can replace or rotate the key.

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

## Traffic

The traffic API answers the questions most integrations actually have, without MetricsQL: which prefixes does my organization have, how much traffic is each one doing right now, what did it look like over the last day, and how many bytes did it move this month. It is served under `/api/v1/traffic` and requires the `traffic:read` scope. A key with `metrics:read` also works, so existing keys keep working. `/api/v1/capabilities` lists a `traffic` provider for keys that can use it, with the effective limits.

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/v1/traffic/prefixes` | `GET` | List the organization's prefixes. |
| `/api/v1/traffic/rates` | `POST` | Current bits/s and packets/s, per prefix. |
| `/api/v1/traffic/series` | `POST` | Rate time series for graphs. |
| `/api/v1/traffic/totals` | `POST` | Bytes and packets over a month or period. |

Data rows never contain customer, shaper, group or organization identifiers, and never expose metric names or labels. (`meta.organization_id` is your own organization, as in every API response.)

### Concepts

**What the numbers measure.** Every prefix you have configured for shaping gets its own traffic class on the shaper. Each class counts the bytes and packets it forwards. Most prefixes are single subscriber addresses (`/32`); business customers and IPv6 delegations are larger networks (for example `/24` or `/56`).
- **Collection:** the shaper reads these counters every 60 seconds and sends them to the statistics service.
- **Timestamps:** each sample is timestamped with the moment it was read on the shaper, not when it arrived.
- **Hardware offload:** traffic that the shaper forwarded through hardware offload is included in the byte and packet numbers, so they show the prefix's full traffic.
- **Counter resets:** counters reset when the shaper rebuilds its classes, for example after a configuration change. The API accounts for resets, so rates and totals stay correct across them.

**Directions.** `down` is traffic toward the customer prefix; `up` is traffic from it. Every response has both, for bits (`bits_per_second_up`, `bits_per_second_down`, `bytes_up`, `bytes_down`) and for packets (`packets_per_second_up`, `packets_per_second_down`, `packets_up`, `packets_down`).

**Prefix forms.** A prefix is a single address or a CIDR network. `192.0.2.1` is the same as `192.0.2.1/32`. IPv6 is canonicalized (`2001:DB8:0:0::/48` becomes `2001:db8::/48`), and the canonical form is what responses return. Matching is exact: `192.0.2.0/24` selects only the prefix stored as `/24` and does not include the `/32`s inside it. Use `GET /api/v1/traffic/prefixes` to see exactly which prefixes exist. Selecting a prefix the organization does not have fails the whole request with `404 unknown_prefix` and the unmatched strings in `error.details.prefixes`.

**Missing values are `null`.** A prefix that exists but had no sample in the window is returned with `null` rates or totals, not zero. Treat `null` as "no data", and `0` as "measured, no traffic". Rates are JSON numbers; totals are integers.

**Double counting.** Traffic is summed across devices. Traffic that crosses more than one device in your organization is counted once per device, so the sum of all prefixes, or a `group_by: "none"` total, can exceed the traffic that actually entered your network.

**Rates and windows.** A rate is the average over a window. `window_seconds` defaults to 300 and must be between the server floor (default 120, see `limits.traffic.rate_window_floor_seconds` in `/capabilities`) and 3600. In `/series`, each sample is the average over one step. Because counters are read once a minute, a window always covers at least two readings; short bursts inside a window are averaged out. A 300-second rate is what most monitoring tools call "5-minute average throughput".

**Units.** `bits_per_second_*` is bits, not bytes: divide by 1,000,000 for Mbit/s. `bytes_*` totals are bytes: divide by 1,000,000,000 for GB (decimal, as ISPs usually report) or by 1,073,741,824 for GiB.

**Drops, shaping limits and contract numbers.** The traffic API reports forwarded traffic only. Per-prefix packet drops, the configured download and upload limits, and the contract number (`service_id`) behind each prefix are available as raw metrics with a `metrics:read` key; see [Metric catalog](#metric-catalog) and [MetricsQL recipes](#metricsql-recipes).

**Time.** In `/rates` a `time`, and in `/series` an `end`, more than one minute in the future is rejected with `400 invalid_request`. `/totals` is different: a future `end` is clamped to now and the period is reported with `period.complete: false`, but a period that starts in the future (a future `month` or `start`) is rejected with `400 invalid_request`. Data is only available from `meta.data_available_from`; earlier times fail with `422 range_not_available`.

### List prefixes

```bash
curl --fail-with-body --silent --show-error \
  "$STATS_API_URL/api/v1/traffic/prefixes?page_size=1000" \
  -H "X-API-Key: $STATS_API_KEY"
```

```json
{
  "data": {
    "prefixes": [
      {"prefix": "192.0.2.0/24", "ip_version": 4},
      {"prefix": "198.51.100.17/32", "ip_version": 4},
      {"prefix": "198.51.100.18/32", "ip_version": 4},
      {"prefix": "198.51.100.19/32", "ip_version": 4},
      {"prefix": "2001:db8:1200::/56", "ip_version": 6}
    ]
  },
  "meta": {
    "request_id": "req_01JZ6FQ4CV2JYJYNJ9E3PG7A7P",
    "organization_id": 42,
    "source": "victoria_metrics",
    "pagination": {"next_cursor": null, "page_size": 1000},
    "truncated": false,
    "data_available_from": "2026-07-13T00:00:00Z"
  }
}
```

In this example `192.0.2.0/24` is a business customer's network, the `/32`s are individual subscribers, and `2001:db8:1200::/56` is a subscriber's IPv6 delegation. Prefixes are sorted: IPv4 before IPv6, then by address, then by length. `page_size` defaults to 1000 and may be up to 5000. When `meta.pagination.next_cursor` is not `null`, pass it back as `?cursor=...` to get the next page. `meta.truncated` is `true` only if the organization has more prefixes than the server indexes.

### Rates for selected prefixes

```bash
curl --fail-with-body --silent --show-error \
  "$STATS_API_URL/api/v1/traffic/rates" \
  -H "X-API-Key: $STATS_API_KEY" \
  -H 'Content-Type: application/json' \
  --data '{
    "prefixes": ["192.0.2.0/24", "198.51.100.17", "198.51.100.19"],
    "window_seconds": 300
  }'
```

```json
{
  "data": {
    "rates": [
      {
        "prefix": "192.0.2.0/24",
        "bits_per_second_up": 41250000.5,
        "bits_per_second_down": 312400000,
        "packets_per_second_up": 9850.2,
        "packets_per_second_down": 27310.8
      },
      {
        "prefix": "198.51.100.17/32",
        "bits_per_second_up": 1840000,
        "bits_per_second_down": 48210000,
        "packets_per_second_up": 1450.2,
        "packets_per_second_down": 4180.5
      },
      {
        "prefix": "198.51.100.19/32",
        "bits_per_second_up": null,
        "bits_per_second_down": null,
        "packets_per_second_up": null,
        "packets_per_second_down": null
      }
    ]
  },
  "meta": {
    "request_id": "req_01JZ6FQ4CV2JYJYNJ9E3PG7A7P",
    "organization_id": 42,
    "source": "victoria_metrics",
    "pagination": {},
    "truncated": false,
    "data_available_from": "2026-07-13T00:00:00Z"
  }
}
```

Read this as follows:
- **The business `/24`** downloads about 312 Mbit/s and uploads 41 Mbit/s, averaged over the last 5 minutes.
- **Subscriber `198.51.100.17`** downloads 48.2 Mbit/s. Its upload is small in bits (1.8 Mbit/s) but busy in packets (1450 packets/s), which is typical of TCP acknowledgements for a large download.
- **Subscriber `198.51.100.19`** has no samples in the window (`null`). Its class may be new or the subscriber may be disconnected; that is not the same as `0`, which means "measured, idle".

Optional `time` (RFC3339) evaluates the window ending at that moment instead of now. You can select at most `limits.traffic.max_selected_prefixes` prefixes (default 200); duplicates collapse. `prefixes: []` is an error, and `prefixes` cannot be combined with `cursor`. Omit `prefixes` to get every prefix in the organization, paged (next section).

The selected prefixes become part of the query the server runs. If they make it longer than the server's query-size limit (16 KiB by default; long IPv6 prefixes use more of it), the request fails with `400 invalid_request` and the message "too many prefixes for one request"; split the prefixes across several requests. The same applies to `/series` and `/totals`.

### Polling recipe: all prefixes every 5 minutes

To collect rates for every prefix, omit `prefixes`, ask for the largest page, and follow `next_cursor` until it is `null`:

```bash
curl --fail-with-body --silent --show-error \
  "$STATS_API_URL/api/v1/traffic/rates" \
  -H "X-API-Key: $STATS_API_KEY" \
  -H 'Content-Type: application/json' \
  --data '{"window_seconds": 300, "page_size": 5000}'
```

```python
import os
import time
import requests

BASE_URL = os.environ["STATS_API_URL"]
HEADERS = {"X-API-Key": os.environ["STATS_API_KEY"], "Accept": "application/json"}


def fetch_all_rates():
    rates, cursor = [], None
    while True:
        body = {"window_seconds": 300, "page_size": 5000}
        if cursor:
            body["cursor"] = cursor
        r = requests.post(f"{BASE_URL}/api/v1/traffic/rates", headers=HEADERS, json=body, timeout=25)
        if r.status_code == 429:
            time.sleep(int(r.headers.get("Retry-After", "5")))
            continue
        r.raise_for_status()
        payload = r.json()
        rates.extend(payload["data"]["rates"])
        cursor = payload["meta"]["pagination"]["next_cursor"]
        if cursor is None:
            return rates


def mbit(value):
    return None if value is None else round(value / 1_000_000, 2)


while True:
    started = time.monotonic()
    rows = fetch_all_rates()
    polled_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    # One line per prefix, ready for a time-series database or a CSV file.
    with open("traffic-rates.csv", "a") as out:
        for row in rows:
            out.write(f'{polled_at},{row["prefix"]},'
                      f'{mbit(row["bits_per_second_down"])},{mbit(row["bits_per_second_up"])}\n')

    # The five busiest prefixes right now (prefixes without data are skipped).
    busiest = sorted((r for r in rows if r["bits_per_second_down"] is not None),
                     key=lambda r: r["bits_per_second_down"], reverse=True)[:5]
    for r in busiest:
        print(f'{r["prefix"]:>20}  down {mbit(r["bits_per_second_down"]):>8} Mbit/s'
              f'  up {mbit(r["bits_per_second_up"]):>8} Mbit/s')

    time.sleep(max(0, 300 - (time.monotonic() - started)))
```

The same single poll in server-side JavaScript (Node.js 18 or later):

```javascript
const baseUrl = process.env.STATS_API_URL;
const headers = {
  "X-API-Key": process.env.STATS_API_KEY,
  "Accept": "application/json",
  "Content-Type": "application/json"
};

async function fetchAllRates() {
  const rates = [];
  let cursor = null;
  for (;;) {
    const body = {window_seconds: 300, page_size: 5000};
    if (cursor) body.cursor = cursor;
    const response = await fetch(`${baseUrl}/api/v1/traffic/rates`, {
      method: "POST",
      headers,
      body: JSON.stringify(body),
      signal: AbortSignal.timeout(25_000)
    });
    if (response.status === 429) {
      const wait = Number(response.headers.get("retry-after") ?? "5");
      await new Promise((resolve) => setTimeout(resolve, wait * 1000));
      continue;
    }
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(`${response.status} ${payload.error?.code}: ${payload.error?.message} request_id=${payload.error?.request_id}`);
    }
    rates.push(...payload.data.rates);
    cursor = payload.meta.pagination.next_cursor;
    if (cursor === null) return rates;
  }
}

const rows = await fetchAllRates();
const busiest = rows
  .filter((r) => r.bits_per_second_down !== null)
  .sort((a, b) => b.bits_per_second_down - a.bits_per_second_down)
  .slice(0, 5);
for (const r of busiest) {
  console.log(`${r.prefix}  down ${(r.bits_per_second_down / 1e6).toFixed(2)} Mbit/s`);
}
```

Save this as `poll-rates.mjs`. The `.mjs` extension lets Node.js use `await` at the top level. Run it from cron or a systemd timer every 5 minutes.

Pages come from one consistent snapshot: the cursor pins the evaluation time, so every page of one run is for the same instant. Do not modify the other request fields between pages; a cursor sent with a different `window_seconds`, or one that is malformed, from another endpoint, older than `data_available_from` or in the future, fails with `400 invalid_cursor`. Restart from the first page rather than reusing an old cursor.

Request budget: one request returns up to 5000 prefixes, so 10,000 prefixes take 2 requests and 60,000 take 12 per poll. That is well inside the default per-key limit of 60 requests per minute. A poll every 5 minutes is plenty because rates are averages over a window of at least 2 minutes; polling more often returns largely the same numbers.

### Graph recipe: series

`/series` returns rates on a fixed time grid for graphing.

```bash
curl --fail-with-body --silent --show-error \
  "$STATS_API_URL/api/v1/traffic/series" \
  -H "X-API-Key: $STATS_API_KEY" \
  -H 'Content-Type: application/json' \
  --data '{
    "prefixes": ["198.51.100.17"],
    "start": "2026-11-23T18:00:00Z",
    "end": "2026-11-23T23:00:00Z",
    "step_seconds": 300
  }'
```

```json
{
  "data": {
    "series": [
      {
        "prefix": "198.51.100.17/32",
        "samples": [
          {
            "timestamp": "2026-11-23T18:00:00Z",
            "bits_per_second_up": 1100000,
            "bits_per_second_down": 47000000,
            "packets_per_second_up": 1400,
            "packets_per_second_down": 4100
          },
          {
            "timestamp": "2026-11-23T18:05:00Z",
            "bits_per_second_up": 1350000,
            "bits_per_second_down": 61800000,
            "packets_per_second_up": 1720,
            "packets_per_second_down": 5390
          },
          {
            "timestamp": "2026-11-23T18:10:00Z",
            "bits_per_second_up": null,
            "bits_per_second_down": null,
            "packets_per_second_up": null,
            "packets_per_second_down": null
          }
        ]
      }
    ]
  },
  "meta": {"request_id": "req_01JZ6FQ4CV2JYJYNJ9E3PG7A7P", "organization_id": 42, "source": "victoria_metrics", "pagination": {}, "truncated": false}
}
```

For the organization total as a single line, use `"group_by": "none"` and omit `prefixes`:

```json
{"start": "2026-11-23T00:00:00Z", "group_by": "none"}
```

With `group_by: "none"` and `prefixes`, you get one series summed over just those prefixes; its `prefix` is `null`. The default `group_by` is `"prefix"`, which requires `prefixes` and returns one series per prefix.

Things to know about the grid:

- `end` defaults to now. `step_seconds` defaults to a value that gives about 240 points over the range.
- `step_seconds` below the server floor (default 120) is raised to the floor. A `step_seconds` longer than the range (`end` minus `start`) fails with `400 invalid_request`.
- `start` is aligned down to a multiple of the step, and the returned grid starts at the aligned time. A `start` of `00:03:00Z` with a 300 s step returns `00:00:00Z` as the first timestamp. Use the returned `timestamp` values, not the ones you requested.
- A timestamp without data has `null` values; do not draw it as zero.
- Too many prefixes times too many points fails with `422 result_too_large`. `error.details.max_prefixes_for_request` says how many prefixes would fit for that range and step (never more than `max_selected_prefixes`); reduce the prefix count, widen the step, or use `group_by: "none"`. The selection itself is checked first: more than `max_selected_prefixes` prefixes is a `400 invalid_request`, and an unknown prefix is a `404 unknown_prefix`, even when the result would also be too large.

### Monthly totals recipe

`/totals` returns bytes and packets for a calendar month. The month is evaluated in `timezone` (an IANA name, default `UTC`):

```bash
curl --fail-with-body --silent --show-error \
  "$STATS_API_URL/api/v1/traffic/totals" \
  -H "X-API-Key: $STATS_API_KEY" \
  -H 'Content-Type: application/json' \
  --data '{"month": "2026-10", "timezone": "Europe/Budapest", "prefixes": ["198.51.100.17"]}'
```

```json
{
  "data": {
    "period": {
      "start": "2026-09-30T22:00:00Z",
      "end": "2026-10-31T23:00:00Z",
      "complete": true,
      "source": "live"
    },
    "totals": [
      {
        "prefix": "198.51.100.17/32",
        "bytes_up": 38120455120,
        "bytes_down": 412377031884,
        "packets_up": 231004871,
        "packets_down": 343647526
      }
    ]
  },
  "meta": {"request_id": "req_01JZ6FQ4CV2JYJYNJ9E3PG7A7P", "organization_id": 42, "source": "victoria_metrics", "pagination": {}, "truncated": false}
}
```

- **Period:** give exactly one of `month` (`YYYY-MM`) or `start` with an optional `end`. `timezone` is only valid with `month`, and must be an IANA name such as `Europe/Budapest` (`Local` is rejected). `period.start` and `period.end` are UTC; `end` is exclusive.
- **`period.complete`** is `true` when the period has fully elapsed. It is `false` for the current month, for a `start`-only range, and when an explicit `end` is later than now; in that case the end is clamped to now and totals cover the period so far. Re-request to get updated numbers.
- **Not for billing.** `period.source` is `"live"`: totals are derived from live counters, rounded to integers, and are subject to the double-counting caveat above. Use them for dashboards and reports, not invoicing.
- **All prefixes:** omit `prefixes` for a page per request over every prefix, using `page_size` and `cursor` exactly as for `/rates`. The cursor pins the period end, so an open month is consistent across pages. `prefixes` and `cursor` cannot be combined.
- **Organization total:** `"group_by": "none"` returns a single row with `prefix: null`. It is not paged, so `cursor` is rejected.

The window must start on or after `meta.data_available_from`, and a custom range is limited to the same 31 days as other queries; earlier months fail with `422 range_not_available`.

In the example, subscriber `198.51.100.17` downloaded about 412 GB and uploaded about 38 GB in October (Budapest time).

A monthly report for every prefix, written to CSV with GB values:

```python
import csv
import os
import requests

BASE_URL = os.environ["STATS_API_URL"]
HEADERS = {"X-API-Key": os.environ["STATS_API_KEY"], "Accept": "application/json"}


def monthly_totals(month, timezone="UTC"):
    rows, cursor = [], None
    while True:
        body = {"month": month, "timezone": timezone, "page_size": 5000}
        if cursor:
            body["cursor"] = cursor
        r = requests.post(f"{BASE_URL}/api/v1/traffic/totals", headers=HEADERS, json=body, timeout=25)
        r.raise_for_status()
        payload = r.json()
        rows.extend(payload["data"]["totals"])
        cursor = payload["meta"]["pagination"]["next_cursor"]
        if cursor is None:
            return payload["data"]["period"], rows


def gb(value):
    return "" if value is None else f"{value / 1e9:.2f}"


period, rows = monthly_totals("2026-10", "Europe/Budapest")
if not period["complete"]:
    print("warning: the month is not over yet; totals are so far")

with open("traffic-2026-10.csv", "w", newline="") as f:
    out = csv.writer(f)
    out.writerow(["prefix", "download_gb", "upload_gb"])
    for row in rows:
        out.writerow([row["prefix"], gb(row["bytes_down"]), gb(row["bytes_up"])])
```

### Traffic errors

In addition to the common errors below:

| Status | `error.code` | Meaning |
|---:|---|---|
| `404` | `unknown_prefix` | A requested prefix is not known for the organization. `details.prefixes` lists the strings that did not resolve. Check them against `/prefixes`. |
| `400` | `invalid_cursor` | The cursor is malformed, was issued for different request parameters or another endpoint, predates `data_available_from`, or is in the future. Restart paging from the first page. |
| `422` | `result_too_large` | The request would exceed the series or point limits. For `/series`, `details.max_prefixes_for_request` is the largest prefix count that fits. |
| `400` | `invalid_request` | For example `prefixes: []`, more than `max_selected_prefixes` prefixes, `prefixes` with `cursor`, `timezone` without `month`, `group_by: "prefix"` without `prefixes` in `/series`, a `step_seconds` longer than the range, too many prefixes for one request (the query would exceed the size limit), or a time in the future (see **Time** above for `/totals`). |

## Metrics

For traffic of your prefixes (rates, graphs, monthly totals) use [Traffic](#traffic) instead. This section is the advanced raw-metrics interface: it exposes every metric we collect, including per-prefix drops, shaping limits and contract numbers, and the health of your shapers.

Metrics endpoints require `metrics:read`. Expressions use MetricsQL. The service adds the organization filter itself, and `organization_id` is reserved and removed from returned labels.

### Metric catalog

#### Per-prefix traffic

One series per prefix per shaper, read from the shaper's traffic classes every 60 seconds. Samples are timestamped with the time they were read on the shaper.

| Metric | Type | Unit | Meaning |
|---|---|---|---|
| `bytes_down`, `bytes_up` | counter | bytes | Bytes forwarded toward (`down`) or from (`up`) the prefix, including hardware-offloaded traffic. |
| `pkts_down`, `pkts_up` | counter | packets | Packets forwarded, including hardware-offloaded traffic. |
| `dropped_down`, `dropped_up` | counter | packets | Packets the shaper dropped for the prefix, usually because it exceeded its shaping limit (including drops in hardware offload). |
| `overlimits_down`, `overlimits_up` | counter | events | Times the class hit its rate limit. Packets may have been delayed rather than dropped. |
| `requeues_down`, `requeues_up` | counter | packets | Packets requeued by the shaper. This is a low-level diagnostic, normally close to zero. |
| `download`, `upload` | gauge | kbit/s | The configured shaping limit for the prefix (its plan speed). `250000` means 250 Mbit/s. |

**Counters only go up** until the shaper rebuilds its classes, which resets them to zero. Never chart a counter's raw value. Use `rate(metric[5m])` for per-second values and `increase(metric[1h])` for amounts over a period; both handle resets. Because readings arrive once a minute, use windows of at least `2m`. **Gauges** (`download`, `upload`) are used as they are.

Labels on every per-prefix series:

| Label | Example | Meaning |
|---|---|---|
| `prefix` | `198.51.100.17/32` | The shaped prefix, exactly as configured on the shaper. It may be written with or without `/32`, so check with discovery before matching exactly, or use the [Traffic](#traffic) API, which normalizes it. |
| `service_id` | `20231187` | Your contract or service number from the CRM (for example the contract number), when the prefix was provisioned from it. Missing when the prefix has none. |
| `grp` | `default` | The shaping group the prefix belongs to. |
| `source` | `crm` | Where the prefix configuration came from, for example the CRM integration or manual configuration. |
| `shaper_id` | `shaper-01` | Hostname of the shaper that measured the traffic. |
| `customer_id` | `1042` | The shaper's statistics account. It is the same for all prefixes of one shaper; it is not your customer's identifier. |

#### Shaper health

One series per shaper (and per network interface for `interface_*`), labelled `shaper_id` and `customer_id` as above.

| Metric | Type | Unit | Meaning |
|---|---|---|---|
| `interface_rx_bytes`, `interface_tx_bytes` | counter | bytes | Bytes received and sent per network interface. The `device` label is the interface name. |
| `interface_rx_packets`, `interface_tx_packets` | counter | packets | Packets received and sent per interface. |
| `interface_rx_dropped`, `interface_tx_dropped` | counter | packets | Packets dropped by the interface. |
| `cpu_dataplane_util_percent` | gauge | % | CPU used for forwarding traffic. This is the one to watch for capacity. |
| `cpu_controlplane_util_percent` | gauge | % | CPU used by management and control processes. |
| `memory_total_bytes`, `memory_used_bytes`, `memory_available_bytes`, `memory_free_bytes` | gauge | bytes | Memory of the shaper. `used` = `total` − `available`. |
| `system_uptime_seconds` | gauge | seconds | Time since the shaper booted. A drop to near zero means a reboot. |
| `system_power_consumption_watts` | gauge | W | Power draw, on hardware that reports it. |
| `system_platform_info`, `system_netxos_version_info`, `system_netc_version_info`, `system_kernel_version_info` | info | — | Always `1`. The information is in the labels `platform`, `netxos`, `netc_version` and `kernel_version`. |

### MetricsQL recipes

Send each expression as `expression` to `/api/v1/metrics/query` (one value per series, at `time` or now) or `/api/v1/metrics/query-range` (a series over `start`–`end`). In JSON, escape the double quotes inside the expression as `\"`.

**Download speed of one subscriber, in bits/s** (summed over shapers, in case the prefix is shaped on more than one):

```
sum(rate(bytes_down{prefix="198.51.100.17/32"}[5m])) * 8
```

**The 10 busiest prefixes right now, by download:**

```
topk(10, sum by (prefix) (rate(bytes_down[5m])) * 8)
```

**How close each prefix is to its plan speed, in percent** (prefixes above 90%):

```
(sum by (prefix) (rate(bytes_down[5m])) * 8)
  / (max by (prefix) (download) * 1000) * 100 > 90
```

`download` is in kbit/s, hence `* 1000`. A subscriber that stays near 100% is using the full plan; combine it with the drop rate below to see whether the limit is actually hurting.

**Drop ratio per prefix, in percent** (prefixes losing more than 1% of downstream packets to shaping):

```
sum by (prefix) (rate(dropped_down[5m]))
  / (sum by (prefix) (rate(pkts_down[5m])) + sum by (prefix) (rate(dropped_down[5m]))) * 100 > 1
```

`pkts_down` counts forwarded packets only, so the total offered is forwarded plus dropped.

**Traffic per contract over the last 30 days, in GB:**

```
sum by (service_id) (increase(bytes_down{service_id!=""}[30d])) / 1e9
```

**Shaper interface throughput, in bits/s:**

```
sum by (shaper_id, device) (rate(interface_rx_bytes[5m])) * 8
```

**Shaper load:** data-plane CPU and memory usage in percent:

```
max by (shaper_id) (cpu_dataplane_util_percent)
```

```
max by (shaper_id) (memory_used_bytes / memory_total_bytes) * 100
```

**Software versions per shaper:**

```
system_netc_version_info
```

The result's labels carry the version (`netc_version`). Use `system_uptime_seconds < 600` to find shapers that rebooted in the last 10 minutes.

### Raw metrics example: query a prefix

To get the downstream packet counter for `198.51.100.17` at a specific time, select `pkts_down` with an exact `prefix` matcher:

```bash
curl --fail-with-body --silent --show-error \
  "$STATS_API_URL/api/v1/metrics/query" \
  -H "X-API-Key: $STATS_API_KEY" \
  -H 'Content-Type: application/json' \
  --data '{
    "expression": "pkts_down{prefix=\"198.51.100.17/32\"}",
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
          "customer_id": "1042",
          "shaper_id": "shaper-01",
          "grp": "default",
          "prefix": "198.51.100.17/32",
          "source": "crm",
          "service_id": "20231187"
        },
        "samples": [
          {"timestamp": "2026-07-13T11:00:00Z", "value": "8412650331"}
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

The value is the counter's raw reading: packets since the class was created, which on its own is rarely useful. Wrap it in `rate()` or `increase()` as in the recipes above. Values are strings in the API response even though the shaper writes integers. The API key supplies the organization scope, so do not add an `organization_id` matcher. The `prefix` value must exactly match the stored label; if you are not sure whether it is stored as `198.51.100.17` or `198.51.100.17/32`, list values with [Metrics discovery](#metrics-discovery) or use `prefix=~"198\\.51\\.100\\.17(/32)?"`. An empty `series` array means no matching sample was found at that time.

Omit `time` to evaluate at the current server time.

### Range query

To graph the download speed of the same prefix over one hour, in bits/s, one point per minute:

```bash
curl --fail-with-body --silent --show-error \
  "$STATS_API_URL/api/v1/metrics/query-range" \
  -H "X-API-Key: $STATS_API_KEY" \
  -H 'Content-Type: application/json' \
  --data '{
    "expression": "sum by (prefix) (rate(bytes_down{prefix=\"198.51.100.17/32\"}[5m])) * 8",
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
          "prefix": "198.51.100.17/32"
        },
        "samples": [
          {"timestamp": "2026-07-13T10:00:00Z", "value": "47013520"},
          {"timestamp": "2026-07-13T10:01:00Z", "value": "52880144"}
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
| `404` | A traffic prefix is unknown (`unknown_prefix`); check it against `/api/v1/traffic/prefixes`. |
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

## MCP endpoint for AI assistants

When enabled (`external_api.mcp_enabled`), the same read-only API is available to AI assistants as a [Model Context Protocol](https://modelcontextprotocol.io) server at `/mcp` (Streamable HTTP, stateless). It uses the same `X-API-Key` header, the same scopes, and the same organization scoping and limits: each tool call runs the matching `/api/v1` operation with the caller's key.

| Tool | Operation |
|---|---|
| `get_capabilities` | `/api/v1/capabilities` |
| `list_traffic_prefixes` | `GET /api/v1/traffic/prefixes` |
| `get_traffic_rates` | `/api/v1/traffic/rates` |
| `get_traffic_series` | `/api/v1/traffic/series` |
| `get_traffic_totals` | `/api/v1/traffic/totals` |
| `query_metrics`, `query_metrics_range` | `/api/v1/metrics/query`, `/api/v1/metrics/query-range` |
| `list_metric_names`, `list_metric_labels`, `list_metric_label_values` | metrics discovery |
| `search_logs`, `get_log_histogram`, `get_log_facets` | `/api/v1/logs/search`, `/histogram`, `/facets` |
| `list_log_fields`, `list_log_field_values` | logs discovery |

The traffic tools are the preferred way for an assistant to answer questions about prefix traffic; raw MetricsQL is only needed for other series. `get_traffic_series` without `prefixes` returns the organization total, and `get_traffic_totals` without a period returns the current month, in `timezone` if given (default UTC). Tool times accept the same forms as the other tools (`now-7d`, a date, RFC3339). A key with only `traffic:read` can use `/mcp`: the traffic tools work, `get_capabilities` reports only the traffic provider, and the raw metrics and log tools return `insufficient_scope`.

Tools also accept relative times (`now`, `now-15m`, `now-6h`, `now-7d`) and default to the last hour. Range queries pick a step of about 240 points per series, and log search returns 50 records by default. Tool results larger than 200 kB are refused with advice to narrow the query.

Claude Code:

```bash
claude mcp add --transport http netx-stats https://stats.netx.as/mcp \
  --header "X-API-Key: sak_your_key"
```

Cursor (`.cursor/mcp.json`) and VS Code (`.vscode/mcp.json`, under `servers` instead of `mcpServers`):

```json
{
  "mcpServers": {
    "netx-stats": {
      "url": "https://stats.netx.as/mcp",
      "headers": { "X-API-Key": "sak_your_key" }
    }
  }
}
```

Claude Desktop and claude.ai custom connectors cannot send custom headers yet, so they cannot use API-key authentication.

Create a separate key for each person or assistant so it can be revoked on its own. Metric values and log records returned by tools are sent to the model the assistant uses.

## Integration checklist

- Store the API key in a secret manager and rotate it according to your organization's credential policy.
- Call `/api/v1/capabilities` during startup or configuration validation.
- Keep request ranges and result sizes below the advertised limits.
- Set a client timeout and implement bounded retry with jitter only for `429` and transient `5xx` responses.
- Record `request_id`, status, and `error.code`, but never record the API key or full sensitive queries.
- Validate the integration with data belonging only to the assigned organization.
