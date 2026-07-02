#!/bin/bash
set -euo pipefail

SITE_NAME="${SITE_NAME:-lms.localhost}"
ADMIN_PASSWORD="${ADMIN_PASSWORD:-admin}"

configure_site() {
    bench --site "$SITE_NAME" set-config developer_mode 1
    bench --site "$SITE_NAME" set-config allow_cors "*"
    bench --site "$SITE_NAME" set-config mute_emails 1
    if [ -n "${FIREBASE_PROJECT_ID:-}" ]; then
        bench --site "$SITE_NAME" set-config firebase_project_id "$FIREBASE_PROJECT_ID"
    fi
    if [ -n "${FIREBASE_AUTH_EMULATOR_HOST:-}" ]; then
        bench --site "$SITE_NAME" set-config firebase_auth_emulator_host "$FIREBASE_AUTH_EMULATOR_HOST"
    fi
    if [ -n "${MOBILE_PACKAGE_NAME:-}" ]; then
        bench --site "$SITE_NAME" set-config mobile_package_name "$MOBILE_PACKAGE_NAME"
    fi
    bench --site "$SITE_NAME" execute lms_mobile_bridge.dev_seed.seed_dev_site
    bench --site "$SITE_NAME" clear-cache
}

if [ -d "/home/frappe/frappe-bench/apps/frappe" ]; then
    echo "Bench already exists — refreshing config and starting"
    cd frappe-bench
    configure_site
    bench start
    exit 0
fi

echo "Creating new bench..."
if [ -n "${NVM_DIR:-}" ] && [ -n "${NODE_VERSION_DEVELOP:-}" ]; then
    export PATH="${NVM_DIR}/versions/node/v${NODE_VERSION_DEVELOP}/bin/:${PATH}"
fi

bench init --skip-redis-config-generation frappe-bench
cd frappe-bench

# Use containers instead of localhost
bench set-mariadb-host mariadb
bench set-redis-cache-host redis://redis:6379
bench set-redis-queue-host redis://redis:6379
bench set-redis-socketio-host redis://redis:6379

# Remove redis, watch from Procfile
sed -i '/redis/d' ./Procfile
sed -i '/watch/d' ./Procfile

# Apps: payments from upstream; lms / mobile_control / lms_mobile_bridge from
# the mounted local checkouts (clones the currently checked-out branch)
bench get-app payments
bench get-app /workspace/apps-src/lms
bench get-app /workspace/apps-src/mobile_control
bench get-app /workspace/apps-src/lms_mobile_bridge

bench new-site "$SITE_NAME" \
    --force \
    --mariadb-root-password 123 \
    --admin-password "$ADMIN_PASSWORD" \
    --no-mariadb-socket

bench --site "$SITE_NAME" install-app payments
bench --site "$SITE_NAME" install-app lms
bench --site "$SITE_NAME" install-app mobile_control
bench --site "$SITE_NAME" install-app lms_mobile_bridge

configure_site
bench use "$SITE_NAME"

bench start
