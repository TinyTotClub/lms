# LMS mobile stack (docker)

One-command local Frappe LMS instance with the mobile-app server addons
installed: **lms** (this repo) + **mobile_control** (token auth for the
Flutter SDK) + **lms_mobile_bridge** (Firebase Auth bridge).

## Prerequisites

Sibling checkouts (paths overridable in `.env`):

```
GitHub/
├── lms/                    # this repo — the branch you have checked out is installed
├── frappe-mobile-control/
└── lms_mobile_bridge/
```

`bench get-app` clones each mounted repo's **currently checked-out branch** —
commit your work before (re)creating the bench.

## Usage

```bash
cd docker/mobile
cp .env.example .env   # fill in FIREBASE_PROJECT_ID etc. — .env is gitignored
docker compose up
```

First boot builds the whole bench (several minutes). Then:

- Web/SPA: http://localhost:8090 (Administrator / admin — change outside local dev)
- Firebase login: `POST /api/v2/method/mobile_auth.login_with_firebase`
- Flutter app: `flutter run --dart-define=LMS_BASE_URL=http://<lan-ip>:8090`

The init script auto-configures the site (developer_mode, CORS, Firebase
project id) and seeds **Mobile Configuration** (LMS doctypes for the SDK's
metadata screens) + **Firebase Auth Settings** (default app_role→LMS role
mappings) idempotently on every start.

## Winding down

```bash
docker compose down        # stop; bench + DB survive
docker compose down -v     # full wipe (bench, database, everything)
```

## Rebuilding after app changes

The bench clones the apps at first boot. To pick up new commits:

```bash
docker compose exec frappe bash -lc \
  "cd frappe-bench/apps/lms && git pull /workspace/apps-src/lms && cd ../.. && bench --site lms.localhost migrate"
```

or just `docker compose down -v && docker compose up` for a clean slate.

## Running server tests

```bash
docker compose exec frappe bash -lc \
  "cd frappe-bench && bench --site lms.localhost run-tests --app lms_mobile_bridge"
```
