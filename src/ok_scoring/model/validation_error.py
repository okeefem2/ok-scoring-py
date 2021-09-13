class OKValidationError(Exception):
    def __init__(self, propertyPath, errorType, errorMessage):
        # Call the base class constructor with the parameters it needs
        super().__init__(f'{propertyPath} invalid: {errorMessage}')

        # Errors will be a dict with more detailed information about the error
        self.errors = {'path': propertyPath, 'errorType': errorType, 'errorMessage': errorMessage}

