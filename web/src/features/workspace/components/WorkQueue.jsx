import React, { useEffect, useState } from "react";

export default function WorkQueue({
  api,
  language,
  data,
}) {
  const [queue, setQueue] = useState({
    noThesis: 0,
    pendingTheses: 0,
    defenses: 0,
  });

  const ar = language === "ar";

  useEffect(() => {
    let active = true;

    async function loadQueue() {
      try {
        const requests = [
          api("/students/?thesis_status=NO_THESIS&page_size=1"),
          api("/theses/?status=SUBMITTED&page_size=1"),
        ];

        const results = await Promise.all(requests);

        if (!active) return;

        setQueue({
          noThesis: results[0]?.pagination?.total || 0,
          pendingTheses: results[1]?.pagination?.total || 0,
          defenses: 0,
        });

      } catch {
        if (active) {
          setQueue({
            noThesis: 0,
            pendingTheses: 0,
            defenses: 0,
          });
        }
      }
    }

    loadQueue();

    return () => {
      active = false;
    };
  }, [api]);


  return (
    <section className="workQueue">
      <header>
        <h3>
          {ar ? "قائمة العمل اليومية" : "Work Queue"}
        </h3>

        <p>
          {ar
            ? "المهام التي تحتاج متابعة من الموظف"
            : "Operational items requiring attention"}
        </p>
      </header>


      <div className="queueGrid">

        <div className="queueCard">
          <strong>{queue.noThesis}</strong>
          <span>
            {ar
              ? "طلاب بدون رسالة مسجلة"
              : "Students without thesis"}
          </span>
        </div>


        <div className="queueCard">
          <strong>{queue.pendingTheses}</strong>
          <span>
            {ar
              ? "رسائل تنتظر المراجعة"
              : "Theses awaiting review"}
          </span>
        </div>


        <div className="queueCard">
          <strong>{queue.defenses}</strong>
          <span>
            {ar
              ? "مناقشات تحتاج متابعة"
              : "Defense follow-ups"}
          </span>
        </div>

      </div>
    </section>
  );
}
