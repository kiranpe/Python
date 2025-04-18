#!/bin/bash

# Usage: ./fix_pubsub_state.sh <PROJECT_ID>
PROJECT_ID=$1
STATE_FILE="tfstate.json"
FIXED_FILE="tfstate_fixed.json"

if [[ -z "$PROJECT_ID" ]]; then
  echo "❌ Usage: $0 <PROJECT_ID>"
  exit 1
fi

echo "📥 Pulling Terraform state..."
terraform state pull > "$STATE_FILE"

echo "🛠️  Patching missing/null project values for Pub/Sub IAM resources..."

# Replace `"project": null` or `"project": ""` with actual project_id
sed -E "s/\"project\": (null|\"\")/\"project\": \"$PROJECT_ID\"/g" "$STATE_FILE" > "$FIXED_FILE"

echo "📤 Pushing patched state back..."
terraform state push "$FIXED_FILE"

echo "✅ State fixed and pushed successfully."
