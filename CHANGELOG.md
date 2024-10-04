# Change log

## [0.1.6] - 2024-10-04

## Changed

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
