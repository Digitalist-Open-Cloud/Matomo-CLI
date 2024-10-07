"""Prometheus Exporter for Matomo."""

import os
import re
import time
import datetime
import requests
from prometheus_client import start_http_server, Gauge, Info

# Matomo credentials and settings
MATOMO_URL = os.getenv("MATOMO_URL", "http://your-matomo-url")
MATOMO_TOKEN = os.getenv("MATOMO_TOKEN", "your-token")
MATOMO_EXPORTER_PORT = int(os.getenv("MATOMO_EXPORTER_PORT", "9110"))
UPDATE_INTERVAL = int(os.getenv("MATOMO_EXPORTER_UPDATE", "300"))
ACTIONS_FROM_YEAR = int(os.getenv("MATOMO_ACTIONS_FROM_YEAR", "2024"))
TRUST_SSL = os.getenv("MATOMO_TRUST_SSL_CERT", "")
EXTRA_API = os.getenv("MATOMO_EXTRA_API", "")

# Exclude users based on email patterns
EXCLUDE_USERS_ENV = os.getenv("MATOMO_EXCLUDE_USERS", "")
EXCLUDE_PATTERNS = [
    pattern.strip() for pattern in EXCLUDE_USERS_ENV.split(",") if pattern.strip()
]

# Prometheus metrics definition
metrics = {
    "total_users": Gauge("matomo_total_users", "Number of total users"),
    "non_excluded_users": Gauge(
        "matomo_total_non_excluded_users", "Number of non-excluded users"
    ),
    "admin_users": Gauge("matomo_super_users", "Number of super users"),
    "number_of_segments": Gauge("matomo_number_of_segments", "Number of segments"),
    "number_of_sites": Gauge("matomo_number_of_sites", "Number of sites"),
}

matomo_version_info = Info(
    "matomo_version", "Matomo version information (full version, major, minor, patch)"
)
php_version_info = Info(
    "matomo_php_version", "PHP version information (full version, major, minor, patch)"
)
matomo_actions_month_gauge = Gauge(
    "matomo_number_of_actions_month", "Actions per month", ["year", "month"]
)
todays_actions_gauge = Gauge("matomo_number_of_actions", "Actions recorded today")
archive_start_time_gauge = Gauge(
    "matomo_archive_start_time", "Timestamp when archiving started"
)
archive_finish_time_gauge = Gauge(
    "matomo_archive_finish_time", "Timestamp when archiving finished"
)
invalidations_total = Gauge("matomo_invalidations_total", "Total invalidations")
invalidations_queued = Gauge("matomo_invalidations_queued", "Queued invalidations")
invalidations_inprogress = Gauge(
    "matomo_invalidations_inprogress", "In-progress invalidations"
)


