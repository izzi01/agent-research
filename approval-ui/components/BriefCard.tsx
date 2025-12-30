"use client";

import { ContentBrief } from "@/types/content";
import { useState } from "react";
import { Eye, TrendingUp, DollarSign, ThumbsUp, ThumbsDown, ChevronDown, ChevronUp } from "lucide-react";

interface BriefCardProps {
  brief: ContentBrief;
  onApprove: () => void;
  onReject: () => void;
  isSelected?: boolean;
  onSelect?: () => void;
}

export default function BriefCard({ brief, onApprove, onReject, isSelected, onSelect }: BriefCardProps) {
  const [showDetails, setShowDetails] = useState(false);

  return (
    <div className={`bg-white rounded-lg shadow-md p-6 hover:shadow-xl border-2 ${
      isSelected ? 'border-blue-500' : 'border-gray-100'
    }`}>
      {onSelect && (
        <div className="flex items-start mb-3">
          <input
            type="checkbox"
            checked={isSelected}
            onChange={onSelect}
            className="mt-1 h-5 w-5 rounded border-gray-300 text-blue-600"
          />
          <label className="ml-2 text-sm text-gray-600 cursor-pointer" onClick={onSelect}>
            Chọn để phê duyệt hàng loạt
          </label>
        </div>
      )}

      <div className="flex justify-between items-start mb-4">
        <h3 className="text-xl font-bold text-gray-900">{brief.trend_id}</h3>
        <span className="px-3 py-1 bg-yellow-100 text-yellow-800 text-sm rounded-full">
          Đang chờ
        </span>
      </div>

      <div className="mb-4">
        <p className="text-gray-700 leading-relaxed line-clamp-3">
          "{brief.vietnamese_hook}"
        </p>
      </div>

      <div className="mb-4">
        <span className="text-xs font-semibold text-gray-500 uppercase">Góc độ:</span>
        <p className="text-sm text-gray-600 mt-1">{brief.content_angle}</p>
      </div>

      <div className="grid grid-cols-2 gap-3 mb-4 p-3 bg-gray-50 rounded-lg">
        <div className="flex items-center gap-2 text-sm">
          <Eye className="w-4 h-4 text-blue-600" />
          <div>
            <p className="text-xs text-gray-500">Lượt xem</p>
            <p className="font-bold text-blue-600">
              {brief.success_metrics?.target_views?.toLocaleString() || 0}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2 text-sm">
          <TrendingUp className="w-4 h-4 text-green-600" />
          <div>
            <p className="text-xs text-gray-500">Tương tác</p>
            <p className="font-bold text-green-600">
              {brief.success_metrics?.expected_engagement_rate || 0}%
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2 col-span-2 text-sm">
          <DollarSign className="w-4 h-4 text-purple-600" />
          <div>
            <p className="text-xs text-gray-500">Doanh thu dự kiến</p>
            <p className="font-bold text-purple-600">
              {((brief.success_metrics?.expected_revenue_vnd || 0) / 1000000).toFixed(1)}M VNĐ
            </p>
          </div>
        </div>
      </div>

      <div className="mb-4">
        <div className="flex flex-wrap gap-2">
          {brief.hashtags?.slice(0, showDetails ? undefined : 4).map((tag: string) => (
            <span key={tag} className="text-xs bg-blue-50 text-blue-700 px-3 py-1 rounded-full border border-blue-200">
              {tag}
            </span>
          ))}
          {!showDetails && brief.hashtags?.length > 4 && (
            <span className="text-xs text-gray-500 px-2 py-1">
              +{brief.hashtags.length - 4} more
            </span>
          )}
        </div>
      </div>

      {showDetails && (
        <div className="mt-4 pt-4 border-t space-y-4">
          <div>
            <h4 className="font-semibold text-sm mb-2">Kịch bản lồng tiếng:</h4>
            <p className="text-sm text-gray-600 leading-relaxed bg-gray-50 p-3 rounded">
              {brief.vietnamese_voiceover}
            </p>
          </div>

          {brief.matched_products && brief.matched_products.length > 0 && (
            <div>
              <h4 className="font-semibold text-sm mb-2">Sản phẩm liên quan:</h4>
              <div className="space-y-2">
                {brief.matched_products.map((product) => (
                  <div key={product.product_id} className="flex justify-between items-center text-sm bg-gray-50 p-2 rounded">
                    <span className="text-gray-700">{product.name}</span>
                    <span className="font-semibold text-gray-900">
                      {product.price_vnd.toLocaleString()} VNĐ
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="flex items-center gap-2 text-sm">
            <span className="font-semibold">Thời gian đăng tối ưu:</span>
            <span className="text-gray-600">{brief.optimal_posting_time}</span>
          </div>

          <div className="flex items-center gap-2 text-sm">
            <span className="font-semibold">Định dạng:</span>
            <span className="text-gray-600">{brief.content_format}</span>
          </div>
        </div>
      )}

      <button
        onClick={() => setShowDetails(!showDetails)}
        className="w-full mt-3 py-2 text-sm text-blue-600 font-medium flex items-center justify-center gap-2 hover:bg-blue-50 rounded"
      >
        {showDetails ? (
          <>
            <ChevronUp className="w-4 h-4" />
            Ẩn chi tiết
          </>
        ) : (
          <>
            <ChevronDown className="w-4 h-4" />
            Xem chi tiết
          </>
        )}
      </button>

      <div className="flex gap-3 mt-4">
        <button onClick={onApprove} className="flex-1 flex items-center justify-center gap-2 px-4 py-3 bg-green-600 text-white rounded-lg font-semibold">
          <ThumbsUp className="w-4 h-4" />
          Phê duyệt
        </button>
        <button onClick={onReject} className="flex-1 flex items-center justify-center gap-2 px-4 py-3 bg-red-600 text-white rounded-lg font-semibold">
          <ThumbsDown className="w-4 h-4" />
          Từ chối
        </button>
      </div>

      {brief.success_metrics?.target_views > 40000 && (
        <div className="mt-3 p-3 bg-green-50 border border-green-200 rounded-lg">
          <p className="text-sm text-green-800 font-medium">
            AI đề xuất: PHÊ DUYỆT - Tiềm năng cao ({brief.success_metrics.target_views.toLocaleString()} views)
          </p>
        </div>
      )}
    </div>
  );
}
