import os

USER_POOL_ID = os.environ.get("USER_POOL_ID")
CLIENT_ID = os.environ.get("CLIENT_ID")
DATABASE_URL = os.environ.get("DATABASE_URL")
AWS_REGION = os.environ.get("AWS_REGION", "ap-south-1")