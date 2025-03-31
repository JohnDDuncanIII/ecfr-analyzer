const config = {
  apiBaseUrl: process.env.NEXT_PUBLIC_DEBUG ? 'http://localhost:8000' : process.env.NEXT_PUBLIC_API_URL,
};

export default config; 