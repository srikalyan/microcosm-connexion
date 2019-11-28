from mock import patch, Mock
from hamcrest import assert_that, calling, raises, is_, equal_to

from microcosm_connexion.resolver import MicrocosmResolver


class SampleController(object):  # pragma: no cover
    def camelCase(self):  # noqa
        pass

    def snake_case(self):
        pass


class TestMicrocosmResolver(object):
    def setup(self):
        self.controller = SampleController()
        self.resolver = MicrocosmResolver(self.controller)

    def test_resolve_function_from_operation_id_value_error(self):
        assert_that(calling(self.resolver.resolve_function_from_operation_id).with_args("something.other_thing"),
                    raises(ValueError))

    def test_resolve_function_from_operation_id_for_camel_case(self):
        operation_id = "camelCase"

        with patch.object(self.resolver, "_make_transactional_func") as mock_make_transactional_func:
            assert_that(self.resolver.resolve_function_from_operation_id(operation_id),
                        is_(equal_to(mock_make_transactional_func.return_value)))

            mock_make_transactional_func.assert_called_once_with(self.controller.camelCase)

    def test_resolve_function_from_operation_id_for_snake_case(self):
        operation_id = "snake_case"

        with patch.object(self.resolver, "_make_transactional_func") as mock_make_transactional_func:
            assert_that(self.resolver.resolve_function_from_operation_id(operation_id),
                        is_(equal_to(mock_make_transactional_func.return_value)))

            mock_make_transactional_func.assert_called_once_with(self.controller.snake_case)

    def test_resolve_function_from_operation_id_for_snake_case_as_camel_case(self):
        operation_id = "snakeCase"

        with patch.object(self.resolver, "_make_transactional_func") as mock_make_transactional_func:
            assert_that(self.resolver.resolve_function_from_operation_id(operation_id),
                        is_(equal_to(mock_make_transactional_func.return_value)))

            mock_make_transactional_func.assert_called_once_with(self.controller.snake_case)

    def test_make_transactional_func_disable(self):
        self.resolver.mark_transactional = False
        some_func = Mock()
        assert_that(self.resolver._make_transactional_func(some_func), is_(equal_to(some_func)))

    @patch("microcosm_postgres.context.transactional")
    def test_make_transactional_func_enable(self, mock_transactional):
        self.resolver.mark_transactional = True
        some_func = Mock()
        assert_that(self.resolver._make_transactional_func(some_func), is_(equal_to(mock_transactional.return_value)))

        mock_transactional.assert_called_once_with(some_func)
