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

"""Prometheus Exporter for Matomo."""
import os
import re
import time
import datetime
import requests
from prometheus_client import start_http_server, Gauge

# Matomo credentials and settings
MATOMO_URL = os.getenv('MATOMO_URL', 'http://your-matomo-url')
MATOMO_TOKEN = os.getenv('MATOMO_TOKEN', 'your-token')
MATOMO_EXPORTER_PORT = int(os.getenv('MATOMO_EXPORTER_PORT', '9110'))
update_metrics_seconds = int(os.getenv('MATOMO_EXPORTER_UPDATE', '300'))
actions_from_year = int(os.getenv('MATOMO_ACTIONS_FROM_YEAR', '2024'))

exclude_users_env = os.getenv('MATOMO_EXCLUDE_USERS', '')
exclude_patterns = [pattern.strip() for pattern in exclude_users_env.split(',') if pattern.strip()]

# Prometheus metrics definition
metrics = {
    'matomo_version': Gauge('matomo_version', 'Version of the Matomo instance', ['full_version','major','minor','patch']),
    'php_version': Gauge('matomo_php_version', 'PHP version of the Matomo instance', ['full_version','major','minor','patch']),
    'total_users': Gauge('matomo_total_users', 'Number of total users'),
    'non_excluded_users': Gauge('matomo_total_non_excluded_users', 'Number of non excluded users'),
    'admin_users': Gauge('matomo_super_users', 'Number of super users'),
    'number_of_segments': Gauge('matomo_number_of_segments', 'Number of segments'),
    'number_of_sites': Gauge('matomo_number_of_sites', 'Number of sites')
}
matomo_actions_gauge = Gauge(
    'matomo_number_of_actions',
    'Number of actions per month in Matomo',
    ['year', 'month']
)

def fetch_api_data(url, token, method, extra_params=None):
    """Helper function to make API requests to Matomo."""
    payload = {
        "module": "API",
        "format": "json",
        "method": method,
        "token_auth": token,
    }
    if extra_params:
        payload.update(extra_params)

    try:
        response = requests.post(url, params=payload, timeout=1000)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch {method}. HTTP status: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching {method}: {e}")
        return None

def set_metric(metric, value, labels=None):
    """Helper function to set Prometheus metric values."""
    if labels:
        metric.labels(**labels).set(value)
    else:
        metric.set(value)

def fetch_and_set_user_count(url, token):
    """Fetch total user count."""
    data = fetch_api_data(url, token, "UsersManager.getUsers")
    if data:
        set_metric(metrics['total_users'], len(data))
        print(f"Number of users: {len(data)}")

def fetch_and_set_non_excluded_users(url, token):
    """Fetch non-excluded users count based on email patterns."""
    data = fetch_api_data(url, token, "UsersManager.getUsers")
    if data:
        exclude_regex = re.compile('|'.join(exclude_patterns)) if exclude_patterns else re.compile(r'^$')
        filtered_users = [user for user in data if not exclude_regex.search(user.get('email', ''))]
        set_metric(metrics['non_excluded_users'], len(filtered_users))
        print(f"Number of non-excluded users: {len(filtered_users)}")

def fetch_and_set_admin_count(url, token):
    """Fetch super user count."""
    data = fetch_api_data(url, token, "UsersManager.getUsersHavingSuperUserAccess")
    if data:
        set_metric(metrics['admin_users'], len(data))
        print(f"Number of super users: {len(data)}")

def fetch_and_set_matomo_version(url, token):
    """Fetch Matomo version and expose it with additional labels for major, minor, and patch."""
    data = fetch_api_data(url, token, "API.getMatomoVersion")
    if data:
        version = data.get('value', 'unknown')

        # Initialize major, minor, and patch as 'unknown' by default
        major, minor, patch = 'unknown', 'unknown', 'unknown'

        # Extract major, minor, and patch version numbers using a regex pattern
        version_match = re.match(r'(\d+)\.(\d+)\.(\d+)', version)
        if version_match:
            major, minor, patch = version_match.groups()

        # Set the metric with full version and the parsed major, minor, patch as labels
        set_metric(metrics['matomo_version'], 1, labels={
            'full_version': version,
            'major': major,
            'minor': minor,
            'patch': patch
        })
        print(f"Matomo version: {version} (major: {major}, minor: {minor}, patch: {patch})")


