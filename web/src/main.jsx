import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";

import { api, hasSession, login, logout } from "./api";

import Header from "./components/Header";
import logo from "./assets/logo.webp";
import AIAssistant from "./features/assistant/AIAssistant";
import CommitteesModule from "./features/committees/CommitteesModule";
import Dashboard from "./features/dashboard/Dashboard";
import DashboardSettings from "./features/settings/DashboardSettings";
import StudentsModule from "./features/students/StudentsModule";
import ThesesModule from "./features/theses/ThesesModule";
import DashboardLayout from "./layouts/DashboardLayout";

import "./styles.css";
import "./auth.css";
import "./features/committees/committees.css";


function Login({ onSuccess }) {
  const [u, setU] = useState("vice_dean");
  const [p, setP] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    setBusy(true);
    setError("");

    try {
      await login(u, p);
      onSuccess();
    } catch (x) {
      setError(x.message);
    } finally {
      setBusy(false);
    }
  };

  return (
    <main className="loginPage" dir="rtl">
      <form className="loginCard" onSubmit={submit}>
        <div className="loginLogo"><img src={logo} alt="Faculty of Medicine - Assiut University" /></div>
        <small>POSTGRADUATE STUDIES</small>
        <h1>تسجيل الدخول</h1>
        <p>منظومة إدارة الدراسات العليا – كلية الطب</p>

        <label>
          اسم المستخدم
          <input value={u} onChange={(e) => setU(e.target.value)} />
        </label>

        <label>
          كلمة المرور
          <input type="password" value={p} onChange={(e) => setP(e.target.value)} />
        </label>

        {error && <div className="error">{error}</div>}

        <button disabled={busy}>
          {busy ? "جارٍ التحقق..." : "دخول آمن"}
        </button>
      </form>
    </main>
  );
}


function DashboardPage() {
  const [user, setUser] = useState(null);
  const [data, setData] = useState(null);
  const [lang, setLang] = useState("ar");
  const [activeSection, setActiveSection] = useState("overview");
  const [error, setError] = useState("");

  const refreshDashboard = async () => {
    const next = await api("/dashboard/");
    setData(next);
    return next;
  };

  useEffect(() => {
    Promise.all([api("/me/"), api("/dashboard/")])
      .then(([me, dashboard]) => {
        setUser(me);
        setLang(me.language || "ar");
        setData(dashboard);
      })
      .catch((e) => setError(e.message));
  }, []);

  if (error) {
    return (
      <div className="fatal" dir="rtl">
        <h2>تعذر تحميل النظام</h2>
        <p>{error}</p>
        <button onClick={() => { logout(); location.reload(); }}>
          العودة لتسجيل الدخول
        </button>
      </div>
    );
  }

  if (!user || !data) {
    return <div className="loading" dir="rtl">جارٍ تحميل لوحة التحكم…</div>;
  }

  const navigation = data.ui?.navigation || [];

  let content;
  if (activeSection === "settings" && user.can_manage_dashboard) {
    content = (
      <DashboardSettings
        api={api}
        language={lang}
        onSaved={refreshDashboard}
      />
    );
  } else if (activeSection === "students") {
    content = <StudentsModule api={api} language={lang} />;
  } else if (activeSection === "theses") {
    content = <ThesesModule api={api} language={lang} />;
  } else if (activeSection === "committees") {
    content = <CommitteesModule api={api} language={lang} />;
  } else {
    content = <Dashboard data={data} language={lang} onNavigate={setActiveSection} />;
  }

  return (
    <DashboardLayout
      language={lang}
      navigation={navigation}
      activeSection={activeSection}
      onNavigate={setActiveSection}
    >
      <Header
        user={user}
        language={lang}
        onLanguageChange={() => setLang(lang === "ar" ? "en" : "ar")}
        onLogout={() => { logout(); location.reload(); }}
      />

      {content}

      <AIAssistant
        api={api}
        actions={data.assistant?.quick_actions || []}
        onNavigate={setActiveSection}
      />
    </DashboardLayout>
  );
}


function App() {
  const [authenticated, setAuthenticated] = useState(hasSession());
  return authenticated
    ? <DashboardPage />
    : <Login onSuccess={() => setAuthenticated(true)} />;
}


createRoot(document.getElementById("root")).render(<App />);
