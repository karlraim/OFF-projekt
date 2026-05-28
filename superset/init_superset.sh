#!/bin/bash

set -e

superset db upgrade

superset fab create-admin \
  --username "$SUPERSET_ADMIN_USERNAME" \
  --firstname "$SUPERSET_ADMIN_FIRSTNAME" \
  --lastname "$SUPERSET_ADMIN_LASTNAME" \
  --email "$SUPERSET_ADMIN_EMAIL" \
  --password "$SUPERSET_ADMIN_PASSWORD" \
|| true

superset init