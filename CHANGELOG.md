# Change log

---

## [0.1.11] - 2024-10-10

## Changed

- `charset-normalizer` updated to 3.4.0
- The check for if using Extra Api Information, set variable from environment variable.

## [0.1.10] - 2024-10-06

## Changed

- Prometheus Exporter: Refactor some of the Prometheus metrics.
- Prometheus Exporter & CLI: Add the possibility to use local certs in requests (env. variable MATOMO_TRUST_SSL_CERT that could be set to path of the local CA, like `mkcert`)
- CLI: Added the option `extra_params` to add extra values to the payload. `extra_params` are added like a comma separated list, like `--extra_params day=today,range=month`

## Removed

- Removed som cli options, this is now replaced with the new

## [0.1.9] - 2024-10-04

### Added

- Prometheus Exporter: example deployment for prometheus exporter in README.
- Prometheus Exporter: example dashboard for Grafana in grafana folder.

## [0.1.8] - 2024-10-04

### Added

- CLI: remove_non_utf8_characters for api calls, to clean the output.

## [0.1.7] - 2024-10-4

### Added

- Prometheus exporter: major, minor and patch version for Matomo and PHP as metric labels

## [0.1.6] - 2024-10-04

### Changed

- Prometheus exporter: changed out of actions count metrics, so month and year now are labels. Example:

```sh
matomo_number_of_actions{month="01",year="2024"} 98118.0
matomo_number_of_actions{month="02",year="2024"} 100301.0
```

## [0.1.5] - 2024-10-03

### Added

- Dockerfile for Prometheus exporter
- Link to Docker hub for docker container for the Prometheus exporter

## [0.1.4] - 2024-10-03

### Added

- Prometheus exporter (see README)
- More environment variables. (see README)

## [0.1.3] - 2024-10-03

### Changed

- Coding format.

### Added

- License (GPL-3.0-or-later)

## [0.1.2] - 2024-10-03

### Changed

- Move api to it's own file, start to use groups in click.
- option `format` changed to `output_format`

### Added

- Some colors to output

### Fixed

- Shorthand options that got wrong.

## [0.1.1] - 2024-10-02

### Added

- Documented some of the supported API calls.
- Added original as output format
- More options added

### Changed

- Some option names for api, for a list for options, run `matomo api --help`

## [0.1.0] - 2024-10-02

### Added

- Limited support for API calls.
