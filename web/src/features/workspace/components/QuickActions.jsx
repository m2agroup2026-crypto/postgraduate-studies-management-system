import React from "react";
import { BookOpen, CalendarClock, FileSearch, Search, UserRoundX } from "lucide-react";

const ACTIONS = [
  { key: "search_student", permission: "students.view", icon: Search, ar: "البحث عن طالب", en: "Find a student" },
  { key: "search_thesis", permission: "theses.view", icon: BookOpen, ar: "البحث عن رسالة", en: "Find a thesis" },
  { key: "no_thesis", permission: "students.view", icon: UserRoundX, ar: "طلاب بدون رسالة", en: "Students without thesis" },
  { key: "pending_review", permission: "theses.view", icon: FileSearch, ar: "رسائل تنتظر المراجعة", en: "Theses awaiting review" },
  { key: "upcoming_defenses", permission: "committees.view", icon: CalendarClock, ar: "مناقشات قادمة", en: "Upcoming defenses" },
];

export default function QuickActions({ language = "ar", permissions = [], activeAction, onAction }) {
  const ar = language === "ar";
  const allowed = new Set(permissions);
  const actions = ACTIONS.filter((action) => allowed.has(action.permission));

  return (
    <div className="workspaceQuickActions" aria-label={ar ? "إجراءات سريعة" : "Quick actions"}>
      {actions.map((action) => {
        const Icon = action.icon;
        return (
          <button
            key={action.key}
            type="button"
            className={activeAction === action.key ? "active" : ""}
            onClick={() => onAction(action.key)}
            aria-pressed={activeAction === action.key}
          >
            <span aria-hidden="true"><Icon size={18} /></span>
            <strong>{ar ? action.ar : action.en}</strong>
          </button>
        );
      })}
    </div>
  );
}