def fetch_api_data(url, token, method, extra_params=None):
    """Helper function to make API requests to Matomo."""
    payload = {"module": "API", "format": "json", "method": method, "token_auth": token}
    if extra_params:
        payload.update(extra_params)

    try:
        response = requests.post(
            url, params=payload, timeout=1000, verify=TRUST_SSL or True
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching {method}: {e}")
        return None


def set_metric(metric, value, labels=None):
    """Helper function to set Prometheus metric values."""
    if labels:
        metric.labels(**labels).set(value)
    else:
        metric.set(value)


def fetch_and_set_user_metrics(url, token):
    """Fetch total, non-excluded, and super user counts."""
    data = fetch_api_data(url, token, "UsersManager.getUsers")
    if data:
        set_metric(metrics["total_users"], len(data))
        exclude_regex = (
            re.compile("|".join(EXCLUDE_PATTERNS))
            if EXCLUDE_PATTERNS
            else re.compile(r"^$")
        )
        non_excluded_users = [
            user for user in data if not exclude_regex.search(user.get("email", ""))
        ]
        set_metric(metrics["non_excluded_users"], len(non_excluded_users))

    # Set super user count
    admin_data = fetch_api_data(
        url, token, "UsersManager.getUsersHavingSuperUserAccess"
    )
    if admin_data:
        set_metric(metrics["admin_users"], len(admin_data))


def fetch_and_set_version_info(url, token):
    """Fetch Matomo and PHP version information."""
    matomo_data = fetch_api_data(url, token, "API.getMatomoVersion")
    if matomo_data:
        version = matomo_data.get("value", "unknown")
        major, minor, patch = extract_version_parts(version)
        matomo_version_info.info(
            {"full_version": version, "major": major, "minor": minor, "patch": patch}
        )

    php_data = fetch_api_data(url, token, "API.getPhpVersion")
    if php_data:
        php_version = php_data.get("version", "unknown")
        major, minor, patch = extract_version_parts(php_version)
        php_version_info.info(
            {
                "full_version": php_version,
                "major": major,
                "minor": minor,
                "patch": patch,
            }
        )


def extract_version_parts(version):
    """Helper to extract major, minor, and patch from a version string."""
    match = re.match(r"(\d+)\.(\d+)\.(\d+)", version)
    return match.groups() if match else ("unknown", "unknown", "unknown")


def fetch_and_set_segments_and_sites(url, token):
    """Fetch the number of segments and sites."""
    segments_data = fetch_api_data(url, token, "SegmentEditor.getAll")
    if segments_data:
        set_metric(metrics["number_of_segments"], len(segments_data))

    sites_data = fetch_api_data(url, token, "SitesManager.getAllSitesId")
    if sites_data:
        set_metric(metrics["number_of_sites"], len(sites_data))


def fetch_and_set_matomo_actions_month(url, token):
    """Fetch actions for each month, with year and month as labels."""
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month

    for year in range(ACTIONS_FROM_YEAR, current_year + 1):
        for month in range(1, (12 if year < current_year else current_month) + 1):
            actions_data = fetch_api_data(
                url,
                token,
                "MultiSites.getAll",
                {"period": "month", "date": f"{year}-{month:02d}-01"},
            )
            if actions_data and isinstance(actions_data, list):
                total_actions = sum(site.get("nb_actions", 0) for site in actions_data)
                matomo_actions_month_gauge.labels(
                    year=str(year), month=f"{month:02d}"
                ).set(total_actions)


def fetch_todays_actions(url, token):
    """Fetch the number of actions for today."""
    actions_data = fetch_api_data(
        url, token, "MultiSites.getAll", {"period": "day", "date": "today"}
    )
    if actions_data and isinstance(actions_data, list):
        total_actions = sum(site.get("nb_actions", 0) for site in actions_data)
        todays_actions_gauge.set(total_actions)


def fetch_and_set_archive_times(url, token):
    """Fetch Matomo archive start and finish times."""
    archive_data = fetch_api_data(url, token, "ExtraApiInformation.getArchivingStatus")
    if archive_data:
        archive_start_time_gauge.set(int(archive_data.get("started", 0)))
        archive_finish_time_gauge.set(int(archive_data.get("finished", 0)))


def fetch_and_set_invalidations_status(url, token):
    """Fetch Matomo invalidations status."""
    invalidations_data = fetch_api_data(
        url, token, "ExtraApiInformation.getInvalidationsCount"
    )
    if invalidations_data:
        invalidations_total.set(int(invalidations_data.get("total", 0)))
        invalidations_queued.set(int(invalidations_data.get("queued", 0)))
        invalidations_inprogress.set(int(invalidations_data.get("inprogress", 0)))


def run_exporter():
    """Start the Prometheus exporter and periodically fetch metrics."""
    start_http_server(MATOMO_EXPORTER_PORT)
    print(f"Prometheus exporter started on port {MATOMO_EXPORTER_PORT}")

    while True:
        fetch_and_set_user_metrics(MATOMO_URL, MATOMO_TOKEN)
        fetch_and_set_version_info(MATOMO_URL, MATOMO_TOKEN)
        fetch_and_set_segments_and_sites(MATOMO_URL, MATOMO_TOKEN)
        fetch_todays_actions(MATOMO_URL, MATOMO_TOKEN)
        fetch_and_set_matomo_actions_month(MATOMO_URL, MATOMO_TOKEN)

        if EXTRA_API:
            fetch_and_set_archive_times(MATOMO_URL, MATOMO_TOKEN)
            fetch_and_set_invalidations_status(MATOMO_URL, MATOMO_TOKEN)

        time.sleep(UPDATE_INTERVAL)


if __name__ == "__main__":
    run_exporter()
