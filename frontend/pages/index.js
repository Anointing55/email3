import { useState, useCallback } from 'react';
import Head from 'next/head';
import UrlInput from '../components/UrlInput';
import ProgressTracker from '../components/ProgressTracker';
import ResultsTable from '../components/ResultsTable';
import ExportControls from '../components/ExportControls';

export default function Home() {
  const [jobId, setJobId] = useState(null);
  const [results, setResults] = useState(null);
  
  const handleSubmit = useCallback(async (urls) => {
    try {
      const response = await fetch('/api/submit-urls', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ urls })
      });
      
      if (!response.ok) {
        throw new Error('Failed to submit URLs');
      }
      
      const data = await response.json();
      setJobId(data.jobId);
      setResults(null);
    } catch (error) {
      console.error('Submission error:', error);
      alert(`Error: ${error.message}`);
    }
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      <Head>
        <title>Contact & Social Media Extractor</title>
        <meta name="description" content="Extract contact info from websites" />
      </Head>

      <main className="container mx-auto px-4 py-8">
        <div className="max-w-6xl mx-auto bg-white rounded-xl shadow-md overflow-hidden">
          <div className="p-8">
            <h1 className="text-3xl font-bold text-center text-gray-800 mb-2">
              Contact & Social Media Extractor
            </h1>
            <p className="text-center text-gray-600 mb-8">
              Extract emails and social media links from websites
            </p>
            
            {!jobId ? (
              <UrlInput onSubmit={handleSubmit} />
            ) : (
              <div className="space-y-6">
                <ProgressTracker 
                  jobId={jobId} 
                  onComplete={setResults} 
                  onError={(error) => alert(`Job failed: ${error}`)}
                />
                
                {results && (
                  <div className="mt-8">
                    <div className="flex justify-between items-center mb-4">
                      <h2 className="text-xl font-semibold text-gray-700">
                        Extraction Results
                      </h2>
                      <ExportControls jobId={jobId} />
                    </div>
                    <ResultsTable data={results} />
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </main>

      <footer className="mt-12 text-center text-gray-500 text-sm py-6">
        <p>© {new Date().getFullYear()} Contact Extractor Tool</p>
      </footer>
    </div>
  );
}
