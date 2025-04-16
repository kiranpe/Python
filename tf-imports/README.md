pubsub
--------

1. Basic Pub/Sub Import (Topics + Subscriptions only)
If you're importing topics and subscriptions (no IAM), run:

```python import_resources.py --file resources.tf --type pubsub --execute```

This will:

Import topics and subscriptions

Skip IAM roles gracefully if --project-number is not provided

Log any skipped IAM blocks

2. Pub/Sub + IAM Import (e.g., pubsub.publisher, subscriber roles)
If your modules include IAM bindings (e.g., `google_pubsub_topic_iam_member`), run:

```python import_resources.py --file resources.tf --type pubsub --project-number 123456789012 --execute --fix-state```

This will:

Import everything including IAM roles

Generate and run import_pubsub_iam.sh for IAM resources

Patch the state to add missing project fields after apply

