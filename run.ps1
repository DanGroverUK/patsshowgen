./.venv/Scripts/activate.ps1
$env:FLASK_APP = "show.py"
$env:FLASK_ENV = "development"
flask run --host=0.0.0.0
