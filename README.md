# autopost

pip install requirements

cd app

celery -A autopost.autopost:celery worker --loglevel=INFO --pool=solo

celery -A autopost.autopost:celery beat -S redbeat.RedBeatScheduler

uvicorn main:app --reload
