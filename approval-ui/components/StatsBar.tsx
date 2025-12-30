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
    totalViews: briefs.reduce((sum, b) => sum + (b.success_metrics?.target_views || 0), 0),
    totalRevenue: briefs.reduce((sum, b) => sum + (b.success_metrics?.expected_revenue_vnd || 0), 0),
    highPotential: briefs.filter(b => (b.success_metrics?.target_views || 0) > 40000).length,
  };

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatCard
          icon={<FileText className="w-6 h-6" />}
          label="Tổng số"
          value={stats.total}
          color="blue"
          subtext="nội dung"
        />
        <StatCard
          icon={<Clock className="w-6 h-6" />}
          label="Đang chờ"
          value={stats.pending}
          color="yellow"
          subtext="cần phê duyệt"
        />
        <StatCard
          icon={<CheckCircle className="w-6 h-6" />}
          label="Đã duyệt"
          value={stats.approved}
          color="green"
          subtext="đã phê duyệt"
        />
        <StatCard
          icon={<XCircle className="w-6 h-6" />}
          label="Đã từ chối"
          value={stats.rejected}
          color="red"
          subtext="đã từ chối"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <PerformanceCard
          icon="👁️"
          label="Tổng lượt xem dự kiến"
          value={stats.totalViews.toLocaleString()}
          color="bg-blue-50 text-blue-700 border-blue-200"
        />
        <PerformanceCard
          icon="💰"
          label="Tổng doanh thu dự kiến"
          value={`${(stats.totalRevenue / 1000000).toFixed(1)}M VNĐ`}
          color="bg-purple-50 text-purple-700 border-purple-200"
        />
        <PerformanceCard
          icon="🔥"
          label="Tiềm năng cao (>40K views)"
          value={`${stats.highPotential} nội dung`}
          color="bg-orange-50 text-orange-700 border-orange-200"
        />
      </div>
    </div>
  );
}

function StatCard({ icon, label, value, color, subtext }: any) {
  const colors: any = {
    blue: { bg: "bg-blue-50", text: "text-blue-600", border: "border-blue-200" },
    yellow: { bg: "bg-yellow-50", text: "text-yellow-600", border: "border-yellow-200" },
    green: { bg: "bg-green-50", text: "text-green-600", border: "border-green-200" },
    red: { bg: "bg-red-50", text: "text-red-600", border: "border-red-200" },
  };

  const colorScheme = colors[color];

  return (
    <div className={`bg-white rounded-lg shadow-md p-6 border-2 ${colorScheme.border}`}>
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <p className="text-gray-600 text-sm font-medium mb-1">{label}</p>
          <p className="text-4xl font-bold mb-1">{value}</p>
          <p className="text-xs text-gray-500">{subtext}</p>
        </div>
        <div className={`p-4 rounded-xl ${colorScheme.bg} ${colorScheme.text}`}>
          {icon}
        </div>
      </div>
    </div>
  );
}

function PerformanceCard({ icon, label, value, color }: any) {
  return (
    <div className={`${color} border-2 rounded-lg p-4`}>
      <div className="flex items-center gap-3">
        <span className="text-3xl">{icon}</span>
        <div>
          <p className="text-xs font-semibold uppercase opacity-75">{label}</p>
          <p className="text-2xl font-bold mt-1">{value}</p>
        </div>
      </div>
    </div>
  );
}
