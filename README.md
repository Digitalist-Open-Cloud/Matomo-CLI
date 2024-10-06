# Readme

"Do one thing, and do it well".

Who are you kidding?

This is one project, with at least two tools (things), and maybe both suck. But the intention is to document the two things the best I can. Even when the function doesn't exist. Never trust the documentation. Trust the code. (the studio audience laughs) But not just this code. When there is like, two, three others contributing, from different companies, then we can start to talk about trust. But I guess that will never happen. Even important projects, that glue this thing together we call life, or INTERNET (yes death, I hear you), too often only have one contributor. That person for some reason had an idea to solve one simple thing, and then got lifesentence on that project, because the idea was really great (mostly not, but enough generic to be reused).

You know, there are a thing, similar to death row, it is called, "THE ISSUE QUEUE" (death, shut up!)

That is why I am trying to solve two things in this project (which you never should), so I don't get stuck here. Someday, maybe I just want to be a guy that sometimes have an umbrella with me.

The legend says, there are only two hard things in computer science: cache invalidation (no cache in this project, I guess we failed early) and naming things (yes, failed that also). The third thing that is hard, which I humble want to add, is documentation. This project try to succeed on that. Even to provide too much documentation. And document things are not even in the code, or has noting to with the code, like my rambling in this readme.

Readme always get me to thinking on that plant in the movie Little Shop of Horrors. "Feed me!". Someone, or something in this case, tells me to do something, my normal reaction is to do the opposite. "Read me" reaction would be to not to read.

Where were I? Oh...

So, the code, in some ways, seems to be smart, because it is documented, or have many words in a text file. But it is still shit. Like most code. We hope some random LLM will improve our coding. But it will just repeat our mistakes. And mistakes are gifts. So with that, I don't know where we would go.

Project comes to GitHub to die. Someone had, what they thought to be a great idea. Then something the project dependent on updated or got removed, and everything broke, or you got divorced or you decided that you should be a buddhist monk or you wanted to bake bread instead of code. And the code you wrote never got updated. It started with a dream, or an itch, and then...

This project is nothing different. Life happens. But the code is open source, so if you need it, use it. If something suck (well, I know it does, this is Python code, and I know nothing about how to write Python, I just googled, wrote random lines with some logic, added some spaces, asked ChatGPT for guidance and hoped for the best), fork it, change it, contribute back, fuck it, or just use it and keep your mouth shut. There is not warranty. There is no batteries included. There is just you and the endless void.

That is why the timeout in the external calls in the code are just over 16 minutes. I thought that endless, in todays context, should be something around 16 minutes. Then you die, or eat cake.

Anyhow.

So.

Here you find, a very limited project, that try to solve two things, maybe badly, but with the intent to be really well documented. Maybe not the functions or the code or the project, but the documentation itself should be documented.

And for what it is worth, I think people should carry umbrellas more often. And shoes. I like shoes, and umbrellas. And vampires. I forgot to write about that, but that should be different story.

## What is this?

This is a CLI tool for Matomo API requests and a [Prometheus exporter](https://prometheus.io/) for Matomo. I guess we succeeded with one thing, target the same platform. I hope to do worse in next project, like failing to be a CLI tool for one project and in the same time be a bad backup automation tool for a total different project.

This was project was created because we, [Digitalist Open Cloud](https://digitalist.cloud/), wanted:

- CLI for Matomo: For getting things out of Matomo for our web analysts to work with.
- Prometheus Exporter for Matomo: to collect all the metrics needed for automation in our Matomo SaaS offering.

Intended for our own use cases, but we tried to build generic tools that could be used by the Matomo community.

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
| MATOMO_TRUST_SSL_CERT | Path to local CA | - |
| MATOMO_EXTRA_OPTIONS | Comma separated list of key and value | - |

Note on MATOMO_TRUST_SSL_CERT - if you are using mkcert, path should be something like this:
'/Users/MYUSER/Library/Application Support/mkcert/rootCA.pem' - check where it stores the CA in your environment.

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

The Matomo API has many methods, and could be extended with plugins, here is a list of methods we know this tool is supporting. Please note, that for now, some methods only works well with json and xml output.

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
| `matomo_number_of_actions` | Number of actions per `month` in `year` |

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
| MATOMO_EXTRA_API | Add metrics from the plugin Extra API Information | False | No |

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

## Coffee sponsorship?

Don't buy me a coffee. Normally, I had too many already at this time of the day. If you have use for this project, just tell someone to fuck off that deserve it.

## License

Copyright (C) 2024 Digitalist Open Cloud <cloud@digitalist.com>

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.
