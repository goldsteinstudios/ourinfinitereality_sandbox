export function Loading() {
  return (
    <div className="flex items-center justify-center h-screen bg-gray-900">
      <div className="text-center">
        <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-500 mx-auto mb-4"></div>
        <p className="text-gray-400">Loading Dao De Jing data...</p>
      </div>
    </div>
  );
}

export function ErrorDisplay({ message }: { message: string }) {
  return (
    <div className="flex items-center justify-center h-screen bg-gray-900">
      <div className="text-center max-w-md">
        <div className="text-red-500 text-5xl mb-4">⚠</div>
        <h2 className="text-xl font-bold text-white mb-2">Error Loading Data</h2>
        <p className="text-gray-400">{message}</p>
      </div>
    </div>
  );
}
