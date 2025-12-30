# 🚀 CopilotKit Approval UI - Implementation Plan

## 📅 **5-Day Implementation Schedule**

---

## **DAY 1: Setup & Foundation**

### **Morning Session (3 hours)**

#### **Task 1.1: Create Next.js Project with CopilotKit** ⏱️ 30 min

```bash
# Navigate to project root
cd /home/cid/projects-personal/agent-research

# Create approval-ui directory
npx copilotkit@latest create approval-ui

# Follow prompts:
# - Framework: Next.js
# - TypeScript: Yes
# - Tailwind: Yes
# - App Router: Yes
# - Install dependencies: Yes

cd approval-ui
```

**Expected result:**
```
approval-ui/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   └── api/
│       └── copilotkit/
├── components/
├── public/
├── package.json
└── next.config.js
```

---

#### **Task 1.2: Install Additional Dependencies** ⏱️ 15 min

```bash
# Install additional packages
uv pip install --system \
  @tanstack/react-query \
  zustand \
  axios \
  date-fns \
  lucide-react \
  @radix-ui/react-dropdown-menu \
  @radix-ui/react-dialog \
  @radix-ui/react-toast

# Or with npm:
npm install @tanstack/react-query zustand axios date-fns lucide-react
npm install @radix-ui/react-dropdown-menu @radix-ui/react-dialog @radix-ui/react-toast
```

---

#### **Task 1.3: Configure CopilotKit Provider** ⏱️ 30 min

**Edit `app/layout.tsx`:**

```typescript
import { CopilotKit } from "@copilotkit/react-core";
import { CopilotSidebar } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="vi"> {/* Vietnamese language */}
      <body>
        <CopilotKit 
          runtimeUrl="/api/copilotkit"
          publicApiKey={process.env.NEXT_PUBLIC_COPILOT_API_KEY}
        >
          <CopilotSidebar
            instructions={`
              Bạn là trợ lý AI giúp phê duyệt nội dung tiếp thị tiếng Việt.
              
              Nhiệm vụ:
              1. Hiển thị các bản dự thảo nội dung cần phê duyệt
              2. Phân tích chất lượng nội dung tiếng Việt
              3. Đề xuất phê duyệt hoặc từ chối
              4. Giải thích lý do quyết định
              
              Phong cách: Thân thiện, chuyên nghiệp, hỗ trợ tối đa
            `}
            labels={{
              title: "Trợ Lý Phê Duyệt",
              initial: "Xin chào! Tôi có thể giúp gì cho bạn?",
              placeholder: "Hỏi về nội dung cần phê duyệt...",
            }}
            defaultOpen={true}
          >
            {children}
          </CopilotSidebar>
        </CopilotKit>
      </body>
    </html>
  );
}
```

---

#### **Task 1.4: Connect to AgentOS Backend** ⏱️ 45 min

**Create `lib/api.ts`:**

```typescript
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
```

**Create `.env.local`:**

```bash
# CopilotKit Configuration
NEXT_PUBLIC_COPILOT_API_KEY=your-copilotkit-api-key-here

# AgentOS Backend
NEXT_PUBLIC_API_URL=http://localhost:8080

# OpenAI for CopilotKit (optional - for AI suggestions)
OPENAI_API_KEY=your-openai-key-here

# Or use GLM (if CopilotKit supports it)
ZHIPU_API_KEY=your-glm-key-here
```

---

#### **Task 1.5: Create TypeScript Types** ⏱️ 30 min

**Create `types/content.ts`:**

```typescript
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
```

---

### **Afternoon Session (3 hours)**

#### **Task 1.6: Create CopilotKit Agent Actions** ⏱️ 1 hour

**Create `app/api/copilotkit/route.ts`:**

