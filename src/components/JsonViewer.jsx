import React, { useState } from "react";

const JsonViewer = ({ data, level = 0 }) => {
  const [expanded, setExpanded] = useState(true); // Initially all open

  if (typeof data !== "object" || data === null) {
    return <span className="text-white font-montserrat">{JSON.stringify(data)}</span>;
  }

  return (
    <div className="ml-4 border-l border-gray-500 pl-2">
      <button
        onClick={() => setExpanded(!expanded)}
        className="text-white font-bold mb-1 flex items-center"
      >
        <span className={`mr-1 ${expanded ? "rotate-90" : ""} transition-transform`}>
        ➤
        </span>
        {Array.isArray(data) ? "" : ""}
      </button>

      {expanded &&
        Object.entries(data).map(([key, value]) => (
          <div key={key} className="ml-4">
            <span className="text-cyan-200 font-bold font-montserrat">{key}:</span>{" "}
            <JsonViewer data={value} level={level + 1} />
          </div>
        ))}
    </div>
  );
};
export default JsonViewer;