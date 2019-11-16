import inflection
from connexion.resolver import Resolver


class MicrocosmResolver(Resolver):
    def __init__(self, controller):
        """
        A custom resolver that uses operation Id and a controller instance to resolve the method name.

        This resolver uses the following rules
        1. If there is a method whose name matches with the operation ID then return that method handler
        2. If there is a method whose name matches with the snake case version of the operation ID then return
        that method handler

        The option 2 is needed as operation IDs can be written in camelcase in the schema and python uses snake case
        to name its methods.

        :param controller: Instance of a controller that defines the methods mentioned int the API spec.
        """
        self.controller = controller

    def resolve_function_from_operation_id(self, operation_id):
        if '.' in operation_id:
            raise ValueError("MicrocosmResolver will not operation id '{}' as it has '.' in it".format(operation_id))

        try:
            return getattr(self.controller, operation_id)
        except AttributeError:
            # Try the snake case
            snake_operation_id = inflection.underscore(operation_id)
            return getattr(self.controller, snake_operation_id)
