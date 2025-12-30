"use client";

import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { CopilotKit } from "@copilotkit/react-core";
import { CopilotSidebar } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useState } from "react";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const [queryClient] = useState(() => new QueryClient());

  return (
    <html lang="vi">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <QueryClientProvider client={queryClient}>
          <CopilotKit 
            runtimeUrl="/api/copilotkit"
            publicApiKey={process.env.NEXT_PUBLIC_COPILOT_API_KEY}
          >
            <CopilotSidebar
              instructions={`
                Bạn là trợ lý AI chuyên phê duyệt nội dung tiếp thị tiếng Việt.
                
                Nhiệm vụ của bạn:
                1. Hiển thị các bản dự thảo nội dung đang chờ phê duyệt
                2. Phân tích chất lượng nội dung tiếng Việt
                3. Đề xuất phê duyệt hoặc từ chối dựa trên:
                   - Chất lượng hook (độ dài, hấp dẫn)
                   - Số lượng hashtag (tối ưu: 4-8)
                   - Dự báo lượt xem (cao: >40K, trung bình: 20-40K)
                   - Tiềm năng doanh thu
                4. Hỗ trợ phê duyệt hàng loạt
                
                Khi phân tích nội dung:
                - Hook ngắn (<50 ký tự) → "Cần cải thiện hook"
                - Lượt xem dự kiến >40K → "Đề xuất PHÊ DUYỆT - Tiềm năng cao"
                - Hashtag <3 → "Cần thêm hashtag"
                
                Phong cách: Thân thiện, chuyên nghiệp, cung cấp số liệu cụ thể
              `}
              labels={{
                title: "Trợ Lý Phê Duyệt AI",
                initial: "Xin chào! Tôi có thể giúp bạn:\n\n✓ Phân tích chất lượng nội dung\n✓ Đề xuất phê duyệt/từ chối\n✓ Phê duyệt hàng loạt\n\nHãy hỏi tôi bất cứ điều gì!",
                placeholder: "Hỏi về nội dung cần phê duyệt...",
              }}
              defaultOpen={true}
            >
              {children}
            </CopilotSidebar>
          </CopilotKit>
        </QueryClientProvider>
      </body>
    </html>
  );
}
