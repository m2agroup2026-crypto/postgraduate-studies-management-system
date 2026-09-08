import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";

import { api, hasSession, login, logout } from "./api";

import Header from "./components/Header";
import AIAssistant from "./features/assistant/AIAssistant";
import Dashboard from "./features/dashboard/Dashboard";
import DashboardSettings from "./features/settings/DashboardSettings";
import StudentsModule from "./features/students/StudentsModule";
import ThesesModule from "./features/theses/ThesesModule";
import DashboardLayout from "./layouts/DashboardLayout";

import "./styles.css";
import "./auth.css";


function Login({ onSuccess }) {
  const [u, setU] = useState("director");
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
        <div className="loginMark">PG</div>
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


function SectionPlaceholder({ section, language }) {
  const ar = language === "ar";
  return (
    <div className="panel sectionPlaceholder">
      <small>{ar ? "وحدة مستقلة قابلة للتوسع" : "Modular workspace"}</small>
      <h2>{section?.label_ar || section?.label_en || section?.key}</h2>
      <p>
        {ar
          ? "تم تجهيز التنقل لهذه الوحدة، وسيتم ربط وظائفها وشاشاتها التشغيلية في مراحل التنفيذ التالية دون التأثير على لوحة القيادة الرئيسية."
          : "Navigation is ready for this module. Its operational screens will be connected in the next implementation stages without affecting the main dashboard."}
      </p>
    </div>
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
  const activeNavigation = navigation.find((item) => item.key === activeSection);

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
  } else if (activeSection === "overview" || !activeNavigation) {
    content = <Dashboard data={data} language={lang} />;
  } else {
    content = <SectionPlaceholder section={activeNavigation} language={lang} />;
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

      <AIAssistant api={api} />
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
