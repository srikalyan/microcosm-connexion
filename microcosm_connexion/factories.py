import connexion

from microcosm.config.validation import typed
from microcosm.decorators import defaults
from microcosm_flask.session import register_session_factory


@defaults(
    port=typed(type=int, default_value=5000)
)
def configure_connexion(graph):
    connexion_app = connexion.App(graph.metadata.import_name,
                                  port=graph.config.connexion.port,
                                  debug=graph.metadata.debug)

    app = connexion_app.app
    app.debug = graph.metadata.debug
    app.testing = graph.metadata.testing

    graph.flask = app
    graph.app = app

    return connexion_app


def configure_postgres_session_factory(graph):
    """
    Bind the SQLAlchemy session context to Flask.

    """
    from microcosm_postgres.context import SessionContext

    return register_session_factory(graph, "db", SessionContext.make)
