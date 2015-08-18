import os
import logging

logging.basicConfig(level=logging.INFO)

ACCOUNT_SID = os.environ["ACCOUNT_SID"]
AUTH_TOKEN = os.environ["AUTH_TOKEN"]
DATABASE_URL = os.environ["DATABASE_URL"]
