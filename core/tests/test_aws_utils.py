# core/tests/test_aws_utils.py

from unittest.mock import patch, MagicMock
from core.aws_utils.storage import upload_file_to_s3, get_file_from_s3
from io import BytesIO


@patch("core.aws_utils.storage.s3_client")
def test_upload_file_to_s3(mock_s3_client):
    # Arrange
    mock_s3_client.upload_fileobj.return_value = None  # simulates success

    file_obj = BytesIO(b"dummy content")
    file_obj.name = "test.pdf"

    # Act
    url = upload_file_to_s3(file_obj, filename_prefix="test")

    # Assert
    assert url.startswith("https://")
    assert url.endswith(".pdf")
    mock_s3_client.upload_fileobj.assert_called_once()


@patch("core.aws_utils.storage.s3_client")
def test_get_file_from_s3(mock_s3_client):
    # Arrange
    mock_response = {"Body": BytesIO(b"hello world")}
    mock_s3_client.get_object.return_value = mock_response

    s3_key = "test/uuid123.pdf"

    # Act
    result = get_file_from_s3(s3_key)

    # Assert
    assert isinstance(result, BytesIO)
    assert result.read() == b"hello world"
    mock_s3_client.get_object.assert_called_once_with(
        Bucket="test-bucket", Key=s3_key
    )