```typescript
import {
  CopilotRuntime,
  OpenAIAdapter,
  copilotRuntimeNextJSAppRouterEndpoint,
} from "@copilotkit/runtime";
import { NextRequest } from "next/server";
import { approvalAPI } from "@/lib/api";

const runtime = new CopilotRuntime({
  actions: [
    {
      name: "get_pending_briefs",
      description: "Lấy danh sách các bản dự thảo nội dung đang chờ phê duyệt",
      parameters: [],
      handler: async () => {
        const response = await approvalAPI.getPending();
        return {
          briefs: response.data,
          count: response.data.length,
        };
      },
    },
    {
      name: "approve_brief",
      description: "Phê duyệt một bản dự thảo nội dung",
      parameters: [
        {
          name: "brief_id",
          type: "string",
          description: "ID của bản dự thảo cần phê duyệt",
          required: true,
        },
        {
          name: "feedback",
          type: "string",
          description: "Nhận xét về nội dung (tùy chọn)",
          required: false,
        },
      ],
      handler: async ({ brief_id, feedback }) => {
        await approvalAPI.submit({
          brief_id,
          approved: true,
          feedback,
        });
        return {
          success: true,
          message: `Đã phê duyệt nội dung ${brief_id}`,
        };
      },
    },
    {
      name: "reject_brief",
      description: "Từ chối một bản dự thảo nội dung",
      parameters: [
        {
          name: "brief_id",
          type: "string",
          description: "ID của bản dự thảo cần từ chối",
          required: true,
        },
        {
          name: "feedback",
          type: "string",
          description: "Lý do từ chối",
          required: true,
        },
      ],
      handler: async ({ brief_id, feedback }) => {
        await approvalAPI.submit({
          brief_id,
          approved: false,
          feedback,
        });
        return {
          success: true,
          message: `Đã từ chối nội dung ${brief_id}`,
        };
      },
    },
    {
      name: "analyze_brief_quality",
      description: "Phân tích chất lượng bản dự thảo nội dung tiếng Việt",
      parameters: [
        {
          name: "brief_id",
          type: "string",
          description: "ID của bản dự thảo cần phân tích",
          required: true,
        },
      ],
      handler: async ({ brief_id }) => {
        // Get brief data
        const response = await approvalAPI.getPending();
        const brief = response.data.find((b: any) => b.brief_id === brief_id);
        
        if (!brief) {
          return { error: "Không tìm thấy bản dự thảo" };
        }
        
        // Analyze Vietnamese quality
        const analysis = {
          hook_quality: brief.vietnamese_hook.length > 50 ? "Tốt" : "Cần cải thiện",
          hashtag_count: brief.hashtags.length,
          expected_views: brief.success_metrics.target_views,
          expected_revenue: brief.success_metrics.expected_revenue_vnd,
          recommendation: brief.success_metrics.target_views > 30000 
            ? "Đề xuất PHÊ DUYỆT - Tiềm năng cao"
            : "Đề xuất XEM XÉT - Tiềm năng trung bình",
        };
        
        return analysis;
      },
    },
    {
      name: "scan_new_trends",
      description: "Quét xu hướng TikTok mới và tạo nội dung",
      parameters: [
        {
          name: "categories",
          type: "array",
          description: "Danh mục sản phẩm (beauty, fashion, food)",
          required: true,
        },
      ],
      handler: async ({ categories }) => {
        const response = await approvalAPI.scanTrends(categories, 0.6);
        return {
          trends_found: response.data.trends_discovered,
          briefs_created: response.data.content_briefs_created,
          message: `Đã tìm thấy ${response.data.trends_discovered} xu hướng và tạo ${response.data.content_briefs_created} nội dung mới`,
        };
      },
    },
  ],
});

export const POST = async (req: NextRequest) => {
  const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
    runtime,
    serviceAdapter: new OpenAIAdapter(),
    endpoint: "/api/copilotkit",
  });

  return handleRequest(req);
};
```

---

#### **Task 1.7: Test CopilotKit Setup** ⏱️ 30 min

```bash
# Start AgentOS backend (if not running)
cd /home/cid/projects-personal/agent-research/agentos
source .venv/bin/activate
python main.py

# In new terminal, start Next.js
cd /home/cid/projects-personal/agent-research/approval-ui
npm run dev

# Open browser
open http://localhost:3000
```

**Expected result:**
- ✅ CopilotKit sidebar appears
- ✅ Can chat with AI in Vietnamese
- ✅ AI can answer questions
- ✅ No errors in console

---

#### **Task 1.8: Test Agent Actions** ⏱️ 30 min

**In CopilotKit chat, test:**

```
User: "Hiển thị các nội dung đang chờ phê duyệt"
AI: [Calls get_pending_briefs action]
    "Hiện có 3 nội dung đang chờ phê duyệt: #BeautyHacks, #FashionTrend, #FoodReview"

User: "Phân tích chất lượng nội dung #BeautyHacks"
AI: [Calls analyze_brief_quality action]
    "Hook quality: Tốt, Expected views: 50,000, Đề xuất: PHÊ DUYỆT"

User: "Phê duyệt nội dung #BeautyHacks với nhận xét: Rất tốt!"
AI: [Calls approve_brief action]
    "Đã phê duyệt nội dung #BeautyHacks"
```

**If working:** ✅ Day 1 Complete!

---

## **DAY 2: Main Dashboard UI**

### **Morning Session (3 hours)**

#### **Task 2.1: Create Dashboard Layout** ⏱️ 1 hour

**Create `app/page.tsx`:**

