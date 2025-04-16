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

Pub/Sub (Topics, Subscriptions, IAM)
------------------------------------

Minimum setup (topics + subscriptions only):

```
python import_resources.py \
  --file resources.tf \
  --type pubsub \
  --execute
```

This will:

IAM imports will be skipped with warnings if --project-number is not provided.

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


