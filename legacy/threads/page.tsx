"use client";

import FooterNav from '../components/FooterNav';
import ThreadItem from '../components/ThreadItem';
import AiReplyModal from '../components/AiReplyModal';
import CardFooter from '../components/CardFooter';
import AskQuestionBar from '../components/AskQuestionBar';
import { useState } from 'react';

const mockThreads = [
  {
    id: "t1",
    user: { avatar: "/avatars/user1.png", name: "小明" },
    question: "台積電為什麼漲停？",
    tags: ["台積電", "AI", "技術分析"],
    aiReplyCards: [
      {
        type: "技術分析",
        image: "/mock/tsmc_chart.png",
        summary: "短線均線多頭排列，成交量放大，技術面偏多。",
        footer: <CardFooter source="TradingView" onReadMore={() => alert('看更多技術分析！')} />
      },
      {
        type: "新聞摘要",
        image: "/mock/tsmc_news.png",
        summary: "台積電今日漲停，法人看好先進製程。",
        footer: <CardFooter source="經濟日報" onReadMore={() => alert('看更多新聞！')} />
      },
      {
        type: "籌碼分析",
        image: "/mock/chips.png",
        summary: "外資連續買超，投信同步加碼，籌碼面偏多。",
        footer: <CardFooter source="CMoney" onReadMore={() => alert('看更多籌碼分析！')} />
      },
      {
        type: "法人動向",
        image: "/mock/institutional.png",
        summary: "外資、投信同步加碼，主力偏多。",
        footer: <CardFooter source="CMoney" onReadMore={() => alert('看更多法人動向！')} />
      },
      {
        type: "AI 總結",
        image: "/mock/ai_summary.png",
        summary: "技術面與籌碼面皆多方，短線有望續強。",
        footer: <CardFooter onAskMore={() => alert('追問 AI！')} />
      }
    ],
    aiReplyCollapsed: false,
    stats: { like: 12, comment: 3, favorite: 5, share: 2 },
    quoteThread: null
  },
  {
    id: "t2",
    user: { avatar: "/avatars/user2.png", name: "小美" },
    question: "聯電今天有什麼新聞？",
    tags: ["聯電", "新聞摘要"],
    aiReplyCards: [
      {
        type: "新聞摘要",
        image: "/mock/umc_news.png",
        summary: "聯電今日漲停，外資連續買超，市場信心回溫。",
        footer: <CardFooter source="工商時報" onReadMore={() => alert('看更多聯電新聞！')} />
      },
      {
        type: "技術分析",
        image: "/mock/umc_chart.png",
        summary: "均線多頭排列，技術面偏多。",
        footer: <CardFooter source="TradingView" onReadMore={() => alert('看更多技術分析！')} />
      },
      {
        type: "法人動向",
        image: "/mock/institutional.png",
        summary: "外資連續買超，主力偏多。",
        footer: <CardFooter source="CMoney" onReadMore={() => alert('看更多法人動向！')} />
      },
      {
        type: "AI 總結",
        image: "/mock/ai_summary.png",
        summary: "聯電短線有望續強，建議留意法人動向。",
        footer: <CardFooter onAskMore={() => alert('追問聯電 AI！')} />
      }
    ],
    aiReplyCollapsed: false,
    stats: { like: 8, comment: 1, favorite: 2, share: 1 },
    quoteThread: null
  },
  {
    id: "t3",
    user: { avatar: "/avatars/user3.png", name: "阿財" },
    question: "請問法人買賣超對股價有什麼影響？",
    tags: ["法人買賣超", "籌碼分析"],
    aiReplyCards: [
      {
        type: "法人買賣超",
        image: "/mock/institutional.png",
        summary: "外資連續買超 5 日，投信同步加碼，顯示主力偏多。",
        footer: <CardFooter source="CMoney" onReadMore={() => alert('看法人買賣超細節！')} />
      },
      {
        type: "技術分析",
        image: "/mock/chips.png",
        summary: "技術面偏多，短線有望續強。",
        footer: <CardFooter source="TradingView" onReadMore={() => alert('看更多技術分析！')} />
      },
      {
        type: "AI 解讀",
        image: "/mock/ai_summary.png",
        summary: "法人買超通常帶動短線股價上漲，但仍需留意量能與技術面。",
        footer: <CardFooter onAskMore={() => alert('追問法人動向！')} />
      }
    ],
    aiReplyCollapsed: false,
    stats: { like: 20, comment: 5, favorite: 10, share: 3 },
    quoteThread: {
      question: "法人買賣超是什麼？"
    }
  },
  {
    id: "t4",
    user: { avatar: "/avatars/user4.png", name: "小志" },
    question: "聯發科未來展望如何？",
    tags: ["聯發科", "產業分析"],
    aiReplyCards: [
      {
        type: "產業分析",
        image: "/mock/mediatek.png",
        summary: "5G 晶片需求持續成長，聯發科市佔率提升。",
        footer: <CardFooter source="工商時報" onReadMore={() => alert('看更多產業分析！')} />
      },
      {
        type: "AI 總結",
        image: "/mock/ai_summary.png",
        summary: "基本面穩健，長線看好。",
        footer: <CardFooter onAskMore={() => alert('追問聯發科 AI！')} />
      }
    ],
    aiReplyCollapsed: true,
    stats: { like: 15, comment: 2, favorite: 7, share: 1 },
    quoteThread: null
  },
  {
    id: "t5",
    user: { avatar: "/avatars/user5.png", name: "小華" },
    question: "鴻海電動車進度如何？",
    tags: ["鴻海", "電動車"],
    aiReplyCards: [
      {
        type: "新聞摘要",
        image: "/mock/foxconn_ev.png",
        summary: "鴻海積極布局電動車，與多家車廠合作。",
        footer: <CardFooter source="經濟日報" onReadMore={() => alert('看更多鴻海新聞！')} />
      },
      {
        type: "AI 總結",
        image: "/mock/ai_summary.png",
        summary: "電動車題材持續發酵，值得關注。",
        footer: <CardFooter onAskMore={() => alert('追問鴻海 AI！')} />
      }
    ],
    aiReplyCollapsed: true,
    stats: { like: 10, comment: 1, favorite: 3, share: 0 },
    quoteThread: null
  },
  {
    id: "t6",
    user: { avatar: "/avatars/user6.png", name: "小安" },
    question: "長榮航運股價為什麼大漲？",
    tags: ["長榮", "航運"],
    aiReplyCards: [
      {
        type: "新聞摘要",
        image: "/mock/evergreen.png",
        summary: "運價上漲，帶動長榮航運股價大漲。",
        footer: <CardFooter source="工商時報" onReadMore={() => alert('看更多長榮新聞！')} />
      },
      {
        type: "AI 總結",
        image: "/mock/ai_summary.png",
        summary: "航運景氣回溫，短線有望續強。",
        footer: <CardFooter onAskMore={() => alert('追問長榮 AI！')} />
      }
    ],
    aiReplyCollapsed: true,
    stats: { like: 7, comment: 0, favorite: 2, share: 0 },
    quoteThread: null
  },
  {
    id: "t7",
    user: { avatar: "/avatars/user7.png", name: "小婷" },
    question: "國泰金殖利率高嗎？",
    tags: ["國泰金", "金融股"],
    aiReplyCards: [
      {
        type: "數據分析",
        image: "/mock/cathay.png",
        summary: "國泰金殖利率高於同業，吸引存股族。",
        footer: <CardFooter source="CMoney" onReadMore={() => alert('看更多國泰金數據！')} />
      },
      {
        type: "AI 總結",
        image: "/mock/ai_summary.png",
        summary: "金融股穩健，適合長期投資。",
        footer: <CardFooter onAskMore={() => alert('追問國泰金 AI！')} />
      }
    ],
    aiReplyCollapsed: true,
    stats: { like: 9, comment: 1, favorite: 4, share: 1 },
    quoteThread: null
  },
  {
    id: "t8",
    user: { avatar: "/avatars/user8.png", name: "小傑" },
    question: "台達電 ESG 表現如何？",
    tags: ["台達電", "ESG"],
    aiReplyCards: [
      {
        type: "ESG 評比",
        image: "/mock/delta.png",
        summary: "台達電 ESG 評比優異，獲多項國際認證。",
        footer: <CardFooter source="經濟日報" onReadMore={() => alert('看更多 ESG 資訊！')} />
      },
      {
        type: "AI 總結",
        image: "/mock/ai_summary.png",
        summary: "ESG 表現佳，有助企業永續發展。",
        footer: <CardFooter onAskMore={() => alert('追問台達電 AI！')} />
      }
    ],
    aiReplyCollapsed: true,
    stats: { like: 6, comment: 0, favorite: 1, share: 0 },
    quoteThread: null
  },
  {
    id: "t9",
    user: { avatar: "/avatars/user9.png", name: "小芸" },
    question: "群創面板價格走勢？",
    tags: ["群創", "面板"],
    aiReplyCards: [
      {
        type: "產業分析",
        image: "/mock/innolux.png",
        summary: "面板價格回升，群創營收成長。",
        footer: <CardFooter source="工商時報" onReadMore={() => alert('看更多面板分析！')} />
      },
      {
        type: "AI 總結",
        image: "/mock/ai_summary.png",
        summary: "面板產業景氣回溫，值得留意。",
        footer: <CardFooter onAskMore={() => alert('追問群創 AI！')} />
      }
    ],
    aiReplyCollapsed: true,
    stats: { like: 5, comment: 0, favorite: 1, share: 0 },
    quoteThread: null
  },
  {
    id: "t10",
    user: { avatar: "/avatars/user10.png", name: "小宏" },
    question: "大立光營收創新高？",
    tags: ["大立光", "營收"],
    aiReplyCards: [
      {
        type: "新聞摘要",
        image: "/mock/largan.png",
        summary: "大立光 6 月營收創新高，市場看好後市。",
        footer: <CardFooter source="經濟日報" onReadMore={() => alert('看更多大立光新聞！')} />
      },
      {
        type: "AI 總結",
        image: "/mock/ai_summary.png",
        summary: "營收成長動能強，股價有望續揚。",
        footer: <CardFooter onAskMore={() => alert('追問大立光 AI！')} />
      }
    ],
    aiReplyCollapsed: true,
    stats: { like: 11, comment: 2, favorite: 3, share: 1 },
    quoteThread: null
  },
  {
    id: "t11",
    user: { avatar: "/avatars/user11.png", name: "小美" },
    question: "台塑化油價展望？",
    tags: ["台塑化", "油價"],
    aiReplyCards: [
      {
        type: "產業分析",
        image: "/mock/fpc.png",
        summary: "國際油價波動，台塑化營運受影響。",
        footer: <CardFooter source="工商時報" onReadMore={() => alert('看更多油價分析！')} />
      },
      {
        type: "AI 總結",
        image: "/mock/ai_summary.png",
        summary: "油價波動需留意，建議分散投資。",
        footer: <CardFooter onAskMore={() => alert('追問台塑化 AI！')} />
      }
    ],
    aiReplyCollapsed: true,
    stats: { like: 4, comment: 0, favorite: 1, share: 0 },
    quoteThread: null
  },
  {
    id: "t12",
    user: { avatar: "/avatars/user12.png", name: "小強" },
    question: "中鋼鋼價走勢？",
    tags: ["中鋼", "鋼鐵"],
    aiReplyCards: [
      {
        type: "產業分析",
        image: "/mock/csc.png",
        summary: "鋼價回升，中鋼營運改善。",
        footer: <CardFooter source="經濟日報" onReadMore={() => alert('看更多鋼價分析！')} />
      },
      {
        type: "AI 總結",
        image: "/mock/ai_summary.png",
        summary: "鋼鐵產業景氣回溫，值得關注。",
        footer: <CardFooter onAskMore={() => alert('追問中鋼 AI！')} />
      }
    ],
    aiReplyCollapsed: true,
    stats: { like: 3, comment: 0, favorite: 1, share: 0 },
    quoteThread: null
  }
];

export default function ThreadsPage() {
  const [aiModalOpen, setAiModalOpen] = useState(false);
  const [expandedThread, setExpandedThread] = useState<string | null>(null);
  const [modalQuestion, setModalQuestion] = useState<string>("");

  const handleAiReply = (question: string) => {
    setModalQuestion(question);
    setAiModalOpen(true);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-100 pb-16">
      <div className="max-w-md mx-auto pt-4 space-y-4">
        {mockThreads.map(thread => (
          <ThreadItem
            key={thread.id}
            {...thread}
            aiReplyCollapsed={typeof thread.aiReplyCollapsed === 'boolean' ? thread.aiReplyCollapsed : expandedThread !== thread.id}
            onExpandAiReply={() => setExpandedThread(thread.id)}
            onAiReply={() => handleAiReply(thread.question)}
          />
        ))}
      </div>
      <AiReplyModal open={aiModalOpen} onClose={() => setAiModalOpen(false)} defaultText={modalQuestion} />
      <AskQuestionBar onSubmit={q => alert('你問了: ' + q)} />
      <FooterNav active="threads" />
    </div>
  );
} 