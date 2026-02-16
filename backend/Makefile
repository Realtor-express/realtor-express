run:
	PYTHONPATH=. uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

rev:
	PYTHONPATH=. alembic revision --autogenerate -m "init"

up:
	PYTHONPATH=. alembic upgrade head
