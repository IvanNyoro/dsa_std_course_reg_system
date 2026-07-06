# Justin's Workspace: Frontend UI & Registration Views

## My role (Member 5 — Frontend / UI Designer & Project Manager)

This folder contains the visual interface for the Student Course
Registration System: the dashboard, course catalog, and waitlist
views, plus the registration flow (eligibility check + register /
join waitlist).

## What's in here

| File | What it does |
|---|---|
| `templates/index.html` | The single-page UI — three tabs (Dashboard, Course Catalog, Waitlist), a registration modal, and the JavaScript that talks to the backend API |
| `static/style.css` | The visual design — a "registrar ledger" theme (ink navy / parchment / gold), with rubber-stamp style badges for course status (Enrolled / Waitlisted / Prereq Blocked / Open) |

## How this connects to the rest of the system

This UI is a **thin client** — it holds no business logic of its own.
It expects a Flask backend exposing these routes (built by Member 4,
using Ivan's `Queue`/`PrerequisiteGraph` and Member 3's search/sort
algorithms):

- `GET  /api/catalog?student_id=...` → list of courses with an
  `eligible` flag per course
- `GET  /api/dashboard/<student_id>` → a student's current schedule
  and waitlist positions
- `GET  /api/waitlist` → every course's waitlist queue, front to back
- `POST /api/register` → body `{student_id, course_code}` → registers
  or waitlists the student
- `POST /api/drop` → body `{student_id, course_code}` → drops a
  course and (if applicable) promotes the next waitlisted student

The frontend renders whatever JSON these routes return — it doesn't
know or care how eligibility is calculated, only what the answer was.

## Design notes (for the report)

- Rubber-stamp badges were chosen as the one recurring visual element
  across every screen, since the whole system is fundamentally about
  stamping an eligibility decision (enrolled / blocked / waitlisted)
  on a request — it ties the visual language to what the backend is
  actually doing.
- Course codes are set in monospace throughout, to read like stamped
  ledger entries rather than plain text.

## Status

UI is visually complete and fully styled as of the July 6th progress
check. Still to do before the final submission: confirm the API
contract above matches whatever Member 4 ships, adjust field names if
needed, and swap browser `alert()` popups for a proper in-page
notification.
