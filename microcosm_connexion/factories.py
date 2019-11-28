import connexion

from microcosm.config.validation import typed
from microcosm.decorators import defaults
from microcosm.hooks import invoke_resolve_hook
from microcosm_flask.session import register_session_factory


@defaults(
    port=typed(type=int, default_value=5000)
)
def configure_connexion(graph):
    """
    Creates and configures connexion's app instance
    :param graph: Instance of microcosm graph
    :return: connexion instance
    """
    connexion_app = connexion.App(graph.metadata.import_name,
                                  port=graph.config.connexion.port,
                                  debug=graph.metadata.debug)

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
    :return:
    """
    from microcosm_postgres.context import SessionContext

    return register_session_factory(graph, graph.config.postgres_session_factory.db_key, SessionContext.make)
