def give_secret():

    from dotenv import load_dotenv
    import os
    from pathlib import Path

    BASE_DIR = Path(__file__).parent.parent.parent
    load_dotenv(BASE_DIR.joinpath(".env"))
    return os.environ["SECRET_KEY"]
