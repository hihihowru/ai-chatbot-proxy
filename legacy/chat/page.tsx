'use client';
import React, { useState, useEffect } from 'react';
import StockSnapshotCard from '../components/StockSnapshotCard';
import AskQuestionBar from '../components/AskQuestionBar';
import WatchlistSummaryCard from '../components/WatchlistSummaryCard';

function getQueryParam(name: string) {
  if (typeof window === 'undefined') return '';
  const url = new URL(window.location.href);
  return url.searchParams.get(name) || '';
}

function isWatchlistSummaryQuestion(q: string) {
  // Example: "自選股摘要:[2330 台積電, 2454 聯發科]"
  return q.startsWith('自選股摘要:');
}

export default function ChatPage() {
  const [page, setPage] = useState<'main' | 'teslaCard'>('main');
  const [question, setQuestion] = useState('');
  const [chat, setChat] = useState<{role: 'user'|'ai', text: string}[]>([]);
  const [sections, setSections] = useState<any[]>([]);
  const [logs, setLogs] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  // 熱門話題 mock
  const hotTopics = [
    { label: 'tesla 表現如何（詳細版圖卡）', action: () => setPage('teslaCard') },
    { label: '台積電法說會重點', action: () => alert('台積電法說會重點') },
    { label: 'AI 概念股', action: () => alert('AI 概念股') },
  ];

  // 自動讀取 query string 並送出
  useEffect(() => {
    const q = getQueryParam('question');
    if (q) {
      setQuestion(q);
      handleSubmit(q);
    }
  }, []);

  async function handleSubmit(q: string) {
    setLoading(true);
    setSections([]);
    setLogs([]);
    setChat(prev => [...prev, {role: 'user', text: q}]);
    if (isWatchlistSummaryQuestion(q)) {
      // Parse stock list from question
      const match = q.match(/\[(.*)\]/);
      let stock_list: number[] = [];
      if (match && match[1]) {
        stock_list = match[1].split(',').map(s => {
          const stockMatch = s.trim().match(/^(\d+)/);
          return stockMatch ? parseInt(stockMatch[1]) : null;
        }).filter(id => id !== null) as number[];
      }
      // SSE streaming
      const eventSource = new EventSource('/api/watchlist-summary-sse?stock_list=' + encodeURIComponent(JSON.stringify(stock_list)));
      eventSource.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          if (data.log) {
            setLogs(prev => [...prev, data.log]);
            setChat(prev => [...prev, {role: 'ai', text: data.log}]);
          }
          if (data.sections) {
            setSections(data.sections);
            setLoading(false);
            eventSource.close();
          }
        } catch (e) {}
      };
      eventSource.onerror = () => {
        setLoading(false);
        setChat(prev => [...prev, {role: 'ai', text: '取得回覆時發生錯誤'}]);
        eventSource.close();
      };
    } else {
      // fallback: old API
      setLogs([]);
      setSections([]);
      try {
        const res = await fetch('/api/ask-llm', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ question: q })
        });
        const data = await res.json();
        setChat(prev => [...prev, {role: 'ai', text: data.answer || '沒有取得回覆'}]);
      } catch (e) {
        setChat(prev => [...prev, {role: 'ai', text: '取得回覆時發生錯誤'}]);
      } finally {
        setLoading(false);
      }
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-100 pb-16">
      {page === 'main' && (
        <div className="max-w-md mx-auto pt-4 space-y-6">
          <h2 className="font-bold text-lg mb-2">熱門話題</h2>
          <div className="space-y-2">
            {hotTopics.map((topic, idx) => (
              <button
                key={topic.label}
                className="w-full text-left px-4 py-3 rounded-xl bg-white/80 shadow hover:bg-blue-50 transition font-medium text-gray-800"
                onClick={topic.action}
              >
                {topic.label}
              </button>
            ))}
          </div>
        </div>
      )}
      {page === 'teslaCard' && (
        <div className="max-w-xl mx-auto pt-8">
          <StockSnapshotCard />
        </div>
      )}
      <div className="max-w-xl mx-auto mt-8">
        <AskQuestionBar
          onSubmit={handleSubmit}
        />
        {/* Chat bubbles */}
        <div className="space-y-4 mt-4">
          {chat.map((msg, idx) => (
            <div key={idx} className={msg.role === 'user' ? 'text-right' : 'text-left'}>
              <div className={
                'inline-block px-4 py-2 rounded-xl shadow ' +
                (msg.role === 'user' ? 'bg-blue-600 text-white' : 'bg-white/80 text-gray-800')
              }>
                {msg.text}
              </div>
            </div>
          ))}
        </div>
        {/* Sectioned summary card output */}
        {sections.length > 0 && (
          <div className="mt-6">
            <WatchlistSummaryCard sections={sections} />
          </div>
        )}
        {loading && <div className="mt-4 text-blue-600">分析中...</div>}
      </div>
      {/* FooterNav or chat footer */}
      <div className="fixed bottom-0 left-0 right-0 bg-white/80 backdrop-blur border-t border-gray-200 py-3 flex justify-center z-10">
        <button
          className="px-6 py-2 rounded bg-blue-600 text-white font-bold shadow hover:bg-blue-700 transition"
          onClick={() => setPage('main')}
        >
          回到主頁
        </button>
      </div>
    </div>
  );
} 