```typescript
"use client";

import { useCopilotReadable, useCopilotAction } from "@copilotkit/react-core";
import { useQuery } from "@tanstack/react-query";
import { approvalAPI } from "@/lib/api";
import { ContentBrief } from "@/types/content";
import BriefCard from "@/components/BriefCard";
import StatsBar from "@/components/StatsBar";

export default function DashboardPage() {
  // Fetch pending briefs
  const { data: briefs, refetch } = useQuery({
    queryKey: ["pending-briefs"],
    queryFn: async () => {
      const response = await approvalAPI.getPending();
      return response.data as ContentBrief[];
    },
    refetchInterval: 30000, // Refetch every 30 seconds
  });

  // Make briefs readable by CopilotKit AI
  useCopilotReadable({
    description: "Danh sách các nội dung đang chờ phê duyệt",
    value: briefs || [],
  });

  // Register action to refresh briefs
  useCopilotAction({
    name: "refresh_briefs",
    description: "Làm mới danh sách nội dung",
    handler: async () => {
      await refetch();
      return { success: true };
    },
  });

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Bảng Điều Khiển Phê Duyệt Nội Dung
          </h1>
          <p className="text-gray-600 mt-2">
            Quản lý và phê duyệt nội dung tiếp thị tiếng Việt
          </p>
        </div>

        {/* Stats Bar */}
        <StatsBar briefs={briefs || []} />

        {/* Brief Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-8">
          {briefs?.map((brief) => (
            <BriefCard 
              key={brief.brief_id} 
              brief={brief} 
              onApprove={() => handleApprove(brief.brief_id)}
              onReject={() => handleReject(brief.brief_id)}
            />
          ))}
        </div>

        {/* Empty State */}
        {briefs?.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg">
              Không có nội dung nào đang chờ phê duyệt
            </p>
            <button 
              className="mt-4 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
              onClick={() => scanTrends()}
            >
              Quét Xu Hướng Mới
            </button>
          </div>
        )}
      </div>
    </div>
  );

  async function handleApprove(briefId: string) {
    await approvalAPI.submit({ brief_id: briefId, approved: true });
    refetch();
  }

  async function handleReject(briefId: string) {
    await approvalAPI.submit({ brief_id: briefId, approved: false });
    refetch();
  }

  async function scanTrends() {
    await approvalAPI.scanTrends(["beauty", "fashion"], 0.6);
    refetch();
  }
}
```

---

#### **Task 2.2: Create BriefCard Component** ⏱️ 1 hour

**Create `components/BriefCard.tsx`:**

```typescript
"use client";

import { ContentBrief } from "@/types/content";
import { ThumbsUp, ThumbsDown, Eye, TrendingUp, DollarSign } from "lucide-react";
import { useState } from "react";

interface BriefCardProps {
  brief: ContentBrief;
  onApprove: () => void;
  onReject: () => void;
}

export default function BriefCard({ brief, onApprove, onReject }: BriefCardProps) {
  const [showDetails, setShowDetails] = useState(false);

  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
      {/* Header */}
      <div className="flex justify-between items-start mb-4">
        <h3 className="text-lg font-bold text-gray-900">
          {brief.trend_id}
        </h3>
        <span className="px-3 py-1 bg-yellow-100 text-yellow-800 text-sm rounded-full">
          Đang chờ
        </span>
      </div>

      {/* Vietnamese Hook */}
      <p className="text-gray-700 mb-4 line-clamp-2">
        {brief.vietnamese_hook}
      </p>

      {/* Metrics */}
      <div className="grid grid-cols-2 gap-3 mb-4">
        <div className="flex items-center gap-2 text-sm">
          <Eye className="w-4 h-4 text-blue-600" />
          <span>{brief.success_metrics.target_views.toLocaleString()} views</span>
        </div>
        <div className="flex items-center gap-2 text-sm">
          <TrendingUp className="w-4 h-4 text-green-600" />
          <span>{brief.success_metrics.expected_engagement_rate}%</span>
        </div>
        <div className="flex items-center gap-2 text-sm col-span-2">
          <DollarSign className="w-4 h-4 text-purple-600" />
          <span>{(brief.success_metrics.expected_revenue_vnd / 1000000).toFixed(1)}M VNĐ</span>
        </div>
      </div>

      {/* Hashtags */}
      <div className="flex flex-wrap gap-2 mb-4">
        {brief.hashtags.slice(0, 3).map((tag) => (
          <span key={tag} className="text-xs bg-gray-100 px-2 py-1 rounded">
            {tag}
          </span>
        ))}
      </div>

      {/* Actions */}
      <div className="flex gap-2">
        <button
          onClick={onApprove}
          className="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
        >
          <ThumbsUp className="w-4 h-4" />
          Phê duyệt
        </button>
        <button
          onClick={onReject}
          className="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
        >
          <ThumbsDown className="w-4 h-4" />
          Từ chối
        </button>
      </div>

      {/* Toggle Details */}
      <button
        onClick={() => setShowDetails(!showDetails)}
        className="w-full mt-3 text-sm text-blue-600 hover:text-blue-800"
      >
        {showDetails ? "Ẩn chi tiết" : "Xem chi tiết"}
      </button>

      {/* Expanded Details */}
      {showDetails && (
        <div className="mt-4 pt-4 border-t space-y-3">
          <div>
            <h4 className="font-semibold text-sm mb-1">Góc độ nội dung:</h4>
            <p className="text-sm text-gray-600">{brief.content_angle}</p>
          </div>
          <div>
            <h4 className="font-semibold text-sm mb-1">Kịch bản lồng tiếng:</h4>
            <p className="text-sm text-gray-600 line-clamp-4">
              {brief.vietnamese_voiceover}
            </p>
          </div>
          <div>
            <h4 className="font-semibold text-sm mb-1">Sản phẩm liên quan:</h4>
            {brief.matched_products.map((product) => (
              <div key={product.product_id} className="text-sm text-gray-600">
                • {product.name} - {product.price_vnd.toLocaleString()} VNĐ
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
```

