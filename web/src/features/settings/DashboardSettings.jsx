import React, { useEffect, useState } from "react";

function updateByKey(items, key, field, value) {
  return items.map((item) => item.key === key ? { ...item, [field]: value } : item);
}

export default function DashboardSettings({ api, language = "ar", onSaved }) {
  const [navigation, setNavigation] = useState([]);
  const [metrics, setMetrics] = useState([]);
  const [busy, setBusy] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const ar = language === "ar";

  useEffect(() => {
    api("/dashboard/configuration/")
      .then((data) => {
        setNavigation(data.navigation || []);
        setMetrics(data.metrics || []);
      })
      .catch((e) => setError(e.message))
      .finally(() => setBusy(false));
  }, [api]);

  const save = async () => {
    setSaving(true);
    setError("");
    setMessage("");
    try {
      const data = await api("/dashboard/configuration/", {
        method: "PATCH",
        body: JSON.stringify({ navigation, metrics }),
      });
      setNavigation(data.navigation || []);
      setMetrics(data.metrics || []);
      setMessage(ar ? "تم حفظ إعدادات لوحة التحكم بنجاح" : "Dashboard configuration saved successfully");
      onSaved?.();
    } catch (e) {
      setError(e.message);
    } finally {
      setSaving(false);
    }
  };

  if (busy) {
    return <div className="panel settingsPanel">{ar ? "جارٍ تحميل الإعدادات…" : "Loading settings…"}</div>;
  }

  return (
    <section className="settingsPage">
      <div className="settingsHeading">
        <div>
          <small>{ar ? "إدارة بدون تعديل الكود" : "No-code administration"}</small>
          <h2>{ar ? "إعدادات لوحة التحكم" : "Dashboard settings"}</h2>
          <p>{ar ? "عدّل أسماء وترتيب وظهور عناصر القائمة والبطاقات ثم احفظ مباشرة." : "Edit labels, order and visibility of navigation and metric cards, then save directly."}</p>
        </div>
        <button type="button" onClick={save} disabled={saving}>
          {saving ? (ar ? "جارٍ الحفظ…" : "Saving…") : (ar ? "حفظ التغييرات" : "Save changes")}
        </button>
      </div>

      {error && <div className="settingsNotice error">{error}</div>}
      {message && <div className="settingsNotice success">{message}</div>}

      <div className="panel settingsPanel">
        <div className="paneltitle">
          <h3>{ar ? "القائمة الجانبية" : "Sidebar navigation"}</h3>
        </div>
        <div className="settingsRows">
          {navigation.map((item) => (
            <div className="settingsRow" key={item.key}>
              <div className="settingsKey">{item.key}</div>
              <label>
                {ar ? "العربية" : "Arabic"}
                <input
                  value={item.label_ar}
                  onChange={(e) => setNavigation(updateByKey(navigation, item.key, "label_ar", e.target.value))}
                />
              </label>
              <label>
                English
                <input
                  value={item.label_en || ""}
                  onChange={(e) => setNavigation(updateByKey(navigation, item.key, "label_en", e.target.value))}
                />
              </label>
              <label className="smallField">
                {ar ? "الترتيب" : "Order"}
                <input
                  type="number"
                  min="0"
                  value={item.sort_order}
                  onChange={(e) => setNavigation(updateByKey(navigation, item.key, "sort_order", Number(e.target.value)))}
                />
              </label>
              <label className="toggleField">
                <input
                  type="checkbox"
                  checked={item.is_active}
                  onChange={(e) => setNavigation(updateByKey(navigation, item.key, "is_active", e.target.checked))}
                />
                {ar ? "ظاهر" : "Visible"}
              </label>
            </div>
          ))}
        </div>
      </div>

      <div className="panel settingsPanel">
        <div className="paneltitle">
          <h3>{ar ? "بطاقات المؤشرات" : "Metric cards"}</h3>
        </div>
        <div className="settingsRows">
          {metrics.map((item) => (
            <div className="settingsRow metricSetting" key={item.key}>
              <div className="settingsKey">{item.key}</div>
              <label>
                {ar ? "العربية" : "Arabic"}
                <input
                  value={item.label_ar}
                  onChange={(e) => setMetrics(updateByKey(metrics, item.key, "label_ar", e.target.value))}
                />
              </label>
              <label>
                English
                <input
                  value={item.label_en || ""}
                  onChange={(e) => setMetrics(updateByKey(metrics, item.key, "label_en", e.target.value))}
                />
              </label>
              <label className="smallField">
                {ar ? "الترتيب" : "Order"}
                <input
                  type="number"
                  min="0"
                  value={item.sort_order}
                  onChange={(e) => setMetrics(updateByKey(metrics, item.key, "sort_order", Number(e.target.value)))}
                />
              </label>
              <label className="toggleField">
                <input
                  type="checkbox"
                  checked={item.is_active}
                  onChange={(e) => setMetrics(updateByKey(metrics, item.key, "is_active", e.target.checked))}
                />
                {ar ? "ظاهر" : "Visible"}
              </label>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
