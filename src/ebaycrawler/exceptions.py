class UnknownFileFormatException(Exception):
    """Exception that is called when an unknown file format is provided."""
    def __init__(self, file_format: str) -> None:
        super().__init__((file_format,))
        self.file_format = file_format
