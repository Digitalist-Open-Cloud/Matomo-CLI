# Readme

This is a very simple and limited cli tool for Matomo API requests and a [Prometheus exporter](https://prometheus.io/) for Matomo.

Very limited support for anything in general regarding API. This was created as a need for a Prometheus exporter for Matomo, and we, [Digitalist Open Cloud](https://digitalist.cloud/), needed a base to test calls to Matomo. Hopefully it could be used and developed together with the community.

## Environment variables

Many options could be replaced with environment variables.

| Environment Variable | Description             | Default |
| -------------------- | ----------------------  | ------- |
| MATOMO_URL           | URL to Matomo instance  | -       |
| MATOMO_TOKEN         | Access token for Matomo | -       |
| MATOMO_ID_SITE       | Site ID                 | 1       |
| MATOMO_ID_SITES      | Comma separated id's    | -       |
| MATOMO_PERIOD        | Period (day, week etc)  | day     |
| MATOMO_DATE          | today, yesterday, 2024-10-02 etc. | - |
| MATOMO_OUTPUT_FORMAT | json, xml or tsv.       | tsv     |
| MATOMO_LIMIT         | Number of results       | -       |

## Usage

```sh

matomo --help
matomo api --help

```

```sh
export MATOMO_URL=https://mymatomo.instance/index.php
export MATOMO_TOKEN=MYAUTHTOKENFROMMATOMO

matomo api --method MultiSites.getAll --period month --date 2024-08-20 --show_columns nb_actions
```

The method you provide is the API call the tool will do (see your Matomo installation on what API:s you could use)

## Installation

```sh
pip install matomo-cli

```

or

```sh
pipx install git+https://github.com/Digitalist-Open-Cloud/Matomo-CLI.git
```

or run as docker image:

```sh
docker run digitalist/matomo-cli matomo --help
```

Docker releases of the cli you can find at [Docker hub](https://hub.docker.com/r/digitalist/matomo-cli).

## Known supported API methods

The Matomo API has many methods, and could be extended with plugins, here is a list of methods we know this tool is supporting. Please note, that for now, some methods only works well with json and xml output. And for all them, not all possible options is available in the tool yet.

| Method     |
| ---------- |
| ActivityLog.getEntries |
| API.getMatomoVersion |
| API.getPhpVersion |
| API.getIpFromHeader |
| API.getSettings |
| BotTracker.defaultBots |
| BotTracker.getTop10 |
| MultiSites.getAll |
| PagePerformance.get |
| SitesManager.addSite |
| SitesManager.deleteSite |
| SitesManager.getAllSites |
| SitesManager.getAllSitesId |
| SitesManager.getJavascriptTag |
| _Etc._ |

## General documentation about Matomo API

See:

- <https://developer.matomo.org/api-reference>
- <https://glossary.matomo.org/>

## Prometheus exporter

The Matomo Prometheus exporter, exposes metrics from your Matomo instance.

| Metric | Description |
| ------ | ----------- |
| `matomo_version` | Your version of Matomo |
| `matomo_php_version` | Which PHP version you are running |
| `matomo_total_users` | Total of users |
| `matomo_total_non_excluded_users` | With the variable `MATOMO_EXCLUDE_USERS` you can exclude users from this count |
| `matomo_super_users` | Total number of super users |
| `matomo_number_of_segments` | Total number of segments |
| `matomo_number_of_sites` | Total number of sites |
| `matomo_number_of_actions_YEAR_MONTH` | Number of actions per `MONTH` IN `YEAR` |

The Matomo Exporter is available at [Docker Hub](https://hub.docker.com/r/digitalist/matomo-exporter).

You can run it with:

```sh
docker run --rm -d -e MATOMO_TOKEN='MyAuthToken' -e MATOMO_URL=https://matomo.url/index.php -p 9110:9110 matomo-exporter
```

Or just test it out from the repo:

```sh
export MATOMO_URL=https://matomo.url/index.php
export MATOMO_TOKEN=MyAuthToken

python3 matomo_cli/prometheus.py
```

### Environment variables for the Prometheus exporter

| Environment Variable | Description             | Default | Required |
| -------------------- | ----------------------  | ------- | -------- |
| MATOMO_URL           | URL to Matomo instance  | -       | Yes      |
| MATOMO_TOKEN         | Access token for Matomo | -       | Yes      |
| MATOMO_EXPORTER_PORT | Port for the exporter   | 9110    | No       |
| MATOMO_EXCLUDE_USERS | Comma separated list of emails to exclude for user metrics | - | No |
| MATOMO_EXPORTER_UPDATE | How often to update metrics (in seconds) | 300 | No |
| MATOMO_ACTIONS_FROM_YEAR | From which year to count number of actions / month | 2024 | No |

Note about `MATOMO_EXCLUDE_USERS` - this could be used like exact matches, or partial, comma separated like:
`MATOMO_EXCLUDE_USERS=me@domain.com,internal.com,external`.

### Deployment example of the Prometheus exporter

You need to have your Matomo URL and you Auth token Base64 encoded into the secret.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: matomo-metrics
  labels:
    app: matomo-metrics
spec:
  replicas: 1
  selector:
    matchLabels:
      app: matomo-metrics
  template:
    metadata:
      labels:
        app: matomo-metrics
      annotations:
        prometheus.io/scrape: 'true'
        prometheus.io/path: '/metrics'
        prometheus.io/port: '9110'
    spec:
      containers:
      - name: matomo-metrics
        image: digitalist/matomo-exporter:0.1.8
        ports:
        - containerPort: 9110
          protocol: TCP
        envFrom:
        - secretRef:
            name: matomo-metrics
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
          limits:
            memory: "128Mi"
            cpu: "500m"
---
kind: Service
apiVersion: v1
metadata:
  name: matomo-metrics
spec:
  selector:
    app: matomo-metrics
  ports:
  - name: metrics
    protocol: TCP
    port: 9110
    targetPort: 9110
---
apiVersion: v1
data:
  MATOMO_URL: <REPLACE THIS WITH A BASE64 ENCODED URL TO YOUR MATOMO>
  MATOMO_TOKEN: <REPLACE THIS WITH A BASE54 ENCODED AUTH TOKEN WITH SUPER USER PRIVILEGES>
kind: Secret
metadata:
  name: matomo-metrics
type: Opaque
```

### Grafana dashboard

If you are using Grafana, a simple dashboard is added as an example in `grafana` folder.

## License

Copyright (C) 2024 Digitalist Open Cloud <cloud@digitalist.com>

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.