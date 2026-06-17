from unittest.mock import MagicMock, patch

from src.services.users.repository.user_repository import create_user


@patch("src.services.users.repository.user_repository.get_connection")
def test_create_user(mock_connection):

    conn = MagicMock()
    cursor = MagicMock()

    conn.cursor.return_value.__enter__.return_value = cursor

    mock_connection.return_value = conn

    create_user(
        "123",
        "kumar",
        "kumar@gmail.com"
    )

    cursor.execute.assert_called_once()