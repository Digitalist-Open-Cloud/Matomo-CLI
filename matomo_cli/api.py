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

"""Module providing an API wrapper for Matomo."""

import requests
import rich_click as click
import unicodedata

@click.command()
@click.option(
    "--url", "-u", envvar="MATOMO_URL", help="URL to Matomo instance"
)
@click.option(
    "--token", "-t", envvar="MATOMO_TOKEN", help="Matomo auth token"
)
@click.option(
    "--output_format", "-f", envvar="MATOMO_OUTPUT_FORMAT", default="tsv",
    help="Format to output (original, json, tsv, and xml supported)"
)
@click.option(
    "--method", "-m", default="API.getMatomoVersion",
    help="Method to use (e.g., API.getMatomoVersion)"
)
@click.option(
    "--id_site", "idSite", "-i", envvar="MATOMO_ID_SITE", default=1, type=int,
    help="ID site to ask for"
)
@click.option(
    "--id_sites", "idSites", "-is", envvar="MATOMO_ID_SITES", default="1",
    help="Comma-separated list of sites"
)
@click.option(
    "--segment_name", "segmentName", "-sn", help="Segment name"
)
@click.option(
    "--period", "-p", envvar="MATOMO_PERIOD", default="day",
    help="Period to ask for (e.g., day, month, year)"
)
@click.option(
    "--date", "-d", envvar="MATOMO_DATE", default="today",
    help="Date to use (e.g., today, yesterday, or 2024-10-02)"
)
@click.option(
    "--show_columns", "showColumns", "-sc", help="Limit which columns are shown"
)
@click.option(
    "--site_name", "siteName", "-sn", help="Site name"
)
@click.option(
    "--api_module", "apiModule", "-am", help="API module"
)
@click.option(
    "--api_action", "apiAction", "-ac", help="API action"
)
@click.option(
    "--serialize", "-se", type=int, help="Serialize (1 or 0)"
)
@click.option(
    "--limit", "-l", envvar="MATOMO_LIMIT", type=int, default=1,
    help="Limit result to this number"
)
@click.option(
    "--offset", "-o", envvar="MATOMO_OFFSET", type=int, default=0,
    help="Offset result"
)

def api(
    url, token, output_format, method, **api_params
) -> None:
    """Make API calls to the Matomo instance."""

    api_url = url
    payload = {
        "module": "API",
        "method": method,
        "format": output_format,
        "token_auth": token,
    }

    # Add parameters to payload from api_params
    payload.update({
        key: value for key, value in api_params.items() if value is not None
    })

    # Special case handling for method SitesManager.addSite
    if "site_name" in api_params and method == "SitesManager.addSite":
        payload.pop("idSite", None)

    # Make API request
    response = requests.post(api_url, params=payload, timeout=1000)

    # Handle the response based on output format
    if response.status_code == 200:
        text = remove_non_utf8_characters(response.text)
        if output_format in ("xml", "original"):
            print(text)
        elif output_format == "tsv":
            print_tsv(text)
        elif output_format == "json":
            print(response.json())


def print_tsv(tsv_data: str) -> None:
    """Format and print TSV data."""
    # Split the TSV data by lines and tabs
    lines = tsv_data.strip().split("\n")

    # Print headers
    headers = lines[0].split("\t")
    print("\t".join(headers))

    # Print each row
    for line in lines[1:]:
        row = line.split("\t")
        print("\t".join(row))

def remove_non_utf8_characters(response):
    """
    Remove non-UTF-8 and other problematic characters from a response.
    """
    # Normalize the string to remove special characters
    response = unicodedata.normalize("NFKD", response)

    # Remove non-ASCII characters that could be causing issues
    clean_response = response.encode('ascii', 'ignore').decode('ascii')

    return clean_response

if __name__ == "__main__":
    api()
