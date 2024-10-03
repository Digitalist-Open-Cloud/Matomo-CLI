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

"""Module creating the main cli app."""
import rich_click as click
from .api import api
from .metrics import metrics


@click.group()
def cli():
    """Simple and basic CLI tool for Matomo"""

cli.add_command(api)
cli.add_command(metrics)

if __name__ == "__main__":
    cli()