---

#### **Task 2.3: Create StatsBar Component** ⏱️ 30 min

**Create `components/StatsBar.tsx`:**

```typescript
import { ContentBrief } from "@/types/content";
import { FileText, CheckCircle, XCircle, Clock } from "lucide-react";

interface StatsBarProps {
  briefs: ContentBrief[];
}

export default function StatsBar({ briefs }: StatsBarProps) {
  const stats = {
    total: briefs.length,
    pending: briefs.filter(b => b.status === 'pending').length,
    approved: briefs.filter(b => b.status === 'approved').length,
    rejected: briefs.filter(b => b.status === 'rejected').length,
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
      <StatCard
        icon={<FileText className="w-6 h-6" />}
        label="Tổng số"
        value={stats.total}
        color="blue"
      />
      <StatCard
        icon={<Clock className="w-6 h-6" />}
        label="Đang chờ"
        value={stats.pending}
        color="yellow"
      />
      <StatCard
        icon={<CheckCircle className="w-6 h-6" />}
        label="Đã duyệt"
        value={stats.approved}
        color="green"
      />
      <StatCard
        icon={<XCircle className="w-6 h-6" />}
        label="Đã từ chối"
        value={stats.rejected}
        color="red"
      />
    </div>
  );
}

function StatCard({ icon, label, value, color }: any) {
  const colors = {
    blue: "bg-blue-100 text-blue-600",
    yellow: "bg-yellow-100 text-yellow-600",
    green: "bg-green-100 text-green-600",
    red: "bg-red-100 text-red-600",
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-gray-600 text-sm">{label}</p>
          <p className="text-3xl font-bold mt-2">{value}</p>
        </div>
        <div className={`p-3 rounded-lg ${colors[color]}`}>
          {icon}
        </div>
      </div>
    </div>
  );
}
```

---

### **Afternoon Session (3 hours)**

#### **Task 2.4: Add React Query Provider** ⏱️ 30 min

**Update `app/layout.tsx`:**

```typescript
"use client";

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useState } from "react";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient());

  return (
    <html lang="vi">
      <body>
        <QueryClientProvider client={queryClient}>
          <CopilotKit runtimeUrl="/api/copilotkit">
            <CopilotSidebar>
              {children}
            </CopilotSidebar>
          </CopilotKit>
        </QueryClientProvider>
      </body>
    </html>
  );
}
```

---

#### **Task 2.5: Test Full Dashboard** ⏱️ 1 hour

```bash
# Ensure AgentOS is running
cd agentos && python main.py

# Start Next.js
cd approval-ui && npm run dev

# Test in browser:
1. View pending briefs
2. Click approve/reject
3. Check CopilotKit sidebar
4. Ask AI: "Phân tích nội dung #BeautyHacks"
5. Ask AI: "Phê duyệt tất cả nội dung beauty"
```

**Expected:**
- ✅ Dashboard shows briefs
- ✅ Can approve/reject with buttons
- ✅ Can approve/reject via AI chat
- ✅ Stats update in real-time

---

#### **Task 2.6: Add Loading & Error States** ⏱️ 30 min

**Update `app/page.tsx`:**

```typescript
const { data: briefs, isLoading, error, refetch } = useQuery({
  queryKey: ["pending-briefs"],
  queryFn: async () => {
    const response = await approvalAPI.getPending();
    return response.data;
  },
});

if (isLoading) {
  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
    </div>
  );
}

if (error) {
  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="text-center">
        <p className="text-red-600 text-lg">Lỗi tải dữ liệu</p>
        <button 
          onClick={() => refetch()}
          className="mt-4 px-6 py-2 bg-blue-600 text-white rounded-lg"
        >
          Thử lại
        </button>
      </div>
    </div>
  );
}
```

**If working:** ✅ Day 2 Complete!

---

## **DAY 3: Advanced Features**

### **Morning Session (3 hours)**

#### **Task 3.1: Batch Approval** ⏱️ 1 hour

**Add to `app/page.tsx`:**

