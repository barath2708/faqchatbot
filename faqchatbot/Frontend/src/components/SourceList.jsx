function SourceList({ sources }) {
  if (!sources || sources.length === 0) return null;

  return (
    <ul className="mt-3 flex flex-col gap-1.5">
      {sources.map((url) => (
        <li key={url} className="text-sm">
          <a href={url} target="_blank" rel="noopener noreferrer" className="text-edge hover:underline break-all font-mono text-xs">
            {url}
          </a>
        </li>
      ))}
    </ul>
  );
}

export default SourceList;
