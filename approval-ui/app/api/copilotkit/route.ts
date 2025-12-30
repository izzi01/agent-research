import {
  CopilotRuntime,
  OpenAIAdapter,
  copilotRuntimeNextJSAppRouterEndpoint,
} from "@copilotkit/runtime";
import { NextRequest } from "next/server";

const runtime = new CopilotRuntime({
  actions: [
    {
      name: "get_pending_briefs",
      description: "Lấy danh sách các bản dự thảo nội dung đang chờ phê duyệt",
      parameters: [],
      handler: async () => {
        try {
          const response = await fetch('http://localhost:8080/api/v1/approvals/pending');
          const data = await response.json();
          return {
            briefs: data,
            count: data.length,
            message: `Hiện có ${data.length} nội dung đang chờ phê duyệt`,
          };
        } catch (error) {
          return {
            error: "Không thể tải danh sách nội dung",
            briefs: [],
            count: 0,
          };
        }
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
      handler: async ({ brief_id, feedback }: { brief_id: string; feedback?: string }) => {
        try {
          await fetch('http://localhost:8080/api/v1/approvals/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              brief_id,
              approved: true,
              feedback,
            }),
          });
          return {
            success: true,
            message: `✅ Đã phê duyệt nội dung ${brief_id}`,
          };
        } catch (error) {
          return {
            success: false,
            message: `❌ Lỗi khi phê duyệt nội dung ${brief_id}`,
          };
        }
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
      handler: async ({ brief_id, feedback }: { brief_id: string; feedback: string }) => {
        try {
          await fetch('http://localhost:8080/api/v1/approvals/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              brief_id,
              approved: false,
              feedback,
            }),
          });
          return {
            success: true,
            message: `❌ Đã từ chối nội dung ${brief_id}`,
          };
        } catch (error) {
          return {
            success: false,
            message: `Lỗi khi từ chối nội dung ${brief_id}`,
          };
        }
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
