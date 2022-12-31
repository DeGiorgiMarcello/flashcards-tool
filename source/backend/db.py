from os.path import dirname, join
from os import environ
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker


envvar = "HOME_CONNECTION_STRING"
env_path = join(dirname(dirname(__file__)), ".env")
load_dotenv(env_path)
conn_str = environ.get(envvar)

engine = create_engine(
    # environ.get(envvar),
    "sqlite:///cards.db",
    connect_args={"check_same_thread": False},
)


Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
