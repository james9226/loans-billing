#!/bin/bash

export PUBSUB_PROJECT_ID=firebase-svelte-381023
export PUBSUB_EMULATOR_HOST=localhost:8085
poetry run python publisher.py firebase-svelte-381023 create loan-events
poetry run python publisher.py firebase-svelte-381023 create loan-creation-requests
poetry run python subscriber.py firebase-svelte-381023 create-push loan-creation-requests loans-billing-loan-creation-subscription http://localhost:8000/consumer/creation