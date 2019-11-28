import connexion

from microcosm.config.validation import typed
from microcosm.decorators import defaults
from microcosm.hooks import invoke_resolve_hook
from microcosm_flask.session import register_session_factory
from werkzeug.exceptions import default_exceptions

from microcosm_connexion.error_handler import ConnexionErrorHandler


@defaults(
    host="0.0.0.0",
    port=typed(type=int, default_value=5000),
    enable_swagger_ui=typed(type=bool, default_value=True),
)
def configure_connexion(graph):
    """
    Creates and configures connexion's app instance
    :param graph: Instance of microcosm graph
    :return: connexion instance
    """
    options = {"swagger_ui": graph.config.connexion.enable_swagger_ui}

    connexion_app = connexion.App(graph.metadata.import_name,
                                  host=graph.config.connexion.host,
                                  port=graph.config.connexion.port,
                                  debug=graph.metadata.debug,
                                  options=options)

    app = connexion_app.app
    app.debug = graph.metadata.debug
    app.testing = graph.metadata.testing

    invoke_resolve_hook(app)

    graph.assign("flask", app)
    graph.assign("app", app)

    return connexion_app


@defaults(
    db_key="db",
)
def configure_postgres_session_factory(graph):
    """
    Binds the Postgres SQLAlchemy session context to Flask.
    :param graph: Instance of microcosm graph
    """
    from microcosm_postgres.context import SessionContext

    return register_session_factory(graph, graph.config.postgres_session_factory.db_key, SessionContext.make)


def connexion_error_handler(graph):
    """
    Creates a connexion error handler instance
    :param graph: Instance of microcosm graph
    :return: ConnexionErrorHandler instance
    """
    return ConnexionErrorHandler()


def configure_connexion_error_handler(graph):
    """
    Registers connexion error handler to various standard errors

    Note: Note: Heavily inspired by the microcosm_flask.errors module just needed a different format

    :param graph: Instance of microcosm graph
    """

    # override all of the werkzeug HTTPExceptions
    for code in default_exceptions.keys():
        graph.flask.register_error_handler(code, graph.connexion_error_handler.handle)

    # register catch all for user exceptions
    graph.flask.register_error_handler(Exception, graph.connexion_error_handler.handle)
