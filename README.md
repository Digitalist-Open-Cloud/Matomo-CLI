# Readme

This is a very simple and limited cli tool for Matomo API requests.

Very limited support for anything in general. This was created as a need for a Prometheus exporter for Matomo, and we needed a base to do the calls to Matomo. Hopefully it could be used and developed together with the community.

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
| MATOMO_FORMAT        | json, xml or tsv.       | tsv       |

## Usage

```sh
export MATOMO_URL=https://mymatomo.instance/index.php
export MATOMO_TOKEN=DHJSHGUAGU8383

matomo api --method MultiSites.getAll --period month --date 2024-08-20 --show_columns nb_actions
```

The method you provide is the API call the tool will do (see your Matomo installation on what API:s you could use)

## Installation

```sh
pipx install git+https://github.com/Digitalist-Open-Cloud/Matomo-CLI.git
```

## Known supported API methods

The Matomo API has many methods, and could be extended with plugins, here is a list of methods we know this tool is supporting. Please note, that for now, some methods only works well with json and xml output. And for all them, not all possible options is available in the tool yet.

| Method     |
| ---------- |
| ActivityLog.getEntries |
| API.getMatomoVersion |
| API.getPhpVersion |
| API.getIpFromHeader |
| API.getSettings |
| MultiSites.getAll |
| PagePerformance.get |
| SitesManager.addSite |
| SitesManager.deleteSite |
| SitesManager.getJavascriptTag |
| _Etc._ |