```typescript
const [selectedBriefs, setSelectedBriefs] = useState<string[]>([]);

const handleBatchApprove = async () => {
  await Promise.all(
    selectedBriefs.map(id => 
      approvalAPI.submit({ brief_id: id, approved: true })
    )
  );
  setSelectedBriefs([]);
  refetch();
};

// Add checkbox to BriefCard
<input
  type="checkbox"
  checked={selectedBriefs.includes(brief.brief_id)}
  onChange={(e) => {
    if (e.target.checked) {
      setSelectedBriefs([...selectedBriefs, brief.brief_id]);
    } else {
      setSelectedBriefs(selectedBriefs.filter(id => id !== brief.brief_id));
    }
  }}
/>

// Add batch action button
{selectedBriefs.length > 0 && (
  <button onClick={handleBatchApprove}>
    Phê duyệt {selectedBriefs.length} nội dung
  </button>
)}
```

---

#### **Task 3.2: Detailed View Modal** ⏱️ 1 hour

**Create `components/BriefDetailModal.tsx`:**

```typescript
import * as Dialog from "@radix-ui/react-dialog";
import { ContentBrief } from "@/types/content";

export default function BriefDetailModal({ 
  brief, 
  open, 
  onClose 
}: { 
  brief: ContentBrief; 
  open: boolean; 
  onClose: () => void;
}) {
  return (
    <Dialog.Root open={open} onOpenChange={onClose}>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 bg-black/50" />
        <Dialog.Content className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-lg p-8 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
          <Dialog.Title className="text-2xl font-bold mb-4">
            {brief.trend_id}
          </Dialog.Title>

          {/* Full content details */}
          <div className="space-y-6">
            <Section title="Hook tiếng Việt">
              {brief.vietnamese_hook}
            </Section>

            <Section title="Góc độ nội dung">
              {brief.content_angle}
            </Section>

            <Section title="Kịch bản lồng tiếng">
              {brief.vietnamese_voiceover}
            </Section>

            <Section title="Hashtags">
              <div className="flex flex-wrap gap-2">
                {brief.hashtags.map(tag => (
                  <span key={tag} className="bg-blue-100 px-3 py-1 rounded">
                    {tag}
                  </span>
                ))}
              </div>
            </Section>

            <Section title="Sản phẩm liên quan">
              {brief.matched_products.map(product => (
                <div key={product.product_id} className="flex justify-between py-2 border-b">
                  <span>{product.name}</span>
                  <span className="font-semibold">
                    {product.price_vnd.toLocaleString()} VNĐ
                  </span>
                </div>
              ))}
            </Section>

            <Section title="Dự báo hiệu quả">
              <div className="grid grid-cols-2 gap-4">
                <Metric 
                  label="Lượt xem mục tiêu" 
                  value={brief.success_metrics.target_views.toLocaleString()} 
                />
                <Metric 
                  label="Tỷ lệ tương tác" 
                  value={`${brief.success_metrics.expected_engagement_rate}%`} 
                />
                <Metric 
                  label="Doanh thu dự kiến" 
                  value={`${(brief.success_metrics.expected_revenue_vnd / 1000000).toFixed(1)}M VNĐ`} 
                />
              </div>
            </Section>
          </div>

          {/* Actions */}
          <div className="flex gap-4 mt-8">
            <button className="flex-1 bg-green-600 text-white py-3 rounded-lg">
              Phê duyệt
            </button>
            <button className="flex-1 bg-red-600 text-white py-3 rounded-lg">
              Từ chối
            </button>
          </div>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div>
      <h3 className="font-semibold text-lg mb-2">{title}</h3>
      <div className="text-gray-700">{children}</div>
    </div>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="bg-gray-50 p-4 rounded">
      <p className="text-sm text-gray-600">{label}</p>
      <p className="text-2xl font-bold mt-1">{value}</p>
    </div>
  );
}
```

---

#### **Task 3.3: Filtering & Sorting** ⏱️ 30 min

**Add filters to dashboard:**

```typescript
const [filter, setFilter] = useState<'all' | 'high' | 'medium'>('all');
const [sortBy, setSortBy] = useState<'views' | 'revenue'>('views');

const filteredBriefs = briefs
  ?.filter(brief => {
    if (filter === 'all') return true;
    if (filter === 'high') return brief.success_metrics.target_views > 40000;
    if (filter === 'medium') return brief.success_metrics.target_views > 20000;
  })
  ?.sort((a, b) => {
    if (sortBy === 'views') {
      return b.success_metrics.target_views - a.success_metrics.target_views;
    }
    return b.success_metrics.expected_revenue_vnd - a.success_metrics.expected_revenue_vnd;
  });

// Add filter UI
<div className="flex gap-4 mb-6">
  <select value={filter} onChange={(e) => setFilter(e.target.value as any)}>
    <option value="all">Tất cả</option>
    <option value="high">Tiềm năng cao (>40K views)</option>
    <option value="medium">Tiềm năng trung bình (>20K views)</option>
  </select>

  <select value={sortBy} onChange={(e) => setSortBy(e.target.value as any)}>
    <option value="views">Sắp xếp theo lượt xem</option>
    <option value="revenue">Sắp xếp theo doanh thu</option>
  </select>
</div>
```

---

### **Afternoon Session (3 hours)**

#### **Task 3.4: AI Suggestions in Sidebar** ⏱️ 1 hour

