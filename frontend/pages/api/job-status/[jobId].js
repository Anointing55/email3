export default async function handler(req, res) {
  const { jobId } = req.query;
  
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }
  
  try {
    // Forward request to backend
    const backendResponse = await fetch(`${process.env.BACKEND_URL}/api/job-status/${jobId}`, {
      headers: {
        'Authorization': `Bearer ${process.env.API_KEY}`
      }
    });
    
    if (!backendResponse.ok) {
      const error = await backendResponse.text();
      throw new Error(`Backend error: ${error}`);
    }
    
    const data = await backendResponse.json();
    res.status(200).json(data);
  } catch (error) {
    console.error('API error:', error);
    res.status(500).json({ error: error.message });
  }
}