def fetch_and_set_php_version(url, token):
    """Fetch PHP version and expose it with additional labels for major, minor, and patch."""
    data = fetch_api_data(url, token, "API.getPhpVersion")
    if data:
        php_version = data.get('version', 'unknown')

        # Initialize major, minor, and patch as 'unknown' by default
        major, minor, patch = 'unknown', 'unknown', 'unknown'

        # Extract major, minor, and patch version numbers using a regex pattern
        version_match = re.match(r'(\d+)\.(\d+)\.(\d+)', php_version)
        if version_match:
            major, minor, patch = version_match.groups()

        # Set the metric with full version and the parsed major, minor, patch as labels
        set_metric(metrics['php_version'], 1, labels={
            'full_version': php_version,
            'major': major,
            'minor': minor,
            'patch': patch
        })
        print(f"PHP version: {php_version} (major: {major}, minor: {minor}, patch: {patch})")


def fetch_and_set_segments_count(url, token):
    """Fetch number of segments."""
    data = fetch_api_data(url, token, "SegmentEditor.getAll")
    if data:
        set_metric(metrics['number_of_segments'], len(data))
        print(f"Number of segments: {len(data)}")

def fetch_and_set_sites_count(url, token):
    """Fetch number of sites."""
    data = fetch_api_data(url, token, "SitesManager.getAllSitesId")
    if data:
        set_metric(metrics['number_of_sites'], len(data))
        print(f"Number of sites: {len(data)}")

def fetch_and_set_matomo_actions(url, token, year):
    """Fetch Matomo actions for each month, with year and month as labels."""
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month

    # Loop through the years and months
    for year in range(actions_from_year, current_year + 1):
        for month in range(1, (12 if year < current_year else current_month) + 1):
            actions = fetch_api_data(
              url,
              token,
              "MultiSites.getAll",
              extra_params={"period": "month", "date": f"{year}-{month:02d}-01"}
            )

            if actions and isinstance(actions, list):
                # Sum up the 'nb_actions' for all sites
                total_actions = sum(site.get('nb_actions', 0) for site in actions)

                # Set the metric with 'year' and 'month' as labels (no new metric creation)
                matomo_actions_gauge.labels(year=str(year), month=f'{month:02d}').set(total_actions)
                print(f"Metric matomo_number_of_actions set to {total_actions} for {year}-{month:02d}")


def run_exporter():
    """Start the Prometheus exporter and fetch metrics periodically."""
    start_http_server(MATOMO_EXPORTER_PORT)
    print(f"Prometheus exporter started on port {MATOMO_EXPORTER_PORT}")

    while True:
        fetch_and_set_matomo_version(MATOMO_URL, MATOMO_TOKEN)
        fetch_and_set_php_version(MATOMO_URL, MATOMO_TOKEN)
        fetch_and_set_user_count(MATOMO_URL, MATOMO_TOKEN)
        fetch_and_set_non_excluded_users(MATOMO_URL, MATOMO_TOKEN)
        fetch_and_set_admin_count(MATOMO_URL, MATOMO_TOKEN)
        fetch_and_set_segments_count(MATOMO_URL, MATOMO_TOKEN)
        fetch_and_set_sites_count(MATOMO_URL, MATOMO_TOKEN)
        fetch_and_set_matomo_actions(MATOMO_URL, MATOMO_TOKEN, actions_from_year)

        time.sleep(update_metrics_seconds)

if __name__ == "__main__":
    run_exporter()
