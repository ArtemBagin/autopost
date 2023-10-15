#!/usr/bin/env bash


if [[ "${1}" == "worker" ]]; then
  celery -A autopost.autopost:celery worker --loglevel=INFO --pool=solo
elif [[ "${1}" == "beat" ]]; then
  celery -A autopost.autopost:celery beat -S redbeat.RedBeatScheduler --max-interval 5
 fi