**Update CopilotKit instructions:**

```typescript
<CopilotSidebar
  instructions={`
    Bạn là chuyên gia phê duyệt nội dung tiếp thị.
    
    Khi người dùng hỏi về nội dung, hãy:
    
    1. PHÂN TÍCH:
       - Chất lượng hook tiếng Việt (dài, hấp dẫn, tự nhiên?)
       - Số lượng hashtag (tối ưu: 4-8)
       - Dự báo lượt xem (cao nếu >40K, trung bình 20-40K, thấp <20K)
       - Tiềm năng doanh thu
    
    2. ĐỀ XUẤT:
       - Nếu lượt xem dự kiến >40K → "Đề xuất PHÊ DUYỆT"
       - Nếu hook ngắn (<50 ký tự) → "Cần cải thiện hook"
       - Nếu hashtag <3 → "Cần thêm hashtag"
    
    3. SO SÁNH:
       - Khi có nhiều nội dung, so sánh tiềm năng
       - Gợi ý phê duyệt top 3 nội dung tốt nhất
    
    4. BATCH ACTIONS:
       - Hỗ trợ phê duyệt hàng loạt: "Phê duyệt tất cả nội dung beauty"
       - Hỗ trợ lọc: "Hiển thị nội dung tiềm năng cao"
    
    Phong cách: Chuyên nghiệp, cung cấp số liệu cụ thể, đề xuất rõ ràng
  `}
  labels={{
    title: "Trợ Lý AI",
    initial: "Tôi có thể giúp bạn:\n\n✓ Phân tích chất lượng nội dung\n✓ Đề xuất phê duyệt/từ chối\n✓ So sánh nhiều nội dung\n✓ Phê duyệt hàng loạt\n\nHãy hỏi tôi!",
    placeholder: "Ví dụ: Phân tích nội dung #BeautyHacks",
  }}
/>
```

---

#### **Task 3.5: Add Toast Notifications** ⏱️ 30 min

**Create `components/Toast.tsx`:**

```typescript
import * as ToastPrimitive from "@radix-ui/react-toast";
import { CheckCircle, XCircle } from "lucide-react";

export function Toast({ 
  title, 
  description, 
  type = "success" 
}: { 
  title: string; 
  description?: string; 
  type?: "success" | "error";
}) {
  const colors = {
    success: "bg-green-50 border-green-200",
    error: "bg-red-50 border-red-200",
  };

  const icons = {
    success: <CheckCircle className="text-green-600" />,
    error: <XCircle className="text-red-600" />,
  };

  return (
    <ToastPrimitive.Root className={`${colors[type]} border rounded-lg p-4 shadow-lg`}>
      <div className="flex items-start gap-3">
        {icons[type]}
        <div>
          <ToastPrimitive.Title className="font-semibold">
            {title}
          </ToastPrimitive.Title>
          {description && (
            <ToastPrimitive.Description className="text-sm text-gray-600">
              {description}
            </ToastPrimitive.Description>
          )}
        </div>
      </div>
    </ToastPrimitive.Root>
  );
}

// Use in dashboard:
import { useToast } from "@/hooks/useToast";

const { toast } = useToast();

const handleApprove = async (briefId: string) => {
  await approvalAPI.submit({ brief_id: briefId, approved: true });
  toast({
    title: "Đã phê duyệt!",
    description: `Nội dung ${briefId} đã được phê duyệt`,
    type: "success",
  });
  refetch();
};
```

---

#### **Task 3.6: Test All Features** ⏱️ 1 hour

**Test checklist:**
```
✅ 1. Dashboard loads pending briefs
✅ 2. Can approve single brief via button
✅ 3. Can reject single brief via button
✅ 4. Can select multiple briefs
✅ 5. Can batch approve via button
✅ 6. Can approve via AI chat: "Phê duyệt #BeautyHacks"
✅ 7. Can analyze via AI: "Phân tích #BeautyHacks"
✅ 8. Can batch approve via AI: "Phê duyệt tất cả beauty"
✅ 9. Filtering works (high/medium/all)
✅ 10. Sorting works (views/revenue)
✅ 11. Detail modal opens and shows full info
✅ 12. Toast notifications appear
✅ 13. Stats update in real-time
✅ 14. Vietnamese text renders correctly
```

**If all pass:** ✅ Day 3 Complete!

---

## **DAY 4: Polish & Optimization**

### **Morning Session (3 hours)**

#### **Task 4.1: Add Keyboard Shortcuts** ⏱️ 30 min

```typescript
import { useHotkeys } from "react-hotkeys-hook";

// In dashboard:
useHotkeys('ctrl+a', () => handleBatchApprove()); // Approve all
useHotkeys('ctrl+r', () => refetch()); // Refresh
useHotkeys('/', () => {
  // Focus CopilotKit search
  document.querySelector('[data-copilotkit-search]')?.focus();
});
```

---

#### **Task 4.2: Responsive Design** ⏱️ 1 hour

