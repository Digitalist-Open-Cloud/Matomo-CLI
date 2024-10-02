# Readme

This is a very simple and limited cli tool for Matomo API requests.

For now it only supports get requests, not anything related to writing. And very limited support for anything in general. This was created as a need for a Prometheus exporter for Matomo, and we needed a base to do the calls to Matomo.

## Environment variables

The cli tool needs two environment variables to be set, the url of the matomo instance (`MATOMO_URL`) and a token that has access to the instance (`MATOMO_TOKEN`).

## Usage

```sh
matomo api --method MultiSites.getAll --period=month --date=2024-08-20 --show_columns nb_actions
```

The method you provide is API call the tool will do.

