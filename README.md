# autopost

pip install -r requirements.txt

cd app

celery -A autopost.autopost:celery worker --loglevel=INFO --pool=solo

celery -A autopost.autopost:celery beat -S redbeat.RedBeatScheduler

uvicorn main:app --reload
