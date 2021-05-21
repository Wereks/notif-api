REST API written in the FastApi framework, using OAuth2 authentication with a JWT token. Unit tests were written in Pytest. 

The API can save, display, edit short messages (to 160 characters) with the additional view count of every message.

Detailed documentation of the API can be found on the server in the endpoint /docs or /redoc in the OpenAPI standard.

If you want to run the API on your local machine, you need to download all modules from the pipfile. Set the environmental variables for:

`ACCESS_TOKEN_EXPIRE_MINUTES : int` - time after the JWT expires
`ALGORITHM : str` - algorithm to hash the token
`DATABASE_URL : str` - SQLalchemy compatibable database url
`SECRET_KEY : str` - sekret key for the token

If everything is set, you can start the api with the command `uvicorn app.api:app`, called from the root folder.

To run the tests, you need to set the `SQLALCHEMY\_TEST\_DATABASE\_URI` variable in the `app/tests/conftest.py` file, after that you can use the `pytest` command to run the tests.