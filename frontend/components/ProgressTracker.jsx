import { useState, useEffect } from 'react';

export default function ProgressTracker({ jobId, onComplete, onError }) {
  const [progress, setProgress] = useState({});
  const [overallStatus, setOverallStatus] = useState('pending');
  const [lastUpdate, setLastUpdate] = useState(null);
  
  useEffect(() => {
    if (!jobId) return;
    
    const interval = setInterval(() => {
      fetch(`/api/job-status/${jobId}`)
        .then(response => {
          if (!response.ok) {
            throw new Error('Failed to fetch job status');
          }
          return response.json();
        })
        .then(data => {
          setProgress(data.progress || {});
          setOverallStatus(data.status || 'pending');
          setLastUpdate(new Date());
          
          if (data.status === 'completed') {
            clearInterval(interval);
            onComplete(data.results);
          } else if (data.status === 'failed') {
            clearInterval(interval);
            onError(data.message || 'Job failed');
          }
        })
        .catch(error => {
          console.error('Progress tracking error:', error);
          clearInterval(interval);
          onError('Failed to track job progress');
        });
    }, 5000);
    
    return () => clearInterval(interval);
  }, [jobId, onComplete, onError]);
  
  const getStatusColor = (status) => {
    switch (status) {
      case 'completed': return 'bg-green-100 text-green-800';
      case 'failed': return 'bg-red-100 text-red-800';
      case 'processing': return 'bg-blue-100 text-blue-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-semibold text-gray-700">
          Processing Job: <span className="font-mono text-sm">{jobId}</span>
        </h2>
        <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(overallStatus)}`}>
          {overallStatus.toUpperCase()}
        </span>
      </div>
      
      <div className="space-y-3">
        {Object.entries(progress).map(([url, { status, message }]) => (
          <div key={url} className="p-3 bg-gray-50 rounded-md border border-gray-200">
            <div className="flex justify-between">
              <div className="truncate pr-2" title={url}>
                {url}
              </div>
              <span className={`px-2 py-1 rounded text-xs font-medium ${getStatusColor(status)}`}>
                {status.toUpperCase()}
              </span>
            </div>
            {message && (
              <div className="mt-1 text-xs text-gray-500">
                {message}
              </div>
            )}
          </div>
        ))}
      </div>
      
      {overallStatus === 'processing' && (
        <div className="mt-4">
          <div className="flex items-center text-sm text-gray-500">
            <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Checking for updates...
          </div>
        </div>
      )}
    </div>
  );
}