**Update Tailwind classes:**

```typescript
// Mobile-first responsive design
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
  {/* Brief cards */}
</div>

// Sidebar on mobile
<CopilotSidebar
  defaultOpen={false} // Closed by default on mobile
  className="md:w-96"
/>
```

---

#### **Task 4.3: Performance Optimization** ⏱️ 1 hour

```typescript
// Memoize components
import { memo } from "react";

const BriefCard = memo(({ brief, onApprove, onReject }) => {
  // Component code
});

// Virtual scrolling for large lists
import { useVirtualizer } from "@tanstack/react-virtual";

const virtualizer = useVirtualizer({
  count: briefs.length,
  getScrollElement: () => scrollRef.current,
  estimateSize: () => 350,
});

// Lazy load images
<img loading="lazy" src={product.image} />
```

---

### **Afternoon Session (3 hours)**

#### **Task 4.4: Add Analytics** ⏱️ 1 hour

**Create `lib/analytics.ts`:**

```typescript
export const analytics = {
  trackApproval: (briefId: string, decision: "approved" | "rejected") => {
    // Send to analytics service
    console.log(`Tracked: ${decision} for ${briefId}`);
  },
  
  trackAIUsage: (action: string, success: boolean) => {
    console.log(`AI Action: ${action}, Success: ${success}`);
  },
};

// Use in components:
analytics.trackApproval(brief.brief_id, "approved");
```

---

#### **Task 4.5: Error Handling & Retry Logic** ⏱️ 1 hour

```typescript
const { data, error, refetch } = useQuery({
  queryKey: ["pending-briefs"],
  queryFn: async () => {
    const response = await approvalAPI.getPending();
    return response.data;
  },
  retry: 3, // Retry 3 times on failure
  retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
  staleTime: 30000, // Cache for 30 seconds
});

// Handle approval errors
const handleApprove = async (briefId: string) => {
  try {
    await approvalAPI.submit({ brief_id: briefId, approved: true });
    toast({ title: "Thành công!", type: "success" });
  } catch (error) {
    toast({ 
      title: "Lỗi!", 
      description: "Không thể phê duyệt. Vui lòng thử lại.",
      type: "error" 
    });
  }
};
```

---

#### **Task 4.6: Final Testing** ⏱️ 1 hour

**Test scenarios:**
```
1. Offline handling:
   - Disconnect network → Should show error → Retry works

2. Large datasets:
   - Load 100+ briefs → Performance OK → Virtual scrolling works

3. Concurrent approvals:
   - Approve multiple at once → All succeed → No race conditions

4. AI edge cases:
   - Ask nonsensical questions → AI handles gracefully
   - Request impossible actions → AI explains why not

5. Mobile testing:
   - Responsive on phone → Sidebar toggles → Touch works
```

**If all pass:** ✅ Day 4 Complete!

---

## **DAY 5: Deployment & Documentation**

### **Morning Session (3 hours)**

#### **Task 5.1: Production Build** ⏱️ 30 min

```bash
# Build for production
npm run build

# Test production build locally
npm run start

# Check bundle size
npm run analyze
```

---

#### **Task 5.2: Docker Configuration** ⏱️ 1 hour

**Create `Dockerfile`:**

```dockerfile
FROM node:20-alpine AS base

# Install dependencies
FROM base AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci

# Build application
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Production image
FROM base AS runner
WORKDIR /app

ENV NODE_ENV=production

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT=3000

CMD ["node", "server.js"]
```

**Build and test:**

```bash
docker build -t approval-ui:latest .
docker run -p 3000:3000 approval-ui:latest
```

---

#### **Task 5.3: Environment Configuration** ⏱️ 30 min

**Create `.env.production`:**

```bash
NEXT_PUBLIC_API_URL=https://marketing.your-domain.com/api
NEXT_PUBLIC_COPILOT_API_KEY=prod-copilotkit-key
OPENAI_API_KEY=prod-openai-key
```

**Create `docker-compose.yml`:**

```yaml
version: '3.8'

services:
  approval-ui:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://agentos:8080
      - NEXT_PUBLIC_COPILOT_API_KEY=${COPILOT_API_KEY}
    depends_on:
      - agentos

  agentos:
    image: your-registry/agentos:latest
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=postgresql://agno:changeme123@postgres:5432/marketing_automation
```

---

#### **Task 5.4: Kubernetes Deployment** ⏱️ 1 hour

**Update `k8s/base/06-approval-ui.yaml`:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: approval-ui
  namespace: marketing-automation
spec:
  replicas: 2
  selector:
    matchLabels:
      app: approval-ui
  template:
    metadata:
      labels:
        app: approval-ui
    spec:
      containers:
      - name: approval-ui
        image: your-registry/approval-ui:latest
        ports:
        - containerPort: 3000
        env:
        - name: NEXT_PUBLIC_API_URL
          value: "http://agentos-service:8080"
        - name: NEXT_PUBLIC_COPILOT_API_KEY
          valueFrom:
            secretKeyRef:
              name: copilotkit-secret
              key: api-key
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: approval-ui-service
  namespace: marketing-automation
