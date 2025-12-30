import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API functions
export const approvalAPI = {
  // Get pending approvals
  getPending: () => 
    api.get('/api/v1/approvals/pending'),
  
  // Submit approval decision
  submit: (data: { brief_id: string; approved: boolean; feedback?: string }) =>
    api.post('/api/v1/approvals/submit', data),
  
  // Scan trends
  scanTrends: (categories: string[], minScore: number) =>
    api.post('/api/v1/trends/scan', {
      product_categories: categories,
      min_relevance_score: minScore,
      max_briefs: 10
    }),
  
  // Generate copy
  generateCopy: (briefId: string, platforms: string[]) =>
    api.post('/api/v1/content/generate-copy', null, {
      params: { brief_id: briefId, platforms }
    }),
};
