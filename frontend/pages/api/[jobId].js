export default async function handler(req, res) {
  const { jobId } = req.query;
  const { format } = req.query;
  
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }
  
  try {
    // Forward request to backend
    const backendResponse = await fetch(`${process.env.BACKEND_URL}/api/export/${jobId}?format=${format}`, {
      headers: {
        'Authorization': `Bearer ${process.env.API_KEY}`
      }
    });
    
    if (!backendResponse.ok) {
      const error = await backendResponse.text();
      throw new Error(`Backend error: ${error}`);
    }
    
    // Get the blob and set appropriate headers
    const blob = await backendResponse.blob();
    const contentType = backendResponse.headers.get('content-type');
    
    res.setHeader('Content-Type', contentType || 'application/octet-stream');
    res.setHeader('Content-Disposition', `attachment; filename=export-${jobId}.${format}`);
    
    // Send the blob as response
    const buffer = await blob.arrayBuffer();
    res.send(Buffer.from(buffer));
  } catch (error) {
    console.error('Export API error:', error);
    res.status(500).json({ error: error.message });
  }
}
