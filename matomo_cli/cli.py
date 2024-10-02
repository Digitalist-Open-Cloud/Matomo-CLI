import requests
import click
import json

from matomo_cli.environment import Environment

@click.command()
@click.argument("api", required=True)
@click.option("--format", "-f", default='tsv', help="Format to output (json, tsv and xml supported)")
@click.option("--method", "-m", default='API.getMatomoVersion', help="Method to use (like: API.getMatomoVersion)")
@click.option("--idsite", "-i", default='1', type=int, help="idsite to ask for")
@click.option("--idsites", "-i", default='1', help="Comma seperated lists for sites")
@click.option("--segmentname", "-sn", help="Segment name")
@click.option("--period", "-p", default='day', help="Period to ask for (like day, month, year)")
@click.option("--date", "-d", default='today', help="Date to use (like today, yesterday or 2024-10-02)")
@click.option("--show_columns", "-sc", help="Limit which columns are shown")

def cli(api: str, format, method, idsite, idsites, segmentname, period, date, show_columns) -> None:

    environment = Environment()
    environment.check_environment()

    api_url = environment.url

    payload = {
        'module': 'API',
        'method': method,
        'format': format,
        'token_auth': environment.token,
    }
    if idsite is not None:
        payload['idSite'] = idsite

    if idsites is not None:
        payload['idSites'] = idsites

    if segmentname is not None:
        payload['segmentName'] = segmentname

    if period is not None:
        payload['period'] = period

    if date is not None:
        payload['date'] = date

    if show_columns is not None:
        payload['showColumns'] = show_columns

    response = requests.post(api_url, params=payload)

    if response.status_code == 200:
      if (format == 'xml'):
        websites = response.text
        print(websites)
      if (format == 'tsv'):
        websites = response.text
        print_tsv(websites)
      if (format == 'json'):
        websites = response.json()
        print(websites)


def print_tsv(tsv_data):
    # Split the TSV data by lines and tabs
    lines = tsv_data.strip().split('\n')

    # Print headers
    headers = lines[0].split('\t')
    print("\t".join(headers))

    # Print each row
    for line in lines[1:]:
        row = line.split('\t')
        print("\t".join(row))


if __name__ == "__main__":
    cli()