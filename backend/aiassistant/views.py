import os
import re
from typing import Optional, cast
from decouple import config
import json
import urllib.request
from google import genai
from decouple import config


from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from accounts.permissions import IsManager
from reports.models import WeeklyReport

# ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
# ANTHROPIC_MODEL = "claude-sonnet-4-6"
# # Read API key via python-decouple so .env is respected when running Django
# ANTHROPIC_API_KEY = config("ANTHROPIC_API_KEY", default=None)

from google import genai

GEMINI_API_KEY = cast(
    Optional[str],
    config("GEMINI_API_KEY", default=None, cast=str)
)


gemini_client = None

if GEMINI_API_KEY:
    gemini_client = genai.Client(
        api_key=GEMINI_API_KEY
    )

    
GEMINI_MODEL = "gemini-2.0-flash"

def _build_context(week_start=None, project_id=None, limit=100):
    """
    Lightweight retrieval step: pull the most relevant submitted reports as plain
    text context for the LLM. This is intentionally simple (no vector DB) — for a
    small team's weekly reports, a direct filtered query is enough context to be
    accurate, and keeps the whole flow auditable and privacy-transparent.
    """
    qs = WeeklyReport.objects.filter(status=WeeklyReport.Status.SUBMITTED).select_related(
        "user", "project"
    )
    if week_start:
        qs = qs.filter(week_start=week_start)
    if project_id:
        qs = qs.filter(project_id=project_id)
    qs = qs.order_by("-week_start")[:limit]

    lines = []
    for r in qs:
        lines.append(
            f"- Week {r.week_start} | {r.user.username} | "
            f"Project: {r.project.name if r.project else 'N/A'}\n"
            f"  Completed: {r.tasks_completed}\n"
            f"  Planned: {r.tasks_planned}\n"
            f"  Blockers: {r.blockers or 'None'}\n"
            f"  Hours: {r.hours_worked or 'N/A'}"
        )
    return "\n".join(lines) if lines else "No submitted reports match this query."


def _local_summarize(context: str, message: str) -> str:
    """
    Lightweight local summarizer used as a fallback when the external LLM
    request fails. It extracts blocker lines from the context and returns a
    concise summary targeted to the user's message.
    """
    if not context or context.startswith("No submitted reports"):
        return "No submitted reports are available to answer that question."

    # Parse the context into structured report entries.
    reports = []
    current = None
    for line in context.splitlines():
        line = line.rstrip()
        if line.startswith("- Week "):
            if current:
                reports.append(current)
            # initialize new report
            current = {
                "header": line,
                "user": None,
                "project": None,
                "completed": "",
                "planned": "",
                "blockers": "",
                "hours": None,
            }
            # try to extract user and project from header
            try:
                parts = line.split("|")
                if len(parts) >= 2:
                    user_part = parts[1].strip()
                    current["user"] = user_part
                if len(parts) >= 3:
                    proj = parts[2].replace("Project:", "").strip()
                    current["project"] = proj
            except Exception:
                pass
        elif current is not None:
            # parse sub-lines like '  Completed: ...'
            stripped = line.strip()
            if stripped.lower().startswith("completed:"):
                current["completed"] = stripped.split(":", 1)[1].strip()
            elif stripped.lower().startswith("planned:"):
                current["planned"] = stripped.split(":", 1)[1].strip()
            elif stripped.lower().startswith("blockers:"):
                current["blockers"] = stripped.split(":", 1)[1].strip()
            elif stripped.lower().startswith("hours:"):
                try:
                    current["hours"] = float(stripped.split(":", 1)[1].strip())
                except Exception:
                    current["hours"] = None
    if current:
        reports.append(current)

    if not reports:
        return "I don't see any submitted reports to summarize."

    # Aggregate insights
    total_reports = len(reports)
    total_hours = sum(r.get("hours") or 0 for r in reports)
    reporters_with_blockers = [r for r in reports if r.get("blockers")]
    blocker_lines = [f"{r.get('user')}: {r.get('blockers')}" for r in reporters_with_blockers]

    # Formulate a concise answer tailored to the incoming message.
    clean = (message or "").lower().strip()

    # Conversational greetings
    if clean and re.match(r'^(hi|hello|hey|hey there|good morning|good afternoon)$', clean):
        summary = f"I can summarize team reports. Found {total_reports} submitted report(s)."
        example = 'Try: "What blockers came up this week?" or "Show hours this week."'
        return f"Hi — {summary} {example}"

    # Small-talk: how are you -> give assistant status + short summary
    if "how are you" in clean or clean in ("how r u", "how are u"):
        status = "I'm the team reports assistant and I'm operational."
        if reporters_with_blockers:
            blk = ", ".join(sorted({r.get("user") for r in reporters_with_blockers}))
            return f"{status} There are blockers reported by: {blk}. Ask 'What blockers came up this week?' to see details."
        return f"{status} No blockers are reported in the available reports."

    answer_lines = []
    answer_lines.append(f"Found {total_reports} submitted report(s). Total hours reported: {total_hours}.")

    # Blocker-focused questions
    # if "blocker" in clean or "blockers" in clean:
    #     if blocker_lines:
    #         answer_lines.append("Recent blockers:")
    #         answer_lines.extend([f"- {b}" for b in blocker_lines[:10]])
    #         users = ", ".join(sorted({r.get("user") for r in reporters_with_blockers}))
    #         answer_lines.append(f"Recommend following up with: {users}.")
    #     else:
    #         answer_lines.append("I don't see any reported blockers in the available reports.")
    #     answer_lines.append("Action: Prioritize a quick sync with people reporting blockers.")
    #     return "\n".join(answer_lines)
    # Blocker-focused questions
    if "blocker" in clean or "blockers" in clean:
        if blocker_lines:
            # Clean up the blocker words into a tidy list
            unique_blockers = sorted(list({r.get('blockers') for r in reporters_with_blockers if r.get('blockers')}))
            blocker_list_str = ", ".join([f'"{b}"' for b in unique_blockers])
            users = ", ".join(sorted({r.get("user") for r in reporters_with_blockers}))
            
            return (
                f"**Current Status:** There are active blockers reported by **{users}**.\n"
                f"**Identified Hurdles:** {blocker_list_str}.\n"
                f"**Suggested Action:** Prioritize a quick sync with **{users}** to clarify these blockers, "
                f"as they appear to be miscategorized task statuses rather than operational impediments."
            )
        else:
            return "I don't see any reported blockers in the available weekly reports."

    # Hours/time questions
    if "hour" in clean or "time" in clean:
        answer_lines.append(f"Average hours per report: {total_hours / total_reports:.1f}.")
        return "\n".join(answer_lines)

    # Who/which questions
    if clean.startswith("who") or clean.startswith("which"):
        # if asking about blockers specifically
        if "blocker" in clean:
            if reporters_with_blockers:
                names = ", ".join(sorted({r.get("user") for r in reporters_with_blockers}))
                return f"Reporters with blockers: {names}."
            return "No reporters with blockers found."

    # Default: general summary of recent activity.
    answer_lines.append("Summary of recent activity:")
    for r in reports[:5]:
        blk = r.get("blockers") or "None"
        answer_lines.append(f"- {r.get('user')} (Project: {r.get('project')}) — Completed: {r.get('completed')}; Blockers: {blk}")

    if reporters_with_blockers:
        answer_lines.append("Action: Prioritize a quick sync with the people reporting blockers.")
    else:
        answer_lines.append("Action: No blockers reported; consider checking planned items for schedule risk.")

    return "\n".join(answer_lines)



