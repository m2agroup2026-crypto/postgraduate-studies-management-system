import { localized } from "../../../i18n";
import React, { useState } from "react";

export default function UniversalSearch({
  api,
  language,
}) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  const ar = language === "ar";

  const search = async () => {
    if (!query.trim()) {
      setResults([]);
      return;
    }

    try {
      const [students, theses] = await Promise.all([
        api(`/students/?q=${encodeURIComponent(query)}&page_size=5`),
        api(`/theses/?q=${encodeURIComponent(query)}&page_size=5`),
      ]);

      setResults([
        ...(students.results || []).map((item) => ({
          type: ar ? "طالب" : "Student",
          title: localized(item, "name", language),
          id: item.id,
        })),
        ...(theses.results || []).map((item) => ({
          type: ar ? "رسالة" : "Thesis",
          title: localized(item, "title", language),
          id: item.id,
        })),
      ]);

    } catch {
      setResults([]);
    }
  };


  return (
    <section className="universalSearch">

      <input
        value={query}
        onChange={(e)=>setQuery(e.target.value)}
        placeholder={
          ar
            ? "بحث باسم الطالب أو الرقم الجامعي أو الرسالة..."
            : "Search student, ID, or thesis..."
        }
      />

      <button onClick={search}>
        {ar ? "بحث" : "Search"}
      </button>


      {results.length > 0 && (
        <div className="searchResults">
          {results.map((item,index)=>(
            <div key={index} className="searchResult">
              <small>{item.type}</small>
              <strong>{item.title}</strong>
            </div>
          ))}
        </div>
      )}

    </section>
  );
}
