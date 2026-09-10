import React from "react";
import { GraduationCap } from "lucide-react";

export default function StudentFileCard({
  record,
  thesisStatus,
  labels,
}) {
  return (
    <article className="studentFileRow" role="row">
      <span className="studentFileIcon">
        <GraduationCap size={19} />
      </span>

      <div className="studentFileIdentity">
        <strong>{record.name_ar}</strong>

        <small>
          {record.university_id} · {record.enrollments_count} {labels.enrollments}
        </small>
      </div>

      <span>{record.department}</span>

      <span>{thesisStatus}</span>

      <span className="recordSource">
        {labels.source}
      </span>
    </article>
  );
}
