python -m venv venv
call "venv/Scripts/activate"

pip install -r requirements.txt

python scripts/generate_random_key.py > .env

set /p key=<.env

set secret=SECRET="%key%"

echo %secret% > .env
