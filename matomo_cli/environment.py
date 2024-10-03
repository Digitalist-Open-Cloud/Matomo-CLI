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


"""Module checking environment variable."""

from os import environ

class Environment:
    """Define environment."""

    def __init__(self):
        self.url = environ.get('MATOMO_URL')
        self.token = environ.get('MATOMO_TOKEN')

    def check_environment_status(self):
        """Check existent status of environment variables."""
        error_string = self.check_environment()

        if len(error_string) > 0:
            raise ValueError(error_string)

        print('MATOMO_URL: ', self.url)
        print('MATOMO_TOKEN: ', self.token)

    def check_environment(self):
        """Check existent of environment variables."""
        error_string = ''
        if self.url is None:
            error_string = 'MATOMO_URL is missing'
        if self.token is None:
            if error_string != '':
                error_string = error_string + ' / '
            error_string = error_string + 'MATOMO_TOKEN is missing'

        return error_string
