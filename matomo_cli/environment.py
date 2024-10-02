from os import environ

class Environment:

    def __init__(self):
        self.url = environ.get('MATOMO_URL')
        self.token = environ.get('MATOMO_TOKEN')

    def check_environment_status(self):
        error_string = self.check_environment()

        if len(error_string) > 0:
          raise Exception(error_string)

        print('MATOMO_URL: ', self.url)
        print('MATOMO_TOKEN: ', self.token)


    def check_environment(self):
        error_string = ''
        if self.url is None:
            error_string = 'MATOMO_URL is missing'
        if self.token is None:
            if error_string != '':
                error_string = error_string + ' / '
            error_string = error_string + 'MATOMO_TOKEN is missing'

        return error_string