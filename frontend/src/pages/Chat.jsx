import { useState, useEffect, useRef } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { useNavigate, Link } from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import { logout } from '../features/auth/authSlice'
import api from '../api/axios'

export default function Chat() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [clearing, setClearing] = useState(false)
  const name = useSelector((state) => state.auth.name)
  const dispatch = useDispatch()
  const navigate = useNavigate()
  const bottomRef = useRef(null)

  useEffect(() => {
    api.get('/chat/history').then((res) => {
      setMessages(res.data)
    })
  }, [])

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const sendMessage = async () => {
    if (!input.trim()) return
    const userMsg = { role: 'user', content: input }
    setMessages((prev) => [...prev, userMsg])
    setInput('')
    setLoading(true)
    try {
      const res = await api.post('/chat/', { message: userMsg.content })
      setMessages((prev) => [...prev, { role: 'assistant', content: res.data.response }])
    } catch {
      setMessages((prev) => [...prev, { role: 'assistant', content: 'Something went wrong. Try again.' }])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  const handleLogout = () => {
    dispatch(logout())
    navigate('/login')
  }

  const handleClearHistory = async () => {
    setClearing(true)
    try {
      await api.delete('/chat/history')
      setMessages([])
    } catch {
    } finally {
      setClearing(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-950 flex flex-col">
      <div className="flex justify-between items-center px-6 py-4 border-b border-gray-800">
        <h1 className="text-white font-bold text-lg">
          Clairo <span className="text-indigo-400 text-sm font-normal">AI Career Advisor</span>
        </h1>
        <div className="flex items-center gap-4">
          <span className="text-gray-400 text-sm">{name}</span>
          <Link to="/profile" className="text-indigo-400 text-sm">Profile</Link>
          <button
            onClick={handleClearHistory}
            disabled={clearing || messages.length === 0}
            className="text-gray-500 text-sm hover:text-red-400 disabled:opacity-30 transition"
          >
            {clearing ? 'Clearing...' : 'Clear chat'}
          </button>
          <button onClick={handleLogout} className="text-gray-500 text-sm hover:text-white">Logout</button>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto px-6 py-4 space-y-4">
        {messages.length === 0 && (
          <p className="text-gray-600 text-sm text-center mt-20">Ask me about your career, skills, or interview prep.</p>
        )}
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[75%] px-4 py-3 rounded-2xl text-sm ${
              msg.role === 'user' ? 'bg-indigo-600 text-white whitespace-pre-wrap' : 'bg-gray-800 text-gray-200'
            }`}>
              {msg.role === 'assistant' ? (
                <ReactMarkdown
                  components={{
                    p: ({ children }) => <p className="mb-2 last:mb-0">{children}</p>,
                    ul: ({ children }) => <ul className="list-disc list-inside mb-2 space-y-1">{children}</ul>,
                    ol: ({ children }) => <ol className="list-decimal list-inside mb-2 space-y-1">{children}</ol>,
                    li: ({ children }) => <li className="text-gray-300">{children}</li>,
                    strong: ({ children }) => <strong className="text-white font-semibold">{children}</strong>,
                    h1: ({ children }) => <h1 className="text-base font-bold text-white mb-1">{children}</h1>,
                    h2: ({ children }) => <h2 className="text-sm font-bold text-white mb-1">{children}</h2>,
                    h3: ({ children }) => <h3 className="text-sm font-semibold text-indigo-300 mb-1">{children}</h3>,
                    code: ({ children }) => <code className="bg-gray-700 text-indigo-300 px-1 rounded text-xs">{children}</code>,
                  }}
                >
                  {msg.content}
                </ReactMarkdown>
              ) : (
                msg.content
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-gray-800 text-gray-400 px-4 py-3 rounded-2xl text-sm">Thinking...</div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <div className="px-6 py-4 border-t border-gray-800 flex gap-3">
        <textarea
          rows={1}
          className="flex-1 bg-gray-800 text-white rounded-xl px-4 py-2 outline-none resize-none text-sm"
          placeholder="Ask Clairo anything..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
        />
        <button
          onClick={sendMessage}
          disabled={loading || !input.trim()}
          className="bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white px-5 rounded-xl transition"
        >
          Send
        </button>
      </div>
    </div>
  )
}