spec:
  selector:
    app: approval-ui
  ports:
  - port: 80
    targetPort: 3000
```

---

### **Afternoon Session (3 hours)**

#### **Task 5.5: Documentation** ⏱️ 2 hours

**Create `approval-ui/README.md`:**

```markdown
# Vietnamese Content Approval UI

AI-powered dashboard for approving Vietnamese marketing content, built with CopilotKit and Next.js.

## Features

- ✅ Visual content brief cards
- ✅ AI chat assistant for approvals
- ✅ Batch approval/rejection
- ✅ Real-time stats dashboard
- ✅ Vietnamese language optimized
- ✅ Mobile responsive

## Quick Start

\`\`\`bash
# Install
npm install

# Run dev server
npm run dev

# Build for production
npm run build
\`\`\`

## Environment Variables

\`\`\`bash
NEXT_PUBLIC_API_URL=http://localhost:8080
NEXT_PUBLIC_COPILOT_API_KEY=your-copilotkit-key
OPENAI_API_KEY=your-openai-key
\`\`\`

## Usage

### Via UI Buttons
1. View pending briefs
2. Click "Phê duyệt" or "Từ chối"

### Via AI Chat
\`\`\`
User: "Phân tích nội dung #BeautyHacks"
AI: [Provides analysis and recommendation]

User: "Phê duyệt nội dung #BeautyHacks"
AI: [Approves the brief]
\`\`\`

## Tech Stack

- Next.js 14
- CopilotKit AG-UI
- React Query
- Tailwind CSS
- Radix UI
- TypeScript
```

---

#### **Task 5.6: Final Deployment** ⏱️ 1 hour

```bash
# Build and push Docker image
docker build -t your-registry/approval-ui:latest .
docker push your-registry/approval-ui:latest

# Deploy to Kubernetes
kubectl apply -f k8s/base/06-approval-ui.yaml

# Verify deployment
kubectl get pods -n marketing-automation -l app=approval-ui
kubectl logs -n marketing-automation -l app=approval-ui -f

# Access UI
# Option 1: Port forward
kubectl port-forward -n marketing-automation svc/approval-ui-service 3000:80

# Option 2: Via ingress (if configured)
# https://marketing.your-domain.com
```

**If successful:** ✅ Day 5 Complete! 🎉

---

## **COMPLETION CHECKLIST**

### **Day 1:** ✅ Setup & Foundation
- [ ] CopilotKit project created
- [ ] Dependencies installed
- [ ] Backend API connected
- [ ] Agent actions configured
- [ ] Basic chat working

### **Day 2:** ✅ Main Dashboard
- [ ] Dashboard layout created
- [ ] Brief cards displaying
- [ ] Stats bar showing metrics
- [ ] Approve/reject buttons working
- [ ] Loading/error states handled

### **Day 3:** ✅ Advanced Features
- [ ] Batch approval implemented
- [ ] Detail modal created
- [ ] Filtering/sorting added
- [ ] AI suggestions enhanced
- [ ] Toast notifications working

### **Day 4:** ✅ Polish & Optimization
- [ ] Keyboard shortcuts added
- [ ] Responsive design implemented
- [ ] Performance optimized
- [ ] Analytics integrated
- [ ] Error handling robust

### **Day 5:** ✅ Deployment
- [ ] Production build successful
- [ ] Docker image created
- [ ] K8s manifests updated
- [ ] Documentation complete
- [ ] Deployed to production

---

## **SUCCESS METRICS**

After 5 days, you should have:

✅ **Functional Approval UI**
- Displays Vietnamese content briefs
- Approve/reject with buttons or AI chat
- Batch operations support
- Real-time stats

✅ **AI Assistant**
- Analyzes content quality
- Provides recommendations
- Executes approvals via conversation
- Answers questions in Vietnamese

✅ **Production Ready**
- Dockerized
- Kubernetes manifests
- Error handling
- Performance optimized

✅ **Documentation**
- Setup guide
- Usage examples
- Deployment instructions

---

## **ESTIMATED EFFORT**

| Phase | Hours | Days (8h/day) |
|-------|-------|---------------|
| Setup | 6h | 0.75 |
| Dashboard | 10h | 1.25 |
| Features | 12h | 1.5 |
| Polish | 8h | 1.0 |
| Deploy | 6h | 0.75 |
| **Total** | **42h** | **5.25 days** |

---

## **NEXT STEPS AFTER COMPLETION**

1. **Gather User Feedback** - Test with marketing team
2. **Add Video Preview** - Show generated videos
3. **Add Analytics Dashboard** - Track approval rates
4. **Integrate More Platforms** - YouTube, Instagram
5. **Add A/B Testing** - Test different copy variants

---

**Ready to start?** Begin with Day 1, Task 1.1! 🚀
