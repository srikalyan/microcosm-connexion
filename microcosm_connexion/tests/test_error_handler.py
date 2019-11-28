from hamcrest import assert_that, equal_to, is_
from mock import Mock, patch

from microcosm_connexion.error_handler import ConnexionErrorHandler


class TestConnexionErrorHandler(object):
    def setup(self):
        self.handler = ConnexionErrorHandler()

    def test_extract_title(self):
        error = Mock()

        assert_that(self.handler.extract_title(error), is_(equal_to(type(error).__name__)))

    @patch("microcosm_connexion.error_handler.type")
    def test_extract_title_unknown(self, mock_type):
        error = Mock()
        mock_type.side_effect = Exception("Some thing unknown!")

        assert_that(self.handler.extract_title(error), is_(equal_to("Unknown!")))

        mock_type.assert_called_once_with(error)

    @patch("microcosm_connexion.error_handler.extract_status_code")
    @patch("microcosm_connexion.error_handler.extract_error_message")
    @patch("microcosm_connexion.error_handler.dump_response_data")
    def test_handle(self, mock_dump_response_data, mock_extract_error_message, mock_extract_status_code):
        error = Mock()

        with patch.object(self.handler, "extract_title") as mock_extract_title:
            with patch.object(self.handler, "logger") as mock_logger:
                mock_extract_status_code.return_value = 400

                assert_that(self.handler.handle(error), is_(equal_to(mock_dump_response_data.return_value)))
                mock_logger.exception.assert_not_called()

                response_data = {
                    "status": mock_extract_status_code.return_value,
                    "title": mock_extract_title.return_value,
                    "detail": mock_extract_error_message.return_value,
                    "type": "about:blank",
                }

                mock_dump_response_data.assert_called_once_with(None, response_data,
                                                                mock_extract_status_code.return_value)
                mock_extract_title.assert_called_once_with(error)
                mock_extract_status_code.assert_called_once_with(error)
                mock_extract_error_message.assert_called_once_with(error)

    @patch("microcosm_connexion.error_handler.extract_status_code")
    @patch("microcosm_connexion.error_handler.extract_error_message")
    @patch("microcosm_connexion.error_handler.dump_response_data")
    def test_handle_stack_trace(self, mock_dump_response_data, mock_extract_error_message, mock_extract_status_code):
        error = Mock()

        with patch.object(self.handler, "extract_title") as mock_extract_title:
            with patch.object(self.handler, "logger") as mock_logger:
                mock_extract_status_code.return_value = 500

                assert_that(self.handler.handle(error), is_(equal_to(mock_dump_response_data.return_value)))
                mock_logger.exception.assert_called_once()

                response_data = {
                    "status": mock_extract_status_code.return_value,
                    "title": mock_extract_title.return_value,
                    "detail": mock_extract_error_message.return_value,
                    "type": "about:blank",
                }

                mock_dump_response_data.assert_called_once_with(None, response_data,
                                                                mock_extract_status_code.return_value)
                mock_extract_title.assert_called_once_with(error)
                mock_extract_status_code.assert_called_once_with(error)
                mock_extract_error_message.assert_called_once_with(error)
