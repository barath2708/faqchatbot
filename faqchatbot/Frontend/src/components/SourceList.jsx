function SourceList({ sources }) {
  if (!sources || sources.length === 0) return null;

  return (
    <ul className="mt-3 flex flex-col gap-1">
      {sources.map((url) => (
        <li key={url} className="text-sm">
          <a
          href={url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-500 hover:underline break-all"
          >
            {url}
          </a>
        </li>
      ))}
    </ul>
  );
}

export default SourceList;