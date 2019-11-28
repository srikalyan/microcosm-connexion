from microcosm_flask.conventions.encoding import dump_response_data
from microcosm_flask.errors import extract_error_message, extract_status_code
from microcosm_logging.decorators import logger


@logger
class ConnexionErrorHandler(object):

    def extract_title(self, error):
        """
        Extracts class name of the error
        :param error: Error from which class name needs to be extracted
        :return: String representing the error's class name or "Unknown"
        """
        try:
            return type(error).__name__
        except Exception:
            self.logger.debug("error '{}' has no type".format(error))
            return "Unknown!"

    def handle(self, error):
        """
        Generates a response that follows connexion's error format i.e.,

        "status": http status code,
        "title": Short description,
        "detail": "detail message",
        "type": "An absolute URI that identifies the problem type.
          When dereferenced, it SHOULD provide human-readable documentation for the problem type"

        Note: Heavily inspired by the microcosm_flask.errors module just needed a different format
        """
        status = extract_status_code(error)
        title = self.extract_title(error)
        detail = extract_error_message(error)
        type_name = "about:blank"

        # To make sure that we have some stack trace for 500+ errors
        if status >= 500:
            self.logger.exception(error)

        self.logger.debug("Handling error {} with status {}, title {}, detail {}, type_name {}".format(
            error,
            status,
            title,
            detail,
            type_name,
        ))

        response_data = {
            "status": status,
            "title": title,
            "detail": detail,
            "type": type_name,
        }

        return dump_response_data(None, response_data, status)
