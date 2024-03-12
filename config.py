from pathlib import Path

ROOT_DIR = Path(__file__).parent.absolute()

MODEL_DIR = ROOT_DIR.joinpath('model')

DATA_DIR = ROOT_DIR.joinpath('data')

for _dir in [MODEL_DIR, DATA_DIR]:
    _dir.mkdir(exist_ok=True)

def catch_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(e)

    return wrapper



USERS = [{
    'name': '1',
    'pass': '12345',
    'gid': 1
}]


GAZES = []
for file in DATA_DIR.joinpath('templates').glob('*'):
    GAZES.append({'name': file.stem, 'url': str(file.resolve()).replace('\\', '/')})
print(GAZES)

MODEL_NAME = 'model_u2_g2.pkl'
DATABASE_PATH = ROOT_DIR.joinpath('sql.db')