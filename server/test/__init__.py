import logging

import connexion
from flask_testing import TestCase

from server import error
from server.encoder import JSONEncoder


class BaseTestCase(TestCase):

    token: str = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImQ0OWU0N2ZiZGQ0ZWUyNDE0Nzk2ZDhlMDhjZWY2YjU1ZDA3MDRlNGQiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdGhlbGFiLTkyNGYzIiwiYXVkIjoidGhlbGFiLTkyNGYzIiwiYXV0aF90aW1lIjoxNjk3NzA2NTkyLCJ1c2VyX2lkIjoibEVXeGN0bDcwYU9rTzU3UkhOck1hZEh4cFhsMiIsInN1YiI6ImxFV3hjdGw3MGFPa081N1JITnJNYWRIeHBYbDIiLCJpYXQiOjE2OTk2MTkwNDEsImV4cCI6MTY5OTYyMjY0MSwiZW1haWwiOiI5OGMyNTM3YS1hYzYyLTQ4NzYtYjk0MS1hOTliMzg5OWIwYjUrcjIyM3JzeXoxY2ZxcGJqbWl4Nm95dTFoZmdud2Nrd3poQHh1bW0ubWUiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsib2lkYy54dW1tIjpbInIyMjNyc3l6MWNmcVBiam1pWDZvWXUxaEZnTndDa1daSCJdLCJlbWFpbCI6WyI5OGMyNTM3YS1hYzYyLTQ4NzYtYjk0MS1hOTliMzg5OWIwYjUrcjIyM3JzeXoxY2ZxcGJqbWl4Nm95dTFoZmdud2Nrd3poQHh1bW0ubWUiXX0sInNpZ25faW5fcHJvdmlkZXIiOiJvaWRjLnh1bW0iLCJzaWduX2luX2F0dHJpYnV0ZXMiOnsiYXBwX25hbWUiOiJUaGUgTGFiIiwibmV0d29ya19pZCI6IjIxMzM3IiwidXNlcnRva2VuX3V1aWR2NCI6ImI2OTcyNDQ4LTA3YWEtNDMxYy05ZDUwLTYxZDBhYWJmN2NmMSIsIm5ldHdvcmtfZW5kcG9pbnQiOiJ3c3M6Ly94YWhhdS5uZXR3b3JrIiwiYXBwX3V1aWR2NCI6Ijk4YzI1MzdhLWFjNjItNDg3Ni1iOTQxLWE5OWIzODk5YjBiNSIsInNjb3BlIjoiWHVtbVBrY2UiLCJzdGF0ZSI6IjE4MmQwNzIwZGNlY2Y1NmMzNGI1YjkwZTQyMjNmOWJlNDU1OTIzYzdjNzIwNmEyNDAxMDk4NGViODIyMTA5MTBjZTM3OWQ3NTkxOWQzOTA1MTA5ZDhlYWIzNjY3ZWFjM2I2ZGE0NWRlNWMzMTRlMWQ0YWVkNmRmM2YzNTFlYzBhIiwibmV0d29ya190eXBlIjoiWEFIQVUiLCJjbGllbnRfaWQiOiI5OGMyNTM3YS1hYzYyLTQ4NzYtYjk0MS1hOTliMzg5OWIwYjUiLCJwYXlsb2FkX3V1aWR2NCI6IjkwYWZlMDE1LTUyZTktNDMxNC1hNmU4LWY0YTE2M2ZiMzM0YSJ9fX0.mSDN79q_uGGWYad7Jq8ItG-MGhjcNxFe4cW_Ab2hjWWXh-9rNHak-CLRHqoOx7LjcRWzG2R6-ADVYp5z3O-BRJssAPud5ucyN0kdWgGUvjbto6PTO2wt4cZKH7E5oZbhusjhjnZGbzAN7_cPeKaDw3V2OMCN3xSNCHZSSQFl0oHvoK5F7aeYdxgWfzyT1ViILt5teZuL3hJYBdEgC_VGg6PThz3shV1KrrxCR2LBBfiXGcwikFnD2f2fPakvHrfF-ImOriqY9TlCG01VhptJvjd4VeBTZVSRfozYELzcrQF7kn2ZGNsc6Wo9mtcpUxhpGQ3Y9utfS8sOT0VGFsinFg"
    
    def create_app(self):
        logging.getLogger('connexion.operation').setLevel('DEBUG')
        app = connexion.App(__name__, specification_dir='../swagger/')
        app.app.json_encoder = JSONEncoder
        app.add_api('latest.yaml')
        app.add_error_handler(
            error.BadRequestError, 
            error.bad_request_handler
        )
        app.add_error_handler(
            error.NotAuthorizedError, 
            error.not_auth_handler
        )
        app.add_error_handler(
            error.NotFoundError, 
            error.not_found_handler
        )
        app.add_error_handler(
            error.InternalServerError, 
            error.internal_handler
        )
        return app.app
