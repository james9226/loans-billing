# loans-billing-engine

poetry run uvicorn loans_billing.main:app --reload

## Pub/Sub Emulator

Requires Java7+ Runtime installed (`brew install openjdk@11`)

- `gcloud components install pubsub-emulator`
- `gcloud components update`

In one terminal, run: `gcloud beta emulators pubsub start --project=firebase-svelte-381023`
In a second terminal, run `bash start.bash`
Start the app in a third terminal!