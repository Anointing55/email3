export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // Forward file to backend
    const formData = new FormData();
    const file = req.files.file;
    formData.append('file', file.data, file.name);
    
    const backendResponse = await fetch(`${process.env.BACKEND_URL}/api/upload`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${process.env.API_KEY}`
      },
      body: formData
    });
    
    if (!backendResponse.ok) {
      const error = await backendResponse.text();
      throw new Error(`Backend error: ${error}`);
    }
    
    const data = await backendResponse.json();
    res.status(200).json(data);
  } catch (error) {
    console.error('Upload API error:', error);
    res.status(500).json({ error: error.message });
  }
}
