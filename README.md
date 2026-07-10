<<<<<<< HEAD
# Weekly Report Generator & Team Dashboard

A full-stack app where **team members** submit structured weekly work reports and **managers**
view/analyze those reports across the team through a consolidated dashboard.

- **Frontend:** Next.js (App Router) + Tailwind CSS + Recharts
- **Backend:** Django + Django REST Framework + SimpleJWT
- **Database:** MySQL
- **AI Chat Assistant (bonus):** Manager-facing chat backed by the Anthropic API, grounded on the
  team's own submitted report data (see [`backend/aiassistant`](backend/aiassistant/views.py)).

---

## 1. Prerequisites

- Python 3.11+
- Node.js 18+
- MySQL Server 8+ running locally (or accessible remotely)

---

## 2. Database setup

Create the database once, from a MySQL shell:

```sql
CREATE DATABASE weekly_reports CHARACTER SET utf8mb4;
```

No native MySQL client libraries are required on the Python side — the backend uses `PyMySQL`
(a pure-Python driver), so there's nothing extra to compile/install beyond `pip install`.

---

## 3. Backend setup (Django)

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env            # then edit .env with your MySQL credentials
python manage.py migrate
python manage.py createsuperuser  # create your first account; set role via /admin or shell

python manage.py runserver       # http://localhost:8000
```

**Creating a manager account:** anyone can self-register via `/api/auth/register/`, but new
signups always default to the `team_member` role (to prevent self-service privilege escalation).
Promote a user to manager either via `/admin/` (Django admin, using your superuser login) or:

```bash
python manage.py shell -c "from accounts.models import User; u=User.objects.get(username='YOUR_USER'); u.role='manager'; u.save()"
```

### Quick local test without MySQL

If you just want to poke around without setting up MySQL yet, set `DB_ENGINE=sqlite` in `.env`
(or `export DB_ENGINE=sqlite`) and `migrate`/`runserver` will use a local SQLite file instead.

### AI Chat Assistant (optional)

Set `ANTHROPIC_API_KEY` in `backend/.env` to enable `/api/ai/chat/`. Without it, the endpoint
still responds (so the frontend doesn't break) but explains the feature isn't configured.

---

## 4. Frontend setup (Next.js)

```bash
cd frontend
cp .env.local.example .env.local   # points the frontend at the backend API
npm install
npm run dev                        # http://localhost:3000
```

---

## 5. Using the app

1. Register a couple of accounts (they'll be Team Members). Promote one to `manager` (see above).
2. Log in as a manager and add a few projects/categories under Projects.
3. Log in as a team member, go to My Reports, and submit a weekly report tagged to a project.
4. Log back in as the manager to see the Team Dashboard: summary metrics, submission
   trend, status-by-member, workload-by-project, recent activity, and filters (member/project/week/date range).
5. Try the 💬 Ask AI widget on the dashboard (manager-only) if `ANTHROPIC_API_KEY` is set.

---

## 6. Project structure

```
backend/
  core/            # Django project settings/urls
  accounts/        # Custom User model, JWT auth, roles, permissions
  projects/        # Project/category CRUD
  reports/         # WeeklyReport model, CRUD, dashboard aggregation endpoint
  aiassistant/     # AI chat endpoint (manager-only, grounded on report data)

frontend/
  src/app/
    login/ register/        # Auth pages
    reports/                 # Personal weekly report page (Team Member)
    dashboard/                # Team Dashboard with charts + filters (Manager)
    projects/                # Project/category management (Manager)
  src/components/            # Navbar, AiChatWidget
  src/lib/                    # Axios API client (JWT attach + refresh), auth helpers
```

## 7. Role-based access, in brief

| Endpoint | Team Member | Manager |
|---|---|---|
| `POST /api/reports/` (own) | ✅ | ✅ |
| `GET /api/reports/` | own only | all, filterable |
| `GET /api/reports/dashboard/summary/` | ❌ | ✅ |
| `POST/PATCH/DELETE /api/projects/` | ❌ | ✅ |
| `GET /api/projects/` | ✅ (read-only) | ✅ |
| `POST /api/ai/chat/` | ❌ | ✅ |

See [`ER_DIAGRAM.md`](ER_DIAGRAM.md) for the database schema.
=======
# Weekly-Report-Generator-Team-Dashboard
A full-stack app where 'team members' submit structured weekly work reports and 'managers' view/analyze those reports across the team through a consolidated dashboard.
>>>>>>> 48266b3596bfae8a3ae2ee157eb3890ebd09b576
