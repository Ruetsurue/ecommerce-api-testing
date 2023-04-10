import pytest

from dotenv import load_dotenv


@pytest.fixture(scope='session', autouse=True)
def create_test_enviroment():
    # config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '', '.env')
    # logging.debug(config_path)
    # load_dotenv(dotenv_path=config_path)
    load_dotenv()
