from enum import Enum
from typing import List

class FileFormat(Enum):
    """
    Enumeration class representing common file formats.

    Attributes:
        PDF: Portable Document Format
        DOCX: Microsoft Word Document
        PPTX: Microsoft PowerPoint Presentation
        TXT: Plain Text File

    Example:
        >>> format = FileFormat.PDF
        >>> print(format)
        FileFormat.PDF
        >>> print(format.value)
        'PDF'
    """

    PDF = "PDF"
    DOCX = "DOCX"
    PPTX = "PPTX"
    TXT = "TXT"

    @classmethod
    def list_formats(cls) -> List[str]:
        """
        Returns a list of all available file format values.

        Returns:
            List[str]: List of file format string values
        """
        return [format.value for format in cls]

    def __str__(self) -> str:
        """
        Returns the string representation of the file format.

        Returns:
            str: The file format value
        """
        return self.value