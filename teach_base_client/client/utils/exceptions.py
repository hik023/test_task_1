class BadAPIAccess(Exception):
    '''Exception raised for errors in auth endpoint connection.

    Attributes:
        status -- Http status of error
        endpoint -- API endpoint which causes error
    '''

    def __init__(self, status, endpoint, message):
        self.message = f'{status} | {endpoint}<br>'\
            f'Response:<br>{message}'
        super().__init__(self.message)