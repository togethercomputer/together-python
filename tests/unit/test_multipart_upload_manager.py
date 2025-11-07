import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

from together.filemanager import MultipartUploadManager
from together.constants import (
    MIN_PART_SIZE_MB,
    TARGET_PART_SIZE_MB,
    MAX_MULTIPART_PARTS,
    MULTIPART_UPLOAD_TIMEOUT,
    MAX_FILE_SIZE_GB,
    NUM_BYTES_IN_GB,
)
from together.types import FilePurpose, FileResponse
from together.types.common import ObjectType
from together.together_response import TogetherResponse
from together.error import FileTypeError, ResponseError


class TestMultipartUploadManager:
    """Test suite for MultipartUploadManager class"""

    @pytest.fixture
    def mock_client(self):
        """Create a mock TogetherClient"""
        return Mock()

    @pytest.fixture
    def manager(self, mock_client):
        """Create a MultipartUploadManager instance with mock client"""
        return MultipartUploadManager(mock_client)

    def test_init(self, mock_client):
        """Test MultipartUploadManager initialization"""
        manager = MultipartUploadManager(mock_client)
        assert manager._client == mock_client
        assert manager.max_concurrent_parts == 4

    def test_get_file_type_jsonl(self, manager):
        """Test file type detection for .jsonl files"""
        file = Path("test.jsonl")
        assert manager._get_file_type(file) == "jsonl"

    def test_get_file_type_parquet(self, manager):
        """Test file type detection for .parquet files"""
        file = Path("test.parquet")
        assert manager._get_file_type(file) == "parquet"

    def test_get_file_type_csv(self, manager):
        """Test file type detection for .csv files"""
        file = Path("test.csv")
        assert manager._get_file_type(file) == "csv"

    def test_get_file_type_unknown_raises_error(self, manager):
        """Test that unknown file types raise ValueError"""
        file = Path("test.txt")
        with pytest.raises(ValueError) as exc_info:
            manager._get_file_type(file)

        error_message = str(exc_info.value)
        assert "Unsupported file extension: '.txt'" in error_message
        assert "Supported extensions: .jsonl, .parquet, .csv" in error_message

    def test_calculate_parts_small_file(self, manager):
        """Test part calculation for files smaller than target part size"""
        file_size = 50 * 1024 * 1024  # 50MB
        part_size, num_parts = manager._calculate_parts(file_size)

        assert num_parts == 1
        assert part_size == file_size

    def test_calculate_parts_medium_file(self, manager):
        """Test part calculation for medium-sized files"""
        file_size = 500 * 1024 * 1024  # 500MB
        part_size, num_parts = manager._calculate_parts(file_size)

        expected_parts = 2  # 500MB / 250MB = 2 parts
        expected_part_size = 250 * 1024 * 1024  # 250MB

        assert num_parts == expected_parts
        assert part_size == expected_part_size

    def test_calculate_parts_large_file(self, manager):
        """Test part calculation for large files that require scaling"""
        file_size = 50 * 1024 * 1024 * 1024  # 50GB
        part_size, num_parts = manager._calculate_parts(file_size)

        # With 250MB target part size, 50GB should use ~205 parts
        expected_parts = 205  # 50GB / 250MB ≈ 205 parts
        assert num_parts == expected_parts
        # Part size should be close to target (within rounding)
        assert part_size >= 249 * 1024 * 1024  # At least 249MB (allowing for rounding)

    def test_calculate_parts_respects_minimum_part_size(self, manager):
        """Test that minimum part size is respected"""
        # Create a scenario where calculated part size would be too small
        file_size = 1000 * 1024 * 1024  # 1GB

        with patch.object(
            manager, "_calculate_parts", wraps=manager._calculate_parts
        ) as mock_calc:
            part_size, num_parts = manager._calculate_parts(file_size)

            # Ensure no part is smaller than minimum
            min_part_size = MIN_PART_SIZE_MB * 1024 * 1024
            assert part_size >= min_part_size

    @patch("together.filemanager.api_requestor.APIRequestor")
    def test_initiate_upload_success(self, mock_requestor_class, manager):
        """Test successful upload initiation"""
        # Setup mock
        mock_requestor = Mock()
        mock_requestor_class.return_value = mock_requestor

        mock_response = TogetherResponse(
            data={
                "upload_id": "test-upload-id",
                "file_id": "test-file-id",
                "parts": [
                    {
                        "part_number": 1,
                        "url": "https://presigned-url-1.com",
                        "headers": {"Authorization": "Bearer token"},
                    }
                ],
            },
            headers={},
        )
        mock_requestor.request.return_value = (mock_response, None, None)

        # Test
        result = manager._initiate_upload(
            "test-url",
            Path("test.jsonl"),
            1024 * 1024,  # 1MB
            1,
            FilePurpose.FineTune,
            "jsonl",
        )

        # Assertions
        assert result["upload_id"] == "test-upload-id"
        assert result["file_id"] == "test-file-id"
        assert len(result["parts"]) == 1

        # Verify API call
        mock_requestor.request.assert_called_once()
        call_args = mock_requestor.request.call_args[1]["options"]
        assert call_args.method == "POST"
        assert call_args.url == "files/multipart/initiate"

    @patch("together.filemanager.requests.put")
    def test_upload_single_part_success(self, mock_put, manager):
        """Test successful single part upload"""
        # Setup mock response
        mock_response = Mock()
        mock_response.headers = {"ETag": '"test-etag"'}
        mock_response.raise_for_status = Mock()
        mock_put.return_value = mock_response

        # Test data
        part_info = {
            "PartNumber": 1,
            "URL": "https://presigned-url.com",
            "Headers": {"Authorization": "Bearer token"},
        }
        part_data = b"test data"

        # Test
        etag = manager._upload_single_part(part_info, part_data)

        # Assertions
        assert etag == "test-etag"
        mock_put.assert_called_once_with(
            "https://presigned-url.com",
            data=part_data,
            headers={"Authorization": "Bearer token"},
            timeout=MULTIPART_UPLOAD_TIMEOUT,
        )
        mock_response.raise_for_status.assert_called_once()

    @patch("together.filemanager.requests.put")
    def test_upload_single_part_no_etag_error(self, mock_put, manager):
        """Test error when no ETag is returned"""
        # Setup mock response without ETag
        mock_response = Mock()
        mock_response.headers = {}
        mock_response.raise_for_status = Mock()
        mock_put.return_value = mock_response

        part_info = {"PartNumber": 1, "URL": "https://test.com", "Headers": {}}
        part_data = b"test data"

        # Test
        with pytest.raises(ResponseError, match="No ETag returned for part 1"):
            manager._upload_single_part(part_info, part_data)

    @patch("together.filemanager.api_requestor.APIRequestor")
    def test_complete_upload_success(self, mock_requestor_class, manager):
        """Test successful upload completion"""
        # Setup mock
        mock_requestor = Mock()
        mock_requestor_class.return_value = mock_requestor

        mock_response = TogetherResponse(
            data={
                "file": {
                    "id": "test-file-id",
                    "object": "file",
                    "filename": "test.jsonl",
                    "bytes": 1024,
                    "purpose": "fine-tune",
                }
            },
            headers={},
        )
        mock_requestor.request.return_value = (mock_response, None, None)

        # Test
        completed_parts = [{"part_number": 1, "etag": "test-etag"}]
        result = manager._complete_upload(
            "test-url", "upload-id", "file-id", completed_parts
        )

        # Assertions
        assert isinstance(result, FileResponse)
        assert result.id == "test-file-id"
        assert result.filename == "test.jsonl"

        # Verify API call
        mock_requestor.request.assert_called_once()
        call_args = mock_requestor.request.call_args[1]["options"]
        assert call_args.method == "POST"
        assert call_args.url == "files/multipart/complete"

    @patch("together.filemanager.api_requestor.APIRequestor")
    def test_abort_upload_success(self, mock_requestor_class, manager):
        """Test successful upload abort"""
        # Setup mock
        mock_requestor = Mock()
        mock_requestor_class.return_value = mock_requestor
        mock_requestor.request.return_value = (Mock(), None, None)

        # Test
        manager._abort_upload("test-url", "upload-id", "file-id")

        # Verify API call
        mock_requestor.request.assert_called_once()
        call_args = mock_requestor.request.call_args[1]["options"]
        assert call_args.method == "POST"
        assert call_args.url == "files/multipart/abort"
        assert call_args.params["upload_id"] == "upload-id"
        assert call_args.params["file_id"] == "file-id"

    @patch("together.filemanager.ThreadPoolExecutor")
    @patch("together.filemanager.open", create=True)
    def test_upload_parts_concurrent(self, mock_open, mock_executor_class, manager):
        """Test concurrent part upload functionality"""
        # Setup mocks
        mock_file = Mock()
        mock_file.seek = Mock()
        mock_file.read.return_value = b"test data"
        mock_open.return_value.__enter__.return_value = mock_file

        mock_executor = Mock()
        mock_executor_class.return_value.__enter__.return_value = mock_executor

        # Mock futures
        mock_future1 = Mock()
        mock_future1.result.return_value = "etag1"
        mock_future2 = Mock()
        mock_future2.result.return_value = "etag2"

        mock_executor.submit.side_effect = [mock_future1, mock_future2]

        # Mock as_completed
        with patch(
            "together.filemanager.as_completed",
            return_value=[mock_future1, mock_future2],
        ):
            upload_info = {
                "parts": [
                    {"PartNumber": 1, "URL": "url1", "Headers": {}},
                    {"PartNumber": 2, "URL": "url2", "Headers": {}},
                ]
            }

            # Test
            result = manager._upload_parts_concurrent(
                Path("test.jsonl"), upload_info, 1024
            )

            # Assertions
            assert len(result) == 2
            assert result[0]["part_number"] == 1
            assert result[0]["etag"] == "etag1"
            assert result[1]["part_number"] == 2
            assert result[1]["etag"] == "etag2"

            # Verify executor was used
            assert mock_executor.submit.call_count == 2

    @patch("together.filemanager.os.stat")
    def test_file_size_exceeds_limit_raises_error(self, mock_stat, manager):
        """Test that files exceeding size limit raise FileTypeError with clear message"""
        # Setup - file size over limit
        file_size = int((MAX_FILE_SIZE_GB + 1) * NUM_BYTES_IN_GB)  # 51.1GB
        mock_stat.return_value.st_size = file_size

        # Should raise FileTypeError with descriptive message
        with pytest.raises(FileTypeError) as exc_info:
            manager.upload("test-url", Path("test.jsonl"), FilePurpose.FineTune)

        error_message = str(exc_info.value)
        assert "51.1GB exceeds maximum supported size of 50.1GB" in error_message

    @patch.object(MultipartUploadManager, "_initiate_upload")
    @patch.object(MultipartUploadManager, "_upload_parts_concurrent")
    @patch.object(MultipartUploadManager, "_complete_upload")
    @patch.object(MultipartUploadManager, "_abort_upload")
    @patch("together.filemanager.os.stat")
    def test_upload_success_flow(
        self,
        mock_stat,
        mock_abort,
        mock_complete,
        mock_upload_parts,
        mock_initiate,
        manager,
    ):
        """Test successful complete upload flow"""
        # Setup mocks
        mock_stat.return_value.st_size = 200 * 1024 * 1024  # 200MB

        mock_initiate.return_value = {
            "upload_id": "test-upload",
            "file_id": "test-file",
            "parts": [{"part_number": 1}],
        }

        mock_upload_parts.return_value = [{"part_number": 1, "etag": "etag1"}]

        expected_response = FileResponse(
            id="test-file",
            object=ObjectType.File,
            filename="test.jsonl",
            bytes=200 * 1024 * 1024,
            purpose=FilePurpose.FineTune,
        )
        mock_complete.return_value = expected_response

        # Test
        result = manager.upload("test-url", Path("test.jsonl"), FilePurpose.FineTune)

        # Assertions
        assert result == expected_response
        mock_initiate.assert_called_once()
        mock_upload_parts.assert_called_once()
        mock_complete.assert_called_once()
        mock_abort.assert_not_called()

    @patch.object(MultipartUploadManager, "_initiate_upload")
    @patch.object(MultipartUploadManager, "_upload_parts_concurrent")
    @patch.object(MultipartUploadManager, "_abort_upload")
    @patch("together.filemanager.os.stat")
    def test_upload_failure_calls_abort(
        self, mock_stat, mock_abort, mock_upload_parts, mock_initiate, manager
    ):
        """Test that abort is called when upload fails"""
        # Setup mocks
        mock_stat.return_value.st_size = 200 * 1024 * 1024  # 200MB

        mock_initiate.return_value = {
            "upload_id": "test-upload",
            "file_id": "test-file",
            "parts": [{"part_number": 1}],
        }

        # Make upload parts fail
        mock_upload_parts.side_effect = Exception("Upload failed")

        # Test
        with pytest.raises(Exception, match="Upload failed"):
            manager.upload("test-url", Path("test.jsonl"), FilePurpose.FineTune)

        # Verify abort was called for cleanup
        mock_abort.assert_called_once_with("test-url", "test-upload", "test-file")
