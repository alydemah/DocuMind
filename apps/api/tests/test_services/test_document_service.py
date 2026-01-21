import tempfile
from pathlib import Path

import pytest

from app.services.document_service import DocumentService


class TestDocumentValidation:
    def test_validate_valid_pdf(self):
        valid, msg = DocumentService.validate_file("test.pdf", 1024 * 1024)
        assert valid is True
        assert msg == ""

    def test_validate_invalid_extension(self):
        valid, msg = DocumentService.validate_file("test.exe", 1024)
        assert valid is False
        assert "not supported" in msg

    def test_validate_file_too_large(self):
        valid, msg = DocumentService.validate_file("test.pdf", 100 * 1024 * 1024)
        assert valid is False
        assert "exceeds" in msg

    def test_compute_file_hash(self):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"test content")
            f.flush()
            hash1 = DocumentService.compute_file_hash(Path(f.name))
            hash2 = DocumentService.compute_file_hash(Path(f.name))

        assert hash1 == hash2
        assert len(hash1) == 64
