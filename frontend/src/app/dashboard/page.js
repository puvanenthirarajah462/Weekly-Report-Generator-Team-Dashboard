"use client";
import { useEffect, useState } from "react";
import {
  LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, PieChart, Pie, Cell, Legend,
} from "recharts";
import Navbar from "@/components/Navbar";
import AiChatWidget from "@/components/AiChatWidget";
import api from "@/lib/api";

const COLORS = ["#4f46e5", "#6366f1", "#818cf8", "#a5b4fc", "#c7d2fe", "#e0e7ff"];

function mondayOf(date) {
  const d = new Date(date);
  const day = d.getDay();
  const diff = d.getDate() - day + (day === 0 ? -6 : 1);
  return new Date(d.setDate(diff)).toISOString().slice(0, 10);
}

export default function DashboardPage() {
  const [summary, setSummary] = useState(null);
  const [reports, setReports] = useState([]);
  const [projects, setProjects] = useState([]);
  const [members, setMembers] = useState([]);
  const [filters, setFilters] = useState({
    week: mondayOf(new Date()),
    user: "",
    project: "",
    start: "",
    end: "",
  });

  async function loadSummary(week) {
    try {
      const { data } = await api.get(`/reports/dashboard/summary/?week=${week}`);
      setSummary(data);
    } catch (err) {
      if (err.response?.status === 401 || err.response?.status === 403) return;
      console.error(err);
    }
  }

  async function loadReports() {
    try {
      const params = new URLSearchParams();
      Object.entries(filters).forEach(([k, v]) => {
        if (v && k !== "week") params.set(k, v);
      });
      // Only filter by exact week if no date range is set
      if (filters.week && !filters.start && !filters.end) params.set("week", filters.week);
      const { data } = await api.get(`/reports/?${params.toString()}`);
      setReports(data);
    } catch (err) {
      if (err.response?.status === 401 || err.response?.status === 403) return;
      console.error(err);
    }
  }

  async function loadMeta() {
    try {
      const [p, u] = await Promise.all([api.get("/projects/"), api.get("/auth/users/")]);
      setProjects(p.data);
      setMembers(u.data.filter((m) => m.role === "team_member"));
    } catch (err) {
      if (err.response?.status === 401 || err.response?.status === 403) return;
      console.error(err);
    }
  }

  useEffect(() => {
    loadMeta();
  }, []);

  useEffect(() => {
    loadSummary(filters.week);
    loadReports();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filters]);

  function updateFilter(field) {
    return (e) => setFilters({ ...filters, [field]: e.target.value });
  }

  return (
    <div>
      <Navbar />
      <main className="max-w-6xl mx-auto p-6 space-y-6">
        <section className="bg-white border rounded-xl p-4 flex flex-wrap gap-4 items-end">
          <div>
            <label className="text-xs text-slate-500 block">Week</label>
            <input type="date" className="border rounded-lg px-3 py-2 text-sm" value={filters.week} onChange={updateFilter("week")} />
          </div>
          <div>
            <label className="text-xs text-slate-500 block">Team member</label>
            <select className="border rounded-lg px-3 py-2 text-sm" value={filters.user} onChange={updateFilter("user")}>
              <option value="">All</option>
              {members.map((m) => (
                <option key={m.id} value={m.id}>{m.username}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="text-xs text-slate-500 block">Project</label>
            <select className="border rounded-lg px-3 py-2 text-sm" value={filters.project} onChange={updateFilter("project")}>
              <option value="">All</option>
              {projects.map((p) => (
                <option key={p.id} value={p.id}>{p.name}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="text-xs text-slate-500 block">From</label>
            <input type="date" className="border rounded-lg px-3 py-2 text-sm" value={filters.start} onChange={updateFilter("start")} />
          </div>
          <div>
            <label className="text-xs text-slate-500 block">To</label>
            <input type="date" className="border rounded-lg px-3 py-2 text-sm" value={filters.end} onChange={updateFilter("end")} />
          </div>
        </section>

        {summary && (
          <section className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <MetricCard label="Reports submitted (selected week)" value={`${summary.summary.total_submitted}/${summary.summary.total_expected}`} />
            <MetricCard label="Submission compliance" value={`${summary.summary.compliance_rate}%`} />
            <MetricCard label="Open blockers" value={summary.summary.open_blockers} accent="text-red-600" />
          </section>
        )}

        {summary && (
          <section className="grid md:grid-cols-2 gap-6">
            <div className="bg-white border rounded-xl p-4">
              <h3 className="text-sm font-medium text-slate-700 mb-3">Reports submitted — last 8 weeks</h3>
              <ResponsiveContainer width="100%" height={220}>
                <LineChart data={summary.trend}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="week" tick={{ fontSize: 11 }} />
                  <YAxis allowDecimals={false} />
                  <Tooltip />
                  <Line type="monotone" dataKey="reports_submitted" stroke="#4f46e5" strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
            </div>

            <div className="bg-white border rounded-xl p-4">
              <h3 className="text-sm font-medium text-slate-700 mb-3">Submission status by team member (selected week)</h3>
              <ResponsiveContainer width="100%" height={220}>
                <BarChart data={summary.status_by_member} layout="vertical">
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis type="number" hide />
                  <YAxis type="category" dataKey="user" tick={{ fontSize: 11 }} width={80} />
                  <Tooltip />
                  <Bar dataKey={(d) => (d.status === "submitted" ? 1 : 0)} fill="#4f46e5" name="Submitted" />
                </BarChart>
              </ResponsiveContainer>
            </div>

            <div className="bg-white border rounded-xl p-4">
              <h3 className="text-sm font-medium text-slate-700 mb-3">Workload distribution by project</h3>
              <ResponsiveContainer width="100%" height={220}>
                <PieChart>
                  <Pie data={summary.workload_by_project} dataKey="count" nameKey="project" outerRadius={80} label>
                    {summary.workload_by_project.map((entry, i) => (
                      <Cell key={i} fill={COLORS[i % COLORS.length]} />
                    ))}
                  </Pie>
                  <Legend />
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>

            <div className="bg-white border rounded-xl p-4">
              <h3 className="text-sm font-medium text-slate-700 mb-3">Recent activity</h3>
              <ul className="space-y-2 text-sm text-slate-600 max-h-56 overflow-y-auto">
                {summary.recent_activity.map((a, i) => (
                  <li key={i} className="border-b pb-2">
                    <span className="font-medium text-slate-800">{a.user}</span> submitted a report for{" "}
                    <span className="text-slate-500">{a.project || "no project"}</span> (week {a.week_start})
                  </li>
                ))}
                {summary.recent_activity.length === 0 && <li>No activity yet.</li>}
              </ul>
            </div>
          </section>
        )}

        <section className="bg-white border rounded-xl">
          <h3 className="text-sm font-medium text-slate-700 px-4 pt-4">Filtered reports</h3>
          <div className="divide-y">
            {reports.map((r) => (
              <div key={r.id} className="px-4 py-3 flex justify-between items-start">
                <div>
                  <p className="text-sm font-medium text-slate-800">
                    {r.username} — week of {r.week_start}
                    <span className="text-xs text-slate-400 ml-2">{r.project_name || "No project"}</span>
                  </p>
                  <p className="text-sm text-slate-600">{r.tasks_completed || "—"}</p>
                  {r.blockers && <p className="text-sm text-red-600">Blocker: {r.blockers}</p>}
                </div>
                <span
                  className={`text-xs px-2 py-1 rounded-full ${
                    r.status === "submitted" ? "bg-green-100 text-green-700" : "bg-amber-100 text-amber-700"
                  }`}
                >
                  {r.status}
                </span>
              </div>
            ))}
            {reports.length === 0 && <p className="px-4 py-4 text-sm text-slate-500">No reports match these filters.</p>}
          </div>
        </section>
      </main>
      <AiChatWidget />
    </div>
  );
}

function MetricCard({ label, value, accent }) {
  return (
    <div className="bg-white border rounded-xl p-5">
      <p className="text-xs text-slate-500">{label}</p>
      <p className={`text-2xl font-semibold mt-1 ${accent || "text-slate-800"}`}>{value}</p>
    </div>
  );
}
