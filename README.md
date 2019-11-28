# microcosm-connexion

## Description:
A python library that exposes [microcosm] factories for [connexion]

[Connexion][connexion] is a python library that reads a open-api/swagger spec and binds methods for a class to the spec.
This project provides the glue between [microcosm] projects and [connexion]. It provides the following components

1. Connexion: An instance of connexion
2. flask: An instance of flask created by connexion
3. app: Same as flask instance.
4. postgress_session_factory: Binds the Postgres SQLAlchemy session context to Flask
5. connexion_error_handler: An instance of the ConnexionErrorHandler used for serializing errors
6. configure_connexion_error_handler: Binds ConnexionErrorHandler to flask's generic error handler mechanism.

The reason for providing flask and app is to make sure that connexion's version of flask overrides [microcosm-flask]'s
app.

Note: A cookiecutter would created to make it easy for app developers to quickly start building APIs.

[connexion]: https://github.com/zalando/connexion
[microcosm]: https://github.com/globality-corp/microcosm
[microcsom-flask]: https://github.com/globality-corp/microcosm-flask
[microcsom-postgres]: https://github.com/globality-corp/microcosm-postgres

