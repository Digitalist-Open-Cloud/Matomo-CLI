# CLI and Prometheus exporter for Matomo.
#
# Copyright (C) 2024 Digitalist Open Cloud <cloud@digitalist.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Module providing metrics for Matomo."""

import rich_click as click
import requests

@click.command()
@click.option('--metrics', "matomoMetrics", help="Which metrics to return")
@click.option(
    "--url", "-u", envvar="MATOMO_URL", help="URL to Matomo instance"
)
@click.option(
    "--token", "-t", envvar="MATOMO_TOKEN", help="Matomo auth token"
)
def metrics(url, token, matomoMetrics):
    """Fetch metrics"""

    payload = {
        "module": "API",
        "format": "json",
        "token_auth": token,
    }

    if matomoMetrics is not None and matomoMetrics == 'version':
        payload['method'] = "API.getMatomoVersion"

    elif matomoMetrics is not None and matomoMetrics == 'php':
        payload['method'] = "API.getPhpVersion"

    response = requests.post(url, params=payload, timeout=1000)

    if response.status_code == 200:
        result = response.json()
        print(result)
        # for key, value in result.items():
        #     print(value)
        #     return(value)
if __name__ == "__main__":
    metrics()