def ask_gemini(context, message):
    """
    Send weekly report context + manager question to Gemini.
    Falls back to local summarizer if API limits are hit.
    """
    if not gemini_client:
        return _local_summarize(context, message)

    prompt = f"""
You are an AI assistant for a project manager.

Answer questions using ONLY the weekly reports below.

Weekly Reports:

{context}


Manager Question:

{message}


Rules:
- Give a clear concise answer.
- Mention team members if relevant.
- Identify blockers and risks.
- Suggest actions.
"""

    try:
        response = gemini_client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )
        return response.text

    except Exception:
        # If Gemini is busy, exhausted, or offline, seamlessly use your local code
        return _local_summarize(context, message)

# def ask_gemini(context, message):
#     """
#     Send weekly report context + manager question to Gemini
#     """

#     if not gemini_client:
#         return _local_summarize(context, message)

#     prompt = f"""
# You are an AI assistant for a project manager.

# Answer questions using ONLY the weekly reports below.

# Weekly Reports:

# {context}


# Manager Question:

# {message}


# Rules:
# - Give a clear concise answer.
# - Mention team members if relevant.
# - Identify blockers and risks.
# - Suggest actions.
# """

#     try:
#         response = gemini_client.models.generate_content(
#             model=GEMINI_MODEL,
#             contents=prompt
#         )

#         return response.text

#     except Exception as e:
#         return f"Gemini error: {str(e)}"

@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated, IsManager])
def chat(request):
    """
    Manager-only chat endpoint. Takes {"message": "...", "week": "YYYY-MM-DD"?, "project": id?}
    and answers using only the team's own report data (no report content ever leaves
    the request except what's sent to the configured LLM provider for this single call).
    """
    message = request.data.get("message", "").strip()
    if not message:
        return Response({"error": "message is required"}, status=400)

    context = _build_context(
        week_start=request.data.get("week"), project_id=request.data.get("project")
    )
    # Use only the local summarizer to provide reliable, instant answers.
    # This keeps the assistant functional even in environments without an
    # external LLM key or network access.
    answer = ask_gemini(context, message)
    return Response({"answer": answer, "context_used": context})
