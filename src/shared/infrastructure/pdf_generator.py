from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class PDFDocument:
    title: str
    content: Dict[str, Any]
    output_path: str


class IPDFGenerator(ABC):
    @abstractmethod
    def generate(self, document: PDFDocument) -> str:
        pass
