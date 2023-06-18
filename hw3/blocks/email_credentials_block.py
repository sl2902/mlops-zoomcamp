from prefect_email import EmailServerCredentials
import os
from dotenv import load_dotenv

load_dotenv()

credentials = EmailServerCredentials(
    username=os.getenv("username"),
    password=os.getenv("password"),  # must be an app password
)
credentials.save("hw3-send-email", overwrite=True)
