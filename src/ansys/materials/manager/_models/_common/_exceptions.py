class ModelValidationException(Exception):
    """
    Provides the exception thrown if pre-flight verification fails.

    Throwing an exception indicates that the provided model state is invalid.
    """

    def __init__(self, message: str):
        """
        Create an instance of the ``ModelValidationException`` class.

        Parameters
        ----------
        message: str
            Text to display for the exception.
        """
        super().__init__(message)
