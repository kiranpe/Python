 Service Account Import
 -----------------------
 ```
python import_resources.py \
  --file resources.tf \
  --type service_account \
  --execute
```

This will:

Import `google_service_account.this`

Import all `google_service_account_iam_member["ROLE"]` if iam_roles is defined

Storage Bucket Import
---------------------

```
python import_resources.py \
  --file resources.tf \
  --type storage_bucket \
  --execute
```

This will:

Import `google_storage_bucket.this` using bucket_name

Compute Instance Import
------------------------

```
python import_resources.py \
  --file resources.tf \
  --type compute_instance \
  --execute
```

This will:

Import `google_compute_instance.this` using zone, name, and project_id

pubsub
--------

1. Basic Pub/Sub Import (Topics + Subscriptions only)
If you're importing topics and subscriptions (no IAM), run:

```
python import_resources.py --file resources.tf --type pubsub --execute
```

This will:

Import topics and subscriptions

Skip IAM roles gracefully if `--project-number` is not provided

Log any skipped IAM blocks

2. Pub/Sub + IAM Import (e.g., pubsub.publisher, subscriber roles)
If your modules include IAM bindings (e.g., `google_pubsub_topic_iam_member`), run:

```
python import_resources.py --file resources.tf --type pubsub --project-number 123456789012 --execute --fix-state
```

This will:

Import everything including IAM roles

Generate and run `import_pubsub_iam.sh` for IAM resources

Patch the state to add missing project fields after apply

3. Pub/Sub with IAM — but Skip Auto Execution of Script
If you want to review or manually run the IAM import shell script:

```
python import_resources.py --file resources.tf --type pubsub --project-number 123456789012 --execute --fix-state --no-run-script
```

