"use client";

import { useCopilotReadable, useCopilotAction } from "@copilotkit/react-core";
import { useQuery } from "@tanstack/react-query";
import { approvalAPI } from "@/lib/api";
import { ContentBrief } from "@/types/content";
import BriefCard from "@/components/BriefCard";
import StatsBar from "@/components/StatsBar";
import { useState } from "react";

export default function DashboardPage() {
  const [selectedBriefs, setSelectedBriefs] = useState<string[]>([]);
  const [filterBy, setFilterBy] = useState<'all' | 'high' | 'medium' | 'low'>('all');
  const [sortBy, setSortBy] = useState<'views' | 'revenue' | 'recent'>('views');

  const { data: briefs, isLoading, error, refetch } = useQuery({
    queryKey: ["pending-briefs"],
    queryFn: async () => {
      const response = await approvalAPI.getPending();
      return response.data as ContentBrief[];
    },
    refetchInterval: 30000,
  });

  useCopilotReadable({
    description: "Danh sách các nội dung đang chờ phê duyệt",
    value: briefs || [],
  });

  useCopilotAction({
    name: "refresh_briefs",
    description: "Làm mới danh sách nội dung",
    parameters: [],
    handler: async () => {
      await refetch();
      return { success: true };
    },
  });

  useCopilotAction({
    name: "batch_approve",
    description: "Phê duyệt nhiều nội dung",
    parameters: [
      {
        name: "brief_ids",
        type: "string[]",
        description: "Danh sách ID",
        required: true,
      },
    ],
    handler: async ({ brief_ids }) => {
      await Promise.all(brief_ids.map(id => approvalAPI.submit({ brief_id: id, approved: true })));
      refetch();
      return { success: true };
    },
  });

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50">
        <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50">
        <div className="bg-white p-8 rounded-lg shadow-xl max-w-md text-center">
          <p className="text-red-600 text-xl font-semibold mb-4">Lỗi kết nối</p>
          <button onClick={() => refetch()} className="px-6 py-3 bg-blue-600 text-white rounded-lg">
            Thử lại
          </button>
        </div>
      </div>
    );
  }

  const filteredBriefs = briefs
    ?.filter(brief => {
      if (filterBy === 'all') return true;
      const views = brief.success_metrics?.target_views || 0;
      if (filterBy === 'high') return views > 40000;
      if (filterBy === 'medium') return views >= 20000 && views <= 40000;
      if (filterBy === 'low') return views < 20000;
      return true;
    })
    ?.sort((a, b) => {
      if (sortBy === 'views') {
        return (b.success_metrics?.target_views || 0) - (a.success_metrics?.target_views || 0);
      }
      if (sortBy === 'revenue') {
        return (b.success_metrics?.expected_revenue_vnd || 0) - (a.success_metrics?.expected_revenue_vnd || 0);
      }
      return 0;
    });

  const handleApprove = async (briefId: string) => {
    await approvalAPI.submit({ brief_id: briefId, approved: true });
    refetch();
  };

  const handleReject = async (briefId: string) => {
    await approvalAPI.submit({ brief_id: briefId, approved: false });
    refetch();
  };

  const handleBatchApprove = async (briefIds?: string[]) => {
    const ids = briefIds || selectedBriefs;
    await Promise.all(ids.map(id => approvalAPI.submit({ brief_id: id, approved: true })));
    setSelectedBriefs([]);
    refetch();
  };

  const handleScanTrends = async () => {
    await approvalAPI.scanTrends(["beauty", "fashion", "food"], 0.6);
    setTimeout(() => refetch(), 2000);
  };

  const toggleSelect = (briefId: string) => {
    setSelectedBriefs(prev =>
      prev.includes(briefId)
        ? prev.filter(id => id !== briefId)
        : [...prev, briefId]
    );
  };

  const selectAll = () => {
    if (selectedBriefs.length === filteredBriefs?.length) {
      setSelectedBriefs([]);
    } else {
      setSelectedBriefs(filteredBriefs?.map(b => b.brief_id) || []);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Bảng Phê Duyệt Nội Dung</h1>
          <p className="text-gray-600">Quản lý và phê duyệt nội dung tiếng Việt với AI</p>
        </div>

        <StatsBar briefs={briefs || []} />

        <div className="mt-8 bg-white rounded-lg shadow-md p-4 flex gap-4 flex-wrap">
          <select
            value={filterBy}
            onChange={(e) => setFilterBy(e.target.value as any)}
            className="px-4 py-2 border rounded-lg"
          >
            <option value="all">Tất cả</option>
            <option value="high">Tiềm năng cao (&gt;40K)</option>
            <option value="medium">Tiềm năng trung bình (20-40K)</option>
            <option value="low">Tiềm năng thấp (&lt;20K)</option>
          </select>

          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as any)}
            className="px-4 py-2 border rounded-lg"
          >
            <option value="views">Theo lượt xem</option>
            <option value="revenue">Theo doanh thu</option>
            <option value="recent">Mới nhất</option>
          </select>

          <button onClick={selectAll} className="px-4 py-2 bg-gray-100 rounded-lg">
            {selectedBriefs.length === filteredBriefs?.length ? 'Bỏ chọn tất cả' : 'Chọn tất cả'}
          </button>

          <button onClick={() => refetch()} className="px-4 py-2 bg-blue-600 text-white rounded-lg">
            Làm mới
          </button>
        </div>

        {selectedBriefs.length > 0 && (
          <div className="mt-4 bg-blue-50 border-2 border-blue-200 rounded-lg p-4 flex items-center justify-between">
            <span>Đã chọn {selectedBriefs.length} nội dung</span>
            <div className="flex gap-3">
              <button onClick={() => handleBatchApprove()} className="px-6 py-2 bg-green-600 text-white rounded-lg">
                Phê duyệt hàng loạt
              </button>
              <button onClick={() => setSelectedBriefs([])} className="px-6 py-2 bg-gray-600 text-white rounded-lg">
                Hủy
              </button>
            </div>
          </div>
        )}

        {filteredBriefs && filteredBriefs.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-6">
            {filteredBriefs.map((brief) => (
              <BriefCard 
                key={brief.brief_id} 
                brief={brief}
                onApprove={() => handleApprove(brief.brief_id)}
                onReject={() => handleReject(brief.brief_id)}
                isSelected={selectedBriefs.includes(brief.brief_id)}
                onSelect={() => toggleSelect(brief.brief_id)}
              />
            ))}
          </div>
        ) : (
          <div className="text-center py-20 bg-white rounded-lg shadow-lg mt-6">
            <p className="text-gray-500 text-xl mb-4">Không có nội dung nào</p>
            <button onClick={handleScanTrends} className="px-8 py-4 bg-blue-600 text-white rounded-lg">
              Quét Xu Hướng Mới
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
