import requests
import rich_click as click

@click.command()
@click.option("--url", "-u", envvar='MATOMO_URL', help="URL to Matomo instance")
@click.option("--token", "-t", envvar='MATOMO_TOKEN', help="Matomo auth token")
@click.option("--format", "-f", envvar='MATOMO_FORMAT', default='tsv', help="Format to output (original, json, tsv and xml supported)")
@click.option("--method", "-m", default='API.getMatomoVersion', help="Method to use (like: API.getMatomoVersion)")
@click.option("--id_site", "-i", envvar='MATOMO_ID_SITE', default='1', type=int, help="idsite to ask for")
@click.option("--id_sites", "-is", envvar='MATOMO_ID_SITES', default='1', help="Comma seperated lists for sites")
@click.option("--segment_name", "-sn", help="Segment name")
@click.option("--period", "-p", envvar='MATOMO_PERIOD', default='day', help="Period to ask for (like day, month, year)")
@click.option("--date", "-d", envvar='MATOMO_DATE', default='today', help="Date to use (like today, yesterday or 2024-10-02)")
@click.option("--show_columns", "-sc", help="Limit which columns are")
@click.option("--site_name", "-sn", help="Site name")
@click.option("--api_module", "-am", help="API module")
@click.option("--api_action", "-ac", help="API action")
@click.option("--serialize", "-se", type=int, help="Serialize (1 or 0)")
@click.option("--limit", "-l", type=int,  default='1', help="Limit result to this number")
@click.option("--offset", "-o", type=int,  default='0', help="Offset result")
def api(
    url,
    token,
    format,
    method,
    id_site,
    id_sites,
    segment_name,
    period,
    date,
    show_columns,
    site_name,
    api_module,
    api_action,
    serialize,
    limit,
    offset
    ) -> None:
    """Do API calls"""

    api_url = url

    payload = {
        'module': 'API',
        'method': method,
        'format': format,
        'token_auth': token,
    }
    if id_site is not None:
        payload['idSite'] = id_site

    if id_sites is not None:
        payload['idSites'] = id_sites

    if segment_name is not None:
        payload['segmentName'] = segment_name

    if period is not None:
        payload['period'] = period

    if date is not None:
        payload['date'] = date

    if show_columns is not None:
        payload['showColumns'] = show_columns

    if site_name is not None:
        payload['siteName'] = site_name
        if method == 'SitesManager.addSite':
          payload.pop('idSite', None)

    if api_module is not None:
        payload['apiModule'] = api_module

    if api_action is not None:
        payload['apiAction'] = api_action

    if serialize is not None:
        payload['serialize'] = serialize

    if limit is not None:
        payload['limit'] = limit

    if offset is not None:
        payload['offset'] = offset


    response = requests.post(api_url, params=payload)

    if response.status_code == 200:
      if (format == 'xml'):
        result = response.text
        print(result)
      if (format == 'original'):
        result = response.text
        print(result)
      if (format == 'tsv'):
        result = response.text
        print_tsv(result)
      if (format == 'json'):
        result = response.json()
        print(result)

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
    api()