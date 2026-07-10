"use client";
import { useEffect, useState } from "react";
import Navbar from "@/components/Navbar";
import api from "@/lib/api";

const EMPTY_FORM = {
  id: null,
  project: "",
  week_start: mondayOf(new Date()),
  tasks_completed: "",
  tasks_planned: "",
  blockers: "",
  hours_worked: "",
  notes: "",
  status: "draft",
};

function mondayOf(date) {
  const d = new Date(date);
  const day = d.getDay();
  const diff = d.getDate() - day + (day === 0 ? -6 : 1);
  const monday = new Date(d.setDate(diff));
  return monday.toISOString().slice(0, 10);
}

export default function ReportsPage() {
  const [reports, setReports] = useState([]);
  const [projects, setProjects] = useState([]);
  const [form, setForm] = useState(EMPTY_FORM);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  async function loadReports() {
    try {
      const { data } = await api.get("/reports/");
      setReports(data);
    } catch (err) {
      if (err.response?.status === 401 || err.response?.status === 403) return;
      console.error(err);
    }
  }

  async function loadProjects() {
    try {
      const { data } = await api.get("/projects/");
      setProjects(data);
    } catch (err) {
      if (err.response?.status === 401 || err.response?.status === 403) return;
      console.error(err);
    }
  }

  useEffect(() => {
    loadReports();
    loadProjects();
  }, []);

  function update(field) {
    return (e) => setForm({ ...form, [field]: e.target.value });
  }

  function editReport(r) {
    setForm({
      id: r.id,
      project: r.project || "",
      week_start: r.week_start,
      tasks_completed: r.tasks_completed,
      tasks_planned: r.tasks_planned,
      blockers: r.blockers,
      hours_worked: r.hours_worked || "",
      notes: r.notes,
      status: r.status,
    });
  }

  async function saveReport(status) {
    setError("");
    setSaving(true);
    const payload = {
      ...form,
      status,
      project: form.project || null,
      hours_worked: form.hours_worked || null,
    };
    try {
      if (form.id) {
        await api.patch(`/reports/${form.id}/`, payload);
      } else {
        await api.post("/reports/", payload);
      }
      setForm(EMPTY_FORM);
      loadReports();
    } catch (err) {
      const data = err.response?.data;
      setError(data ? JSON.stringify(data) : "Failed to save report.");
    } finally {
      setSaving(false);
    }
  }

  return (
    <div>
      <Navbar />
      <main className="max-w-5xl mx-auto p-6 grid md:grid-cols-2 gap-6">
        <section className="bg-white border rounded-xl p-6">
          <h2 className="font-semibold text-slate-800 mb-4">
            {form.id ? "Edit report" : "New weekly report"}
          </h2>
          {error && <p className="text-sm text-red-600 mb-3">{error}</p>}
          <div className="space-y-3">
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="text-xs text-slate-500">Week starting (Monday)</label>
                <input
                  type="date"
                  className="mt-1 w-full border rounded-lg px-3 py-2 text-sm"
                  value={form.week_start}
                  onChange={update("week_start")}
                />
              </div>
              <div>
                <label className="text-xs text-slate-500">Project / category</label>
                <select
                  className="mt-1 w-full border rounded-lg px-3 py-2 text-sm"
                  value={form.project}
                  onChange={update("project")}
                >
                  <option value="">— None —</option>
                  {projects.map((p) => (
                    <option key={p.id} value={p.id}>
                      {p.name}
                    </option>
                  ))}
                </select>
              </div>
            </div>
            <div>
              <label className="text-xs text-slate-500">Tasks completed</label>
              <textarea
                className="mt-1 w-full border rounded-lg px-3 py-2 text-sm"
                rows={3}
                value={form.tasks_completed}
                onChange={update("tasks_completed")}
              />
            </div>
            <div>
              <label className="text-xs text-slate-500">Tasks planned for next week</label>
              <textarea
                className="mt-1 w-full border rounded-lg px-3 py-2 text-sm"
                rows={3}
                value={form.tasks_planned}
                onChange={update("tasks_planned")}
              />
            </div>
            <div>
              <label className="text-xs text-slate-500">Blockers / challenges</label>
              <textarea
                className="mt-1 w-full border rounded-lg px-3 py-2 text-sm"
                rows={2}
                value={form.blockers}
                onChange={update("blockers")}
              />
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="text-xs text-slate-500">Hours worked (optional)</label>
                <input
                  type="number"
                  step="0.5"
                  className="mt-1 w-full border rounded-lg px-3 py-2 text-sm"
                  value={form.hours_worked}
                  onChange={update("hours_worked")}
                />
              </div>
              <div>
                <label className="text-xs text-slate-500">Notes / links (optional)</label>
                <input
                  className="mt-1 w-full border rounded-lg px-3 py-2 text-sm"
                  value={form.notes}
                  onChange={update("notes")}
                />
              </div>
            </div>
            <div className="flex gap-3 pt-2">
              <button
                disabled={saving}
                onClick={() => saveReport("draft")}
                className="px-4 py-2 text-sm rounded-lg border border-slate-300 text-slate-700 hover:bg-slate-50"
              >
                Save draft
              </button>
              <button
                disabled={saving}
                onClick={() => saveReport("submitted")}
                className="px-4 py-2 text-sm rounded-lg bg-brand-600 text-white hover:bg-brand-700"
              >
                Submit
              </button>
              {form.id && (
                <button
                  onClick={() => setForm(EMPTY_FORM)}
                  className="px-4 py-2 text-sm rounded-lg text-slate-500 hover:underline"
                >
                  Cancel edit
                </button>
              )}
            </div>
          </div>
        </section>

        <section>
          <h2 className="font-semibold text-slate-800 mb-4">My report history</h2>
          <div className="space-y-3">
            {reports.length === 0 && (
              <p className="text-sm text-slate-500">No reports yet — create your first one.</p>
            )}
            {reports.map((r) => (
              <div key={r.id} className="bg-white border rounded-xl p-4">
                <div className="flex justify-between items-start">
                  <div>
                    <p className="font-medium text-slate-800">Week of {r.week_start}</p>
                    <p className="text-xs text-slate-500">{r.project_name || "No project"}</p>
                  </div>
                  <div className="flex items-center gap-2">
                    <span
                      className={`text-xs px-2 py-1 rounded-full ${
                        r.status === "submitted"
                          ? "bg-green-100 text-green-700"
                          : "bg-amber-100 text-amber-700"
                      }`}
                    >
                      {r.status}
                    </span>
                    <button
                      onClick={() => editReport(r)}
                      className="text-xs text-brand-600 hover:underline"
                    >
                      Edit
                    </button>
                  </div>
                </div>
                <p className="text-sm text-slate-600 mt-2">
                  <span className="font-medium">Completed:</span> {r.tasks_completed || "—"}
                </p>
                {r.blockers && (
                  <p className="text-sm text-red-600 mt-1">
                    <span className="font-medium">Blockers:</span> {r.blockers}
                  </p>
                )}
              </div>
            ))}
          </div>
        </section>
      </main>
    </div>
  );
}
