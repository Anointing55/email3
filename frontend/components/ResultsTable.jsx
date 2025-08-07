import { useState, useMemo } from 'react';
import { format } from 'date-fns';

export default function ResultsTable({ data }) {
  const [filter, setFilter] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [selectedSite, setSelectedSite] = useState(null);
  const itemsPerPage = 10;
  
  // Flatten data for table
  const tableData = useMemo(() => {
    return Object.entries(data).map(([url, result]) => ({
      url,
      emails: result.emails,
      facebook: result.facebook,
      instagram: result.instagram,
      tiktok: result.tiktok,
      screenshot: result.screenshots?.homepage,
      timestamp: result.timestamp
    }));
  }, [data]);
  
  // Apply filtering
  const filteredData = useMemo(() => {
    if (!filter) return tableData;
    
    const lowerFilter = filter.toLowerCase();
    return tableData.filter(item => 
      item.url.toLowerCase().includes(lowerFilter) ||
      item.emails.some(email => email.toLowerCase().includes(lowerFilter)) ||
      item.facebook.some(fb => fb.toLowerCase().includes(lowerFilter)) ||
      item.instagram.some(ig => ig.toLowerCase().includes(lowerFilter)) ||
      item.tiktok.some(tt => tt.toLowerCase().includes(lowerFilter))
    );
  }, [tableData, filter]);
  
  // Pagination
  const totalPages = Math.ceil(filteredData.length / itemsPerPage);
  const currentItems = filteredData.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );
  
  const renderSocialLinks = (links) => {
    if (links.length === 0) return '-';
    
    return (
      <div className="space-y-1">
        {links.map((link, index) => (
          <a 
            key={index}
            href={link}
            target="_blank"
            rel="noopener noreferrer"
            className="block text-blue-600 hover:underline truncate"
          >
            {link}
          </a>
        ))}
      </div>
    );
  };

  return (
    <div className="overflow-hidden shadow ring-1 ring-black ring-opacity-5 rounded-lg">
      <div className="bg-white">
        <div className="px-4 py-5 sm:px-6 flex justify-between items-center">
          <div>
            <h3 className="text-lg font-medium text-gray-900">
              Extraction Results
            </h3>
            <p className="mt-1 text-sm text-gray-500">
              {filteredData.length} websites processed
            </p>
          </div>
          
          <div className="flex space-x-2">
            <input
              type="text"
              placeholder="Filter results..."
              className="border border-gray-300 rounded-md px-3 py-1 text-sm"
              value={filter}
              onChange={(e) => {
                setFilter(e.target.value);
                setCurrentPage(1);
              }}
            />
          </div>
        </div>
        
        <div className="border-t border-gray-200">
          <table className="min-w-full divide-y divide-gray-300">
            <thead className="bg-gray-50">
              <tr>
                <th scope="col" className="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-6">
                  Website
                </th>
                <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                  Emails
                </th>
                <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                  Facebook
                </th>
                <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                  Instagram
                </th>
                <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                  TikTok
                </th>
                <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                  Screenshot
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200 bg-white">
              {currentItems.map((item) => (
                <tr key={item.url} className="hover:bg-gray-50">
                  <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm sm:pl-6">
                    <div className="font-medium text-gray-900">{item.url}</div>
                    <div className="text-gray-500 text-xs mt-1">
                      {format(new Date(item.timestamp), 'MMM d, yyyy h:mm a')}
                    </div>
                  </td>
                  <td className="whitespace-normal px-3 py-4 text-sm text-gray-500">
                    {item.emails.length > 0 ? (
                      <ul className="list-disc pl-5 space-y-1">
                        {item.emails.map((email, index) => (
                          <li key={index}>
                            <a 
                              href={`mailto:${email}`}
                              className="text-blue-600 hover:underline"
                            >
                              {email}
                            </a>
                          </li>
                        ))}
                      </ul>
                    ) : (
                      <span className="text-gray-400">None found</span>
                    )}
                  </td>
                  <td className="whitespace-normal px-3 py-4 text-sm text-gray-500">
                    {renderSocialLinks(item.facebook)}
                  </td>
                  <td className="whitespace-normal px-3 py-4 text-sm text-gray-500">
                    {renderSocialLinks(item.instagram)}
                  </td>
                  <td className="whitespace-normal px-3 py-4 text-sm text-gray-500">
                    {renderSocialLinks(item.tiktok)}
                  </td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                    {item.screenshot ? (
                      <button
                        onClick={() => setSelectedSite(item)}
                        className="text-blue-600 hover:underline"
                      >
                        View
                      </button>
                    ) : (
                      <span className="text-gray-400">None</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        
        {/* Pagination */}
        <div className="flex items-center justify-between border-t border-gray-200 px-4 py-3 sm:px-6">
          <div className="flex flex-1 justify-between sm:hidden">
            <button
              onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
              disabled={currentPage === 1}
              className="relative inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50"
            >
              Previous
            </button>
            <button
              onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
              disabled={currentPage === totalPages}
              className="relative ml-3 inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50"
            >
              Next
            </button>
          </div>
          <div className="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between">
            <div>
              <p className="text-sm text-gray-700">
                Showing <span className="font-medium">{(currentPage - 1) * itemsPerPage + 1}</span> to{' '}
                <span className="font-medium">
                  {Math.min(currentPage * itemsPerPage, filteredData.length)}
                </span>{' '}
                of <span className="font-medium">{filteredData.length}</span> results
              </p>
            </div>
            <div>
              <nav className="isolate inline-flex -space-x-px rounded-md shadow-sm" aria-label="Pagination">
                <button
                  onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                  disabled={currentPage === 1}
                  className="relative inline-flex items-center rounded-l-md px-2 py-2 text-gray-400 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0 disabled:opacity-50"
                >
                  <span className="sr-only">Previous</span>
                  <svg className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                    <path fillRule="evenodd" d="M12.79 5.23a.75.75 0 01-.02 1.06L8.832 10l3.938 3.71a.75.75 0 11-1.04 1.08l-4.5-4.25a.75.75 0 010-1.08l4.5-4.25a.75.75 0 011.06.02z" clipRule="evenodd" />
                  </svg>
                </button>
                
                {Array.from({ length: totalPages }, (_, i) => i + 1).map(page => (
                  <button
                    key={page}
                    onClick={() => setCurrentPage(page)}
                    className={`relative inline-flex items-center px-4 py-2 text-sm font-semibold ${
                      currentPage === page 
                        ? 'z-10 bg-blue-600 text-white focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600'
                        : 'text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:outline-offset-0'
                    }`}
                  >
                    {page}
                  </button>
                ))}
                
                <button
                  onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
                  disabled={currentPage === totalPages}
                  className="relative inline-flex items-center rounded-r-md px-2 py-2 text-gray-400 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0 disabled:opacity-50"
                >
                  <span className="sr-only">Next</span>
                  <svg className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                    <path fillRule="evenodd" d="M7.21 14.77a.75.75 0 01.02-1.06L11.168 10 7.23 6.29a.75.75 0 111.04-1.08l4.5 4.25a.75.75 0 010 1.08l-4.5 4.25a.75.75 0 01-1.06-.02z" clipRule="evenodd" />
                  </svg>
                </button>
              </nav>
            </div>
          </div>
        </div>
      </div>
      
      {/* Screenshot Modal */}
      {selectedSite && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-auto">
            <div className="p-4 border-b flex justify-between items-center">
              <h3 className="text-lg font-medium">{selectedSite.url}</h3>
              <button
                onClick={() => setSelectedSite(null)}
                className="text-gray-500 hover:text-gray-700"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <div className="p-4">
              {selectedSite.screenshot ? (
                <img 
                  src={selectedSite.screenshot} 
                  alt={`Screenshot of ${selectedSite.url}`}
                  className="w-full h-auto border"
                />
              ) : (
                <div className="text-center py-12 text-gray-500">
                  No screenshot available
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
