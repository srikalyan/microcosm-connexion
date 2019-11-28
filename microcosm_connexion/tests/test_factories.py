from hamcrest import assert_that, is_, equal_to
from microcosm_postgres.context import SessionContext
from mock import Mock, patch, call

from microcosm_connexion.factories import configure_connexion, configure_postgres_session_factory


@patch("microcosm_connexion.factories.invoke_resolve_hook")
@patch("microcosm_connexion.factories.connexion")
def test_configure_connexion(mock_connexion, mock_invoke_resolve_hook):
    graph = Mock()
    connexion_instance = configure_connexion(graph)

    assert_that(connexion_instance, is_(equal_to(mock_connexion.App.return_value)))

    mock_connexion.App.assert_called_once_with(graph.metadata.import_name,
                                               port=graph.config.connexion.port,
                                               debug=graph.metadata.debug)
    app = mock_connexion.App.return_value.app

    mock_invoke_resolve_hook.assert_called_once_with(app)
    graph.assign.assert_has_calls([
        call("flask", app),
        call("app", app)
    ])

    assert_that(graph.assign.call_count, is_(equal_to(2)))


@patch("microcosm_connexion.factories.register_session_factory")
def test_configure_postgres_session_factory(mock_register_session_factory):
    graph = Mock()

    assert_that(configure_postgres_session_factory(graph), is_(equal_to(mock_register_session_factory.return_value)))

    mock_register_session_factory.assert_called_once_with(graph, graph.config.postgres_session_factory.db_key,
                                                          SessionContext.make)
