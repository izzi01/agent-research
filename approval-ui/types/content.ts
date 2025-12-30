export interface ContentBrief {
  brief_id: string;
  trend_id: string;
  vietnamese_hook: string;
  content_angle: string;
  vietnamese_voiceover: string;
  hashtags: string[];
  optimal_posting_time: string;
  success_metrics: {
    target_views: number;
    expected_engagement_rate: number;
    expected_revenue_vnd: number;
  };
  matched_products: Array<{
    product_id: string;
    name: string;
    price_vnd: number;
    relevance_score: number;
  }>;
  content_format: string;
  created_at: string;
  status: 'pending' | 'approved' | 'rejected';
}

export interface ApprovalDecision {
  brief_id: string;
  approved: boolean;
  feedback?: string;
  reviewer?: string;
  timestamp: string;
}

export interface TrendScanResult {
  workflow_id: string;
  status: string;
  trends_discovered: number;
  content_briefs_created: number;
  briefs: ContentBrief[];
}
