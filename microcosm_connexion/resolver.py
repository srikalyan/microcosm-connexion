import inflection
from connexion.resolver import Resolver


class MicrocosmResolver(Resolver):
    def __init__(self, controller, mark_transactional=True):
        """
        A custom resolver that uses operation Id and a controller instance to resolve the method name.

        This resolver uses the following rules
        1. If there is a method whose name matches with the operation ID then return that method handler
        2. If there is a method whose name matches with the snake case version of the operation ID then return
        that method handler

        The option 2 is needed as operation IDs can be written in camelcase in the schema and python uses snake case
        to name its methods.

        :param controller: Instance of a controller that defines the methods mentioned int the API spec.
        :param mark_transactional: Boolean to indicate if controller methods needs to be run inside a DB transaction.
        """
        self.controller = controller
        self.mark_transactional = mark_transactional

    def resolve_function_from_operation_id(self, operation_id):
        if '.' in operation_id:
            raise ValueError("MicrocosmResolver will not operation id '{}' as it has '.' in it".format(operation_id))

        try:
            return self._make_transactional_func(getattr(self.controller, operation_id))
        except AttributeError:
            # Try the snake case
            snake_operation_id = inflection.underscore(operation_id)
            return self._make_transactional_func(getattr(self.controller, snake_operation_id))

    def _make_transactional_func(self, func):
        if not self.mark_transactional:
            return func

        from microcosm_postgres.context import transactional
        return transactional(func)
