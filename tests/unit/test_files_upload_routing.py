import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

from together.resources.files import Files
from together.types import FilePurpose, FileResponse
from together.types.common import ObjectType
from together.constants import MULTIPART_THRESHOLD_GB, NUM_BYTES_IN_GB


class TestFilesUploadRouting:
    """Test suite for Files.upload() size-based routing logic"""

    @pytest.fixture
    def mock_client(self):
        """Create a mock TogetherClient"""
        return Mock()

    @pytest.fixture
    def files_resource(self, mock_client):
        """Create a Files resource instance with mock client"""
        return Files(mock_client)

    @pytest.fixture
    def mock_file_response(self):
        """Create a mock FileResponse for testing"""
        return FileResponse(
            id="test-file-id",
            object=ObjectType.File,
            filename="test.jsonl",
            bytes=1024 * 1024,  # 1MB
            purpose=FilePurpose.FineTune,
        )

    @patch("together.resources.files.check_file")
    @patch("together.resources.files.os.stat")
    @patch("together.resources.files.UploadManager")
    def test_small_file_uses_single_upload(
        self,
        mock_upload_manager_class,
        mock_stat,
        mock_check_file,
        files_resource,
        mock_file_response,
    ):
        """Test that files under 5GB use single-part upload"""
        # Setup - file size under threshold
        file_size = 3 * NUM_BYTES_IN_GB  # 3GB
        mock_stat.return_value.st_size = file_size

        # Mock file validation
        mock_check_file.return_value = {"is_check_passed": True}

        # Mock upload manager
        mock_upload_manager = Mock()
        mock_upload_manager.upload.return_value = mock_file_response
        mock_upload_manager_class.return_value = mock_upload_manager

        # Test
        result = files_resource.upload(Path("test.jsonl"), purpose=FilePurpose.FineTune)

        # Assertions
        assert result == mock_file_response

        # Verify single-part upload was used
        mock_upload_manager_class.assert_called_once_with(files_resource._client)
        mock_upload_manager.upload.assert_called_once_with(
            "files", Path("test.jsonl"), purpose=FilePurpose.FineTune, redirect=True
        )

    @patch("together.resources.files.check_file")
    @patch("together.resources.files.os.stat")
    @patch("together.resources.files.MultipartUploadManager")
    def test_large_file_uses_multipart_upload(
        self,
        mock_multipart_manager_class,
        mock_stat,
        mock_check_file,
        files_resource,
        mock_file_response,
    ):
        """Test that files over 5GB use multipart upload"""
        # Setup - file size over threshold
        file_size = 10 * NUM_BYTES_IN_GB  # 10GB
        mock_stat.return_value.st_size = file_size

        # Mock file validation
        mock_check_file.return_value = {"is_check_passed": True}

        # Mock multipart upload manager
        mock_multipart_manager = Mock()
        mock_multipart_manager.upload.return_value = mock_file_response
        mock_multipart_manager_class.return_value = mock_multipart_manager

        # Test
        result = files_resource.upload(Path("test.jsonl"), purpose=FilePurpose.FineTune)

        # Assertions
        assert result == mock_file_response

        # Verify multipart upload was used
        mock_multipart_manager_class.assert_called_once_with(files_resource._client)
        mock_multipart_manager.upload.assert_called_once_with(
            "files", Path("test.jsonl"), FilePurpose.FineTune
        )

    @patch("together.resources.files.check_file")
    @patch("together.resources.files.os.stat")
    @patch("together.resources.files.UploadManager")
    def test_threshold_boundary_exactly_5gb(
        self,
        mock_upload_manager_class,
        mock_stat,
        mock_check_file,
        files_resource,
        mock_file_response,
    ):
        """Test routing behavior at exactly the 5GB threshold"""
        # Setup - file size exactly at threshold
        file_size = MULTIPART_THRESHOLD_GB * NUM_BYTES_IN_GB  # Exactly 5GB
        mock_stat.return_value.st_size = file_size

        # Mock file validation
        mock_check_file.return_value = {"is_check_passed": True}

        # Mock upload manager
        mock_upload_manager = Mock()
        mock_upload_manager.upload.return_value = mock_file_response
        mock_upload_manager_class.return_value = mock_upload_manager

        # Test
        result = files_resource.upload(Path("test.jsonl"), purpose=FilePurpose.FineTune)

        # Assertions - exactly at threshold should use single upload
        assert result == mock_file_response
        mock_upload_manager_class.assert_called_once()

    @patch("together.resources.files.check_file")
    @patch("together.resources.files.os.stat")
    @patch("together.resources.files.MultipartUploadManager")
    def test_just_over_threshold_uses_multipart(
        self,
        mock_multipart_manager_class,
        mock_stat,
        mock_check_file,
        files_resource,
        mock_file_response,
    ):
        """Test that files just over 5GB use multipart upload"""
        # Setup - file size just over threshold
        file_size = int((MULTIPART_THRESHOLD_GB + 0.1) * NUM_BYTES_IN_GB)  # 5.1GB
        mock_stat.return_value.st_size = file_size

        # Mock file validation
        mock_check_file.return_value = {"is_check_passed": True}

        # Mock multipart upload manager
        mock_multipart_manager = Mock()
        mock_multipart_manager.upload.return_value = mock_file_response
        mock_multipart_manager_class.return_value = mock_multipart_manager

        # Test
        result = files_resource.upload(Path("test.jsonl"), purpose=FilePurpose.FineTune)

        # Assertions - just over threshold should use multipart
        assert result == mock_file_response
        mock_multipart_manager_class.assert_called_once()

    @patch("together.resources.files.check_file")
    @patch("together.resources.files.os.stat")
    def test_file_validation_still_works(
        self, mock_stat, mock_check_file, files_resource
    ):
        """Test that file validation is still performed regardless of routing"""
        # Setup - invalid file
        file_size = 1 * NUM_BYTES_IN_GB  # 1GB (small file)
        mock_stat.return_value.st_size = file_size

        # Mock file validation failure
        mock_check_file.return_value = {
            "is_check_passed": False,
            "message": "Invalid file format",
        }

        # Test - should raise FileTypeError
        from together.error import FileTypeError

        with pytest.raises(FileTypeError, match="Invalid file format"):
            files_resource.upload(
                Path("test.jsonl"), purpose=FilePurpose.FineTune, check=True
            )

        # Verify validation was called
        mock_check_file.assert_called_once()

    @patch("together.resources.files.check_file")
    @patch("together.resources.files.os.stat")
    @patch("together.resources.files.UploadManager")
    def test_check_disabled_skips_validation(
        self,
        mock_upload_manager_class,
        mock_stat,
        mock_check_file,
        files_resource,
        mock_file_response,
    ):
        """Test that check=False skips file validation"""
        # Setup
        file_size = 1 * NUM_BYTES_IN_GB  # 1GB
        mock_stat.return_value.st_size = file_size

        # Mock upload manager
        mock_upload_manager = Mock()
        mock_upload_manager.upload.return_value = mock_file_response
        mock_upload_manager_class.return_value = mock_upload_manager

        # Test with check=False
        result = files_resource.upload(
            Path("test.jsonl"), purpose=FilePurpose.FineTune, check=False
        )

        # Assertions
        assert result == mock_file_response
        # Verify validation was NOT called
        mock_check_file.assert_not_called()

    @patch("together.resources.files.check_file")
    @patch("together.resources.files.os.stat")
    @patch("together.resources.files.UploadManager")
    def test_eval_purpose_skips_validation(
        self,
        mock_upload_manager_class,
        mock_stat,
        mock_check_file,
        files_resource,
        mock_file_response,
    ):
        """Test that non-FineTune purposes skip validation"""
        # Setup
        file_size = 1 * NUM_BYTES_IN_GB  # 1GB
        mock_stat.return_value.st_size = file_size

        # Mock upload manager
        mock_upload_manager = Mock()
        mock_upload_manager.upload.return_value = mock_file_response
        mock_upload_manager_class.return_value = mock_upload_manager

        # Test with Eval purpose
        result = files_resource.upload(
            Path("test.csv"), purpose=FilePurpose.Eval, check=True
        )

        # Assertions
        assert result == mock_file_response
        # Verify validation was NOT called (only FineTune purpose gets validated)
        mock_check_file.assert_not_called()

    @patch("together.resources.files.check_file")
    @patch("together.resources.files.os.stat")
    @patch("together.resources.files.MultipartUploadManager")
    def test_string_path_converted_to_path(
        self,
        mock_multipart_manager_class,
        mock_stat,
        mock_check_file,
        files_resource,
        mock_file_response,
    ):
        """Test that string file paths are converted to Path objects"""
        # Setup
        file_size = 10 * NUM_BYTES_IN_GB  # 10GB
        mock_stat.return_value.st_size = file_size

        # Mock file validation
        mock_check_file.return_value = {"is_check_passed": True}

        # Mock multipart upload manager
        mock_multipart_manager = Mock()
        mock_multipart_manager.upload.return_value = mock_file_response
        mock_multipart_manager_class.return_value = mock_multipart_manager

        # Test with string path
        result = files_resource.upload("test.jsonl", purpose=FilePurpose.FineTune)

        # Assertions
        assert result == mock_file_response

        # Verify Path object was passed to upload manager
        call_args = mock_multipart_manager.upload.call_args[0]
        assert isinstance(call_args[1], Path)
        assert str(call_args[1]) == "test.jsonl"

    @patch("together.resources.files.check_file")
    @patch("together.resources.files.os.stat")
    @patch("together.resources.files.UploadManager")
    def test_string_purpose_converted_to_enum(
        self,
        mock_upload_manager_class,
        mock_stat,
        mock_check_file,
        files_resource,
        mock_file_response,
    ):
        """Test that string purposes are converted to FilePurpose enum"""
        # Setup
        file_size = 1 * NUM_BYTES_IN_GB  # 1GB
        mock_stat.return_value.st_size = file_size

        # Mock file validation
        mock_check_file.return_value = {"is_check_passed": True}

        # Mock upload manager
        mock_upload_manager = Mock()
        mock_upload_manager.upload.return_value = mock_file_response
        mock_upload_manager_class.return_value = mock_upload_manager

        # Test with string purpose
        result = files_resource.upload(Path("test.jsonl"), purpose="fine-tune")

        # Assertions
        assert result == mock_file_response

        # Verify FilePurpose enum was passed to upload manager
        call_args = mock_upload_manager.upload.call_args[1]
        assert call_args["purpose"] == FilePurpose.FineTune
