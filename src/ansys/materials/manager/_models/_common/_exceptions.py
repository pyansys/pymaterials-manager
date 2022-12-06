class ModelValidationException(Exception):
    """
    Exception thrown if pre-flight verification fails.

    This indicates that the provided model state is invalid.
    """

    def __init__(self, message: str):
        """
        Create an instance of ModelValidationException.

        Parameters
        ----------
        message: str
            Exception text
        """
        super().__init__(message)
