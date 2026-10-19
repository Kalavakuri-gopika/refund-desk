#!/usr/bin/env bash
set -euo pipefail

echo "==> Seeding RefundDesk Pod Data..."

# 1. Upload Knowledge Files
echo "--> Uploading store policies and response templates..."
lemma files upload ./files/knowledge/store_policies.md /knowledge/store_policies.md
lemma files upload ./files/knowledge/email_templates.md /knowledge/email_templates.md

# 2. Seed Orders and Tickets Records
echo "--> Importing 30-day synthetic orders..."
lemma records import orders ./seed/orders.json

echo "--> Importing sample tickets and approval gate state..."
lemma records import tickets ./seed/tickets.json

echo "==> Seeding complete! RefundDesk is ready for operations."
