import { useState } from 'react'
import { Link } from 'react-router-dom'
import api from '../api/axios'

export default function Profile() {
  const [file, setFile] = useState(null)
  const [profile, setProfile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleUpload = async () => {
    if (!file) return
    setLoading(true)
    setError('')
    try {
      const formData = new FormData()
      formData.append('file', file)
      const res = await api.post('/profile/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      setProfile(res.data.profile)
    } catch (err) {
      setError(err.response?.data?.detail || 'Upload failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white p-8">
      <div className="max-w-2xl mx-auto space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-bold">Your Profile</h1>
          <Link to="/" className="text-indigo-400 text-sm">← Back to Chat</Link>
        </div>
        <div className="bg-gray-900 p-6 rounded-2xl space-y-4">
          <p className="text-gray-400 text-sm">Upload your resume (PDF) to personalize Clairo's advice.</p>
          <input
            type="file"
            accept=".pdf"
            onChange={(e) => setFile(e.target.files[0])}
            className="text-sm text-gray-300"
          />
          <button
            onClick={handleUpload}
            disabled={loading || !file}
            className="bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white px-5 py-2 rounded-lg transition"
          >
            {loading ? 'Parsing...' : 'Upload Resume'}
          </button>
          {error && <p className="text-red-400 text-sm">{error}</p>}
        </div>
        {profile && (
          <div className="bg-gray-900 p-6 rounded-2xl space-y-3">
            <h2 className="text-lg font-semibold">{profile.full_name}</h2>
            <p className="text-gray-400 text-sm">{profile.summary}</p>
            <div>
              <p className="text-xs text-gray-500 uppercase mb-1">Skills</p>
              <div className="flex flex-wrap gap-2">
                {profile.skills?.map((s) => (
                  <span key={s} className="bg-indigo-900 text-indigo-200 text-xs px-2 py-1 rounded-full">{s}</span>
                ))}
              </div>
            </div>
            <div>
              <p className="text-xs text-gray-500 uppercase mb-1">Experience</p>
              {profile.experience?.map((e, i) => (
                <p key={i} className="text-sm text-gray-300">{e.role} @ {e.company} ({e.years})</p>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}