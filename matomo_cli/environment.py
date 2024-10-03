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
