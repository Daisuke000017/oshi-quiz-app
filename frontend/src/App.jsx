import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Link, useNavigate, useParams, useLocation } from 'react-router-dom'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Sparkles, Trophy, Clock, Target, Home, Plus, TrendingUp, Heart, Star, User } from 'lucide-react'
import './App.css'

const API_BASE = import.meta.env.VITE_API_URL ? `${import.meta.env.VITE_API_URL}/api` : '/api'

// LocalStorageからプレイヤー情報を取得/保存するユーティリティ
const getPlayerName = () => localStorage.getItem('playerName') || ''
const setPlayerName = (name) => localStorage.setItem('playerName', name)
const getUserId = () => localStorage.getItem('userId') || null
const setUserId = (id) => localStorage.setItem('userId', id)

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-oshinoko-dark custom-scrollbar">
        <Header />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/quiz/:id" element={<QuizDetailPage />} />
            <Route path="/quiz/:id/play" element={<QuizPlayPage />} />
            <Route path="/quiz/:id/result" element={<QuizResultPage />} />
            <Route path="/quiz/:id/ranking" element={<RankingPage />} />
            <Route path="/create" element={<CreateQuizPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

function Header() {
  return (
    <header className="glass-card border-b border-purple-400/20 sticky top-0 z-50 shadow-lg">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="flex items-center gap-3 hover:opacity-90 transition-all">
            <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center shadow-xl star-float">
              <Star className="w-8 h-8 text-white star-twinkle" />
            </div>
            <div>
              <h1 className="text-[20px] md:text-2xl font-black text-oshinoko whitespace-nowrap">
                【推しの子】クイズ
              </h1>
              <p className="text-xs text-purple-400 font-medium">Oshi no Ko Quiz</p>
            </div>
          </Link>
          <nav className="flex items-center gap-3">
            <Link to="/">
              <Button variant="ghost" size="sm" className="gap-2 text-gray-700 hover:text-purple-600 hover:bg-purple-50 font-medium">
                <Home className="w-4 h-4" />
                ホーム
              </Button>
            </Link>
          </nav>
        </div>
      </div>
    </header>
  )
}

function HomePage() {
  const [quizzes, setQuizzes] = useState([])
  const [selectedDifficulty, setSelectedDifficulty] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch(`${API_BASE}/quizzes`).then(r => r.json()).then(quizzesData => {
      setQuizzes(quizzesData)
      setLoading(false)
    })
  }, [])

  const difficulties = [
    { value: 'beginner', label: '初級編', color: 'from-green-400 to-green-500' },
    { value: 'intermediate', label: '中級編', color: 'from-yellow-400 to-yellow-500' },
    { value: 'mania', label: '上級編', color: 'from-red-400 to-red-500' },
  ]

  const filteredQuizzes = selectedDifficulty
    ? quizzes.filter(q => q.difficulty === selectedDifficulty)
    : quizzes

  const difficultyColors = {
    beginner: 'bg-green-100 text-green-700 border-green-200',
    intermediate: 'bg-yellow-100 text-yellow-700 border-yellow-200',
    advanced: 'bg-orange-100 text-orange-700 border-orange-200',
    mania: 'bg-red-100 text-red-700 border-red-200'
  }

  const difficultyLabels = {
    beginner: '初級',
    intermediate: '中級',
    advanced: '上級',
    mania: 'マニア級'
  }

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Hero Section */}
      <div className="glass-card-dark text-center space-y-6 py-8 px-6 md:px-8 md:py-12 rounded-3xl overflow-hidden">
        {/* メインビジュアル画像 */}
        <div className="flex justify-center mb-6">
          <div className="relative w-full max-w-md">
            <img
              src="/main-sp.png"
              alt="【推しの子】メインビジュアル"
              className="w-full h-auto rounded-2xl shadow-2xl"
            />
            <Star className="w-8 h-8 text-pink-400 absolute -top-2 -left-2 star-twinkle" />
            <Star className="w-6 h-6 text-purple-400 absolute -top-1 -right-2 star-twinkle" style={{ animationDelay: '0.3s' }} />
          </div>
        </div>
        <h2 className="text-[25px] md:text-4xl font-bold text-oshinoko">
          あなたの知識は本物か？
        </h2>
        <p className="text-purple-200 text-base md:text-lg font-medium">
          アニメ・漫画『【推しの子】』の究極クイズに挑戦！初級から上級まで、あなたの愛と知識が試される
        </p>
      </div>

      {/* Difficulty Filter */}
      <div className="flex justify-center gap-3 flex-wrap">
        <button
          onClick={() => setSelectedDifficulty(null)}
          className={`px-6 py-3 rounded-full font-bold transition-all shadow-md ${
            selectedDifficulty === null
              ? 'btn-oshinoko text-white'
              : 'glass-card text-gray-700 hover:scale-105'
          }`}
        >
          すべて
          <span className="ml-2 text-sm opacity-80">{quizzes.length}</span>
        </button>
        {difficulties.map(diff => {
          const count = quizzes.filter(q => q.difficulty === diff.value).length
          return (
            <button
              key={diff.value}
              onClick={() => setSelectedDifficulty(diff.value)}
              className={`px-6 py-3 rounded-full font-bold transition-all shadow-md ${
                selectedDifficulty === diff.value
                  ? `btn-oshinoko text-white`
                  : 'glass-card text-gray-700 hover:scale-105'
              }`}
            >
              {diff.label}
              <span className="ml-2 text-sm opacity-80">{count}</span>
            </button>
          )
        })}
      </div>

      {/* Quiz List */}
      <div>
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
            <TrendingUp className="w-6 h-6 text-white" />
          </div>
          <h3 className="text-2xl font-bold text-white">クイズ一覧</h3>
          <span className="text-sm text-purple-300 ml-2">{filteredQuizzes.length}件</span>
        </div>

        {loading ? (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-purple-400 border-t-pink-400"></div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredQuizzes.map(quiz => (
              <Card key={quiz.id} className="h-full glass-card border-purple-200 flex flex-col">
                <Link to={`/quiz/${quiz.id}`} className="group flex-1">
                  <CardHeader>
                    <div className="flex items-start justify-between gap-2 mb-2">
                      <Badge className={`${difficultyColors[quiz.difficulty]} border font-medium`}>
                        {difficultyLabels[quiz.difficulty]}
                      </Badge>
                      <Badge variant="outline" className="text-xs bg-purple-50 text-purple-700 border-purple-200">
                        {quiz.oshi_tag?.name}
                      </Badge>
                    </div>
                    <CardTitle className="text-xl text-gray-800 group-hover:text-transparent group-hover:bg-clip-text group-hover:bg-gradient-to-r group-hover:from-purple-600 group-hover:to-pink-600 transition-all">
                      {quiz.title}
                    </CardTitle>
                    <CardDescription className="text-sm text-gray-600">
                      {quiz.description}
                    </CardDescription>
                  </CardHeader>
                </Link>
                <CardFooter className="flex flex-col gap-3 pt-0">
                  <div className="flex items-center gap-4 text-sm text-gray-500 w-full">
                    <div className="flex items-center gap-1">
                      <Target className="w-4 h-4 text-purple-500" />
                      <span>{quiz.question_count}問</span>
                    </div>
                    <div className="flex items-center gap-1">
                      <Trophy className="w-4 h-4 text-pink-500" />
                      <span>{quiz.play_count}回</span>
                    </div>
                  </div>
                  <Link to={`/quiz/${quiz.id}/ranking`} className="w-full" onClick={(e) => e.stopPropagation()}>
                    <Button
                      variant="outline"
                      className="w-full border-2 border-yellow-400 text-yellow-600 hover:bg-yellow-50 font-bold text-sm h-10"
                    >
                      <Trophy className="w-4 h-4 mr-1" />
                      ランキング
                    </Button>
                  </Link>
                </CardFooter>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

function QuizDetailPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [quiz, setQuiz] = useState(null)
  const [loading, setLoading] = useState(true)
  const [showNameModal, setShowNameModal] = useState(false)
  const [playerName, setPlayerNameLocal] = useState(getPlayerName())

  useEffect(() => {
    fetch(`${API_BASE}/quizzes/${id}`)
      .then(r => r.json())
      .then(data => {
        setQuiz(data)
        setLoading(false)
      })
  }, [id])

  const handleStartQuiz = () => {
    if (!playerName.trim()) {
      setShowNameModal(true)
    } else {
      navigate(`/quiz/${id}/play`)
    }
  }

  const handleNameSubmit = async () => {
    if (playerName.trim()) {
      // ユーザーIDが既にある場合は、ユーザー名を更新
      let userId = getUserId()

      if (userId) {
        // 既存ユーザーの名前を更新
        try {
          await fetch(`${API_BASE}/users/${userId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: playerName.trim() })
          })
          setPlayerName(playerName.trim())
        } catch (err) {
          console.error('Failed to update user:', err)
        }
      } else {
        // 新規ユーザーを作成
        try {
          const response = await fetch(`${API_BASE}/users`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: playerName.trim() })
          })
          const newUser = await response.json()
          setUserId(newUser.id)
          setPlayerName(playerName.trim())
        } catch (err) {
          console.error('Failed to create user:', err)
        }
      }

      setShowNameModal(false)
      navigate(`/quiz/${id}/play`)
    }
  }

  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-purple-200 border-t-purple-500"></div>
      </div>
    )
  }

  const difficultyColors = {
    beginner: 'bg-green-100 text-green-700 border-green-200',
    intermediate: 'bg-yellow-100 text-yellow-700 border-yellow-200',
    advanced: 'bg-orange-100 text-orange-700 border-orange-200',
    mania: 'bg-red-100 text-red-700 border-red-200'
  }

  const difficultyLabels = {
    beginner: '初級',
    intermediate: '中級',
    advanced: '上級',
    mania: 'マニア級'
  }

  return (
    <div className="max-w-3xl mx-auto">
      <Card className="glass-card border-purple-200 shadow-2xl">
        <CardHeader className="space-y-6">
          <div className="flex items-center gap-3">
            <Badge className={`${difficultyColors[quiz.difficulty]} border font-bold text-base px-4 py-1`}>
              {difficultyLabels[quiz.difficulty]}
            </Badge>
            <Badge variant="outline" className="bg-purple-50 text-purple-700 border-purple-200 font-bold text-base px-4 py-1">
              {quiz.oshi_tag?.name}
            </Badge>
          </div>
          <CardTitle className="text-4xl font-black text-oshinoko leading-tight">
            {quiz.title}
          </CardTitle>
          <CardDescription className="text-lg text-gray-600 leading-relaxed">
            {quiz.description}
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-8">
          <div className="grid grid-cols-3 gap-6">
            <div className="text-center p-6 bg-gradient-to-br from-purple-50 to-purple-100 rounded-2xl border-2 border-purple-200 shadow-lg">
              <div className="text-4xl font-black text-purple-600 mb-2">{quiz.question_count}</div>
              <div className="text-sm text-gray-600 font-bold">問題数</div>
            </div>
            <div className="text-center p-6 bg-gradient-to-br from-pink-50 to-pink-100 rounded-2xl border-2 border-pink-200 shadow-lg">
              <div className="text-4xl font-black text-pink-600 mb-2">{quiz.play_count}</div>
              <div className="text-sm text-gray-600 font-bold">挑戦回数</div>
            </div>
            <div className="text-center p-6 bg-gradient-to-br from-blue-50 to-blue-100 rounded-2xl border-2 border-blue-200 shadow-lg">
              <div className="text-4xl font-black text-blue-600 mb-2">{quiz.average_score.toFixed(0)}%</div>
              <div className="text-sm text-gray-600 font-bold">平均正答率</div>
            </div>
          </div>

          <div className="space-y-4">
            <Button
              onClick={handleStartQuiz}
              className="btn-oshinoko w-full h-16 text-xl font-black text-white"
            >
              <span className="relative z-10 flex items-center justify-center gap-3">
                <Sparkles className="w-6 h-6" />
                クイズに挑戦する
              </span>
            </Button>
            <Button
              onClick={() => navigate(`/quiz/${id}/ranking`)}
              variant="outline"
              className="w-full h-14 border-2 border-yellow-400 text-yellow-600 hover:bg-yellow-50 font-bold text-lg"
            >
              <Trophy className="w-5 h-5 mr-2" />
              ランキングを見る
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* プレイヤー名入力モーダル */}
      {showNameModal && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <Card className="glass-card border-purple-200 shadow-2xl max-w-md w-full">
            <CardHeader className="space-y-4">
              <div className="flex justify-center">
                <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-purple-400 to-pink-400 flex items-center justify-center shadow-lg">
                  <User className="w-9 h-9 text-white" />
                </div>
              </div>
              <CardTitle className="text-2xl font-black text-oshinoko text-center">
                プレイヤー名を入力
              </CardTitle>
              <CardDescription className="text-center text-base">
                ランキングに記録するための名前を入力してください
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <input
                  type="text"
                  value={playerName}
                  onChange={(e) => setPlayerNameLocal(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleNameSubmit()}
                  placeholder="例: 推しの子ファン"
                  className="w-full px-4 py-3 border-2 border-purple-200 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent text-lg"
                  maxLength={20}
                  autoFocus
                />
                <p className="text-xs text-gray-500 mt-2">最大20文字まで</p>
              </div>
              <div className="flex gap-3">
                <Button
                  onClick={() => setShowNameModal(false)}
                  variant="outline"
                  className="flex-1 h-12 border-2 border-purple-300 text-purple-600 hover:bg-purple-50 font-bold"
                >
                  キャンセル
                </Button>
                <Button
                  onClick={handleNameSubmit}
                  disabled={!playerName.trim()}
                  className="btn-oshinoko flex-1 h-12 text-white font-bold disabled:opacity-50"
                >
                  <span className="relative z-10">開始</span>
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  )
}

function QuizPlayPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [quiz, setQuiz] = useState(null)
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [answers, setAnswers] = useState({})
  const [loading, setLoading] = useState(true)
  const [startTime] = useState(Date.now())

  useEffect(() => {
    fetch(`${API_BASE}/quizzes/${id}?include_questions=true`)
      .then(r => r.json())
      .then(data => {
        setQuiz(data)
        setLoading(false)
      })
  }, [id])

  if (loading || !quiz) {
    return (
      <div className="text-center py-12">
        <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-purple-200 border-t-purple-500"></div>
      </div>
    )
  }

  const currentQuestion = quiz.questions[currentQuestionIndex]
  const progress = ((currentQuestionIndex + 1) / quiz.questions.length) * 100

  const handleAnswer = (choiceId) => {
    setAnswers({ ...answers, [currentQuestion.id]: choiceId })
  }

  const handleNext = () => {
    if (currentQuestionIndex < quiz.questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1)
    } else {
      submitQuiz()
    }
  }

  const submitQuiz = () => {
    const timeTaken = Math.floor((Date.now() - startTime) / 1000)
    const answersList = quiz.questions.map(q => ({
      question_id: q.id,
      selected_choice_id: answers[q.id]
    }))

    // ローカルストレージからユーザーIDを取得（なければ1をデフォルト）
    const userId = getUserId() || 1

    fetch(`${API_BASE}/quizzes/${id}/submit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_id: parseInt(userId),
        answers: answersList,
        time_taken: timeTaken
      })
    })
      .then(r => r.json())
      .then(result => {
        navigate(`/quiz/${id}/result`, { state: { result, answers } })
      })
  }

  const isAnswered = answers[currentQuestion.id] !== undefined

  return (
    <div className="max-w-3xl mx-auto">
      {/* Progress Bar */}
      <div className="mb-8 glass-card rounded-3xl p-6 shadow-lg border border-purple-200">
        <div className="flex items-center justify-between mb-3">
          <span className="text-sm font-bold text-gray-700">
            問題 {currentQuestionIndex + 1} / {quiz.questions.length}
          </span>
          <span className="text-sm font-bold text-oshinoko">{Math.round(progress)}%</span>
        </div>
        <div className="relative w-full bg-purple-100 rounded-full h-4 overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-purple-500 via-pink-500 to-purple-500 transition-all duration-500 rounded-full progress-shimmer"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      {/* Question Card */}
      <Card className="glass-card border-purple-200 shadow-2xl">
        <CardHeader className="text-center space-y-6 pb-8">
          <div className="flex justify-center">
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-purple-400 to-pink-400 flex items-center justify-center shadow-lg star-float">
              <Heart className="w-9 h-9 text-white star-twinkle" />
            </div>
          </div>
          <CardTitle className="text-2xl leading-relaxed text-gray-800 font-bold">
            {currentQuestion.question_text}
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4 px-8 pb-8">
          {currentQuestion.choices.map((choice, index) => (
            <button
              key={choice.id}
              onClick={() => handleAnswer(choice.id)}
              className={`choice-btn w-full p-5 rounded-2xl text-left border-2 ${
                answers[currentQuestion.id] === choice.id
                  ? 'choice-selected'
                  : 'bg-white hover:bg-purple-50 border-purple-200 hover:border-purple-400 text-gray-700 hover:shadow-lg'
              }`}
            >
              <div className="flex items-center gap-4">
                <div className={`w-10 h-10 rounded-full flex items-center justify-center font-bold text-lg ${
                  answers[currentQuestion.id] === choice.id
                    ? 'bg-white/30 text-white'
                    : 'bg-purple-100 text-purple-600'
                }`}>
                  {currentQuestion.question_type === 'true_false' ? '' : String.fromCharCode(65 + index)}
                </div>
                <span className="font-medium text-base">{choice.choice_text}</span>
              </div>
            </button>
          ))}

          <Button
            onClick={handleNext}
            disabled={!isAnswered}
            className="btn-oshinoko w-full h-16 mt-8 text-lg font-bold disabled:opacity-50 disabled:cursor-not-allowed text-white"
          >
            <span className="relative z-10">
              {currentQuestionIndex < quiz.questions.length - 1 ? '次へ' : '結果を見る'}
            </span>
          </Button>
        </CardContent>
      </Card>
    </div>
  )
}

function RankingPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [quiz, setQuiz] = useState(null)
  const [rankings, setRankings] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // クイズ情報を取得
    fetch(`${API_BASE}/quizzes/${id}`)
      .then(r => r.json())
      .then(data => setQuiz(data))

    // ランキングデータを取得（バックエンドAPIから）
    fetch(`${API_BASE}/quizzes/${id}/rankings`)
      .then(r => r.json())
      .then(data => {
        setRankings(data.rankings)
        setLoading(false)
      })
      .catch(err => {
        console.error('Failed to fetch rankings:', err)
        setLoading(false)
      })
  }, [id])

  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-purple-400 border-t-pink-400"></div>
      </div>
    )
  }

  const getRankMedal = (rank) => {
    if (rank === 1) return { emoji: '🥇', color: 'from-yellow-400 to-yellow-500' }
    if (rank === 2) return { emoji: '🥈', color: 'from-gray-300 to-gray-400' }
    if (rank === 3) return { emoji: '🥉', color: 'from-orange-400 to-orange-500' }
    return { emoji: `${rank}位`, color: 'from-purple-400 to-pink-400' }
  }

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Header */}
      <div className="text-center space-y-4">
        <div className="flex justify-center">
          <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-yellow-400 to-orange-400 flex items-center justify-center shadow-xl">
            <Trophy className="w-12 h-12 text-white" />
          </div>
        </div>
        <h1 className="text-4xl font-black text-oshinoko">ランキング</h1>
        {quiz && (
          <p className="text-purple-200 text-lg font-medium">{quiz.title}</p>
        )}
      </div>

      {/* Ranking List */}
      <Card className="glass-card border-purple-200 shadow-2xl">
        <CardHeader>
          <CardTitle className="text-2xl font-black text-oshinoko">
            トップ10
          </CardTitle>
          <CardDescription>上位プレイヤーの記録</CardDescription>
        </CardHeader>
        <CardContent className="space-y-3">
          {rankings.map((entry) => {
            const medal = getRankMedal(entry.rank)
            return (
              <div
                key={entry.rank}
                className="glass-card p-4 rounded-2xl border-2 border-purple-200 hover:shadow-lg transition-shadow"
              >
                <div className="flex items-center gap-4">
                  {/* 順位 */}
                  <div className={`w-16 h-16 rounded-xl bg-gradient-to-br ${medal.color} flex items-center justify-center shadow-lg flex-shrink-0`}>
                    <span className="text-2xl font-black text-white">{medal.emoji}</span>
                  </div>

                  {/* プレイヤー情報 */}
                  <div className="flex-1 min-w-0">
                    <div className="font-bold text-lg text-gray-800 truncate">
                      {entry.player_name}
                    </div>
                    <div className="flex items-center gap-4 text-sm text-gray-600 mt-1">
                      <span className="font-bold text-purple-600">
                        {entry.score}問正解
                      </span>
                      <span>{entry.percentage}%</span>
                      <span className="flex items-center gap-1">
                        <Clock className="w-3 h-3" />
                        {entry.time_taken}秒
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            )
          })}
        </CardContent>
        <CardFooter className="flex justify-center gap-4 pt-6">
          <Button
            onClick={() => navigate(`/quiz/${id}`)}
            variant="outline"
            className="border-2 border-purple-300 text-purple-600 hover:bg-purple-50 font-bold"
          >
            クイズ詳細へ
          </Button>
          <Button
            onClick={() => navigate(`/quiz/${id}/play`)}
            className="btn-oshinoko text-white font-bold"
          >
            <span className="relative z-10">挑戦する</span>
          </Button>
        </CardFooter>
      </Card>
    </div>
  )
}

function QuizResultPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const location = useLocation()
  const result = location.state?.result
  const [quiz, setQuiz] = useState(null)
  const [myRank, setMyRank] = useState(null)

  useEffect(() => {
    fetch(`${API_BASE}/quizzes/${id}?include_questions=true`)
      .then(r => r.json())
      .then(data => setQuiz(data))

    // ランキングを取得して自分の順位を調べる
    if (result?.id) {
      fetch(`${API_BASE}/quizzes/${id}/rankings`)
        .then(r => r.json())
        .then(data => {
          const myAttempt = data.rankings.find(r => r.attempt_id === result.id)
          if (myAttempt) {
            setMyRank(myAttempt.rank)
          }
        })
        .catch(err => console.error('Failed to fetch rankings:', err))
    }
  }, [id, result])

  if (!result || !quiz) {
    return (
      <div className="text-center py-12">
        <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-purple-200 border-t-purple-500"></div>
      </div>
    )
  }

  // バックエンドから返されたanswersを使用（result.answersに正解情報が含まれている）
  const answerMap = {}
  if (result.answers) {
    result.answers.forEach(ans => {
      answerMap[ans.question_id] = ans
    })
  }

  const getRankColor = (rank) => {
    const colors = {
      'S': 'from-yellow-400 to-orange-400',
      'A': 'from-blue-400 to-purple-400',
      'B': 'from-green-400 to-teal-400',
      'C': 'from-gray-400 to-gray-500',
      'D': 'from-gray-500 to-gray-600'
    }
    return colors[rank] || colors['C']
  }

  const getRankMessage = (rank) => {
    const messages = {
      'S': '完璧です！真の推しマスター！',
      'A': '素晴らしい！推し愛が伝わります',
      'B': 'よくできました！',
      'C': 'もう少し頑張りましょう',
      'D': '推し活を深めましょう'
    }
    return messages[rank] || messages['C']
  }

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Result Summary */}
      <Card className="glass-card border-purple-200 shadow-2xl text-center">
        <CardHeader className="space-y-8 pb-10">
          <div className="flex justify-center">
            <div className={`rank-badge w-36 h-36 rounded-full bg-gradient-to-br ${getRankColor(result.rank)} flex items-center justify-center shadow-2xl`}>
              <span className="text-7xl font-black text-white">{result.rank}</span>
            </div>
          </div>
          <div>
            <h2 className="text-4xl font-black text-oshinoko mb-3">
              {getRankMessage(result.rank)}
            </h2>
            <p className="text-gray-600 text-lg font-medium">おめでとうございます！</p>
          </div>

          {/* ランキング表示 - 評価の下に目立つように配置 */}
          {myRank && (
            <div className="p-8 bg-gradient-to-br from-yellow-50 to-yellow-100 rounded-3xl border-4 border-yellow-300 shadow-2xl">
              <div className="flex items-center justify-center gap-4">
                <Trophy className="w-10 h-10 text-yellow-600" />
                <div className="text-center">
                  <div className="text-6xl font-black text-yellow-600 mb-1">{myRank}</div>
                  <div className="text-lg text-gray-700 font-bold">位</div>
                </div>
                <Trophy className="w-10 h-10 text-yellow-600" />
              </div>
              <div className="text-center mt-3 text-sm text-gray-600 font-medium">
                全プレイヤー中の順位
              </div>
            </div>
          )}
        </CardHeader>
        <CardContent className="space-y-8 px-8 pb-10">
          <div className="grid grid-cols-2 gap-6">
            <div className="p-8 bg-gradient-to-br from-purple-50 to-purple-100 rounded-3xl border-2 border-purple-200 shadow-lg">
              <div className="text-5xl font-black text-purple-600 mb-3">
                {result.score}/{result.total_questions}
              </div>
              <div className="text-sm text-gray-600 font-bold">正解数</div>
            </div>
            <div className="p-8 bg-gradient-to-br from-pink-50 to-pink-100 rounded-3xl border-2 border-pink-200 shadow-lg">
              <div className="text-5xl font-black text-pink-600 mb-3">
                {result.percentage}%
              </div>
              <div className="text-sm text-gray-600 font-bold">正答率</div>
            </div>
          </div>

          <div className="grid grid-cols-1 gap-6">
            <div className="p-8 bg-gradient-to-br from-blue-50 to-blue-100 rounded-3xl border-2 border-blue-200 shadow-lg">
              <div className="flex items-center justify-center gap-3">
                <Clock className="w-6 h-6 text-blue-600" />
                <span className="text-3xl font-black text-blue-600">{result.time_taken}</span>
                <span className="text-gray-600 font-bold text-lg">秒</span>
              </div>
            </div>
          </div>

          <div className="flex flex-col gap-4 pt-6">
            <Button
              onClick={() => navigate(`/quiz/${id}/ranking`)}
              className="w-full h-16 bg-gradient-to-r from-yellow-400 to-orange-400 hover:from-yellow-500 hover:to-orange-500 text-white font-black text-lg shadow-xl"
            >
              <Trophy className="w-6 h-6 mr-2" />
              ランキングを見る
            </Button>
            <div className="flex gap-4">
              <Button
                onClick={() => navigate('/')}
                variant="outline"
                className="flex-1 h-14 border-2 border-purple-300 text-purple-600 hover:bg-purple-50 font-bold text-base"
              >
                ホームに戻る
              </Button>
              <Button
                onClick={() => navigate(`/quiz/${id}/play`)}
                className="btn-oshinoko flex-1 h-14 text-white font-bold text-base"
              >
                <span className="relative z-10">もう一度挑戦</span>
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Answer Details */}
      <div className="space-y-6">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
            <Target className="w-7 h-7 text-white" />
          </div>
          <h3 className="text-3xl font-black text-white">解答詳細</h3>
        </div>
        {quiz.questions.map((question, index) => {
          const answerInfo = answerMap[question.id]
          const isCorrect = answerInfo?.is_correct || false

          return (
            <Card key={question.id} className="glass-card border-purple-200 shadow-lg hover:shadow-xl transition-shadow">
              <CardHeader>
                <div className="flex items-start gap-4">
                  <div className={`w-12 h-12 rounded-full flex items-center justify-center font-black text-white text-xl shadow-lg ${
                    isCorrect ? 'bg-gradient-to-br from-green-400 to-green-500' : 'bg-gradient-to-br from-red-400 to-red-500'
                  }`}>
                    {isCorrect ? '✓' : '✗'}
                  </div>
                  <div className="flex-1">
                    <CardTitle className="text-xl mb-3 font-bold text-gray-800">
                      問{index + 1}: {question.question_text}
                    </CardTitle>
                    <div className="space-y-3">
                      <div className="flex items-start gap-2">
                        <span className="text-sm font-bold text-gray-600 whitespace-nowrap">あなたの回答:</span>
                        <span className={`font-bold ${isCorrect ? 'text-green-600' : 'text-red-600'}`}>
                          {answerInfo?.selected_choice_text || '未回答'}
                        </span>
                      </div>
                      {!isCorrect && (
                        <div className="flex items-start gap-2">
                          <span className="text-sm font-bold text-gray-600 whitespace-nowrap">正解:</span>
                          <span className="font-bold text-green-600">{answerInfo?.correct_choice_text}</span>
                        </div>
                      )}
                      {question.explanation && (
                        <div className="mt-4 p-5 bg-gradient-to-br from-purple-50 to-pink-50 rounded-2xl border-2 border-purple-200">
                          <p className="text-sm text-gray-700 leading-relaxed">{question.explanation}</p>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </CardHeader>
            </Card>
          )
        })}
      </div>
    </div>
  )
}

function CreateQuizPage() {
  const navigate = useNavigate()
  const [tags, setTags] = useState([])
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    oshi_tag_id: '',
    difficulty: 'beginner',
    questions: [
      {
        question_text: '',
        question_type: 'multiple_choice',
        choices: [
          { choice_text: '', is_correct: false },
          { choice_text: '', is_correct: false },
          { choice_text: '', is_correct: false },
          { choice_text: '', is_correct: false }
        ]
      }
    ]
  })

  useEffect(() => {
    fetch(`${API_BASE}/tags`)
      .then(r => r.json())
      .then(data => setTags(data))
  }, [])

  const handleSubmit = (e) => {
    e.preventDefault()
    
    fetch(`${API_BASE}/quizzes`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ...formData,
        creator_id: 1
      })
    })
      .then(r => r.json())
      .then(data => {
        navigate(`/quiz/${data.id}`)
      })
  }

  const addQuestion = () => {
    setFormData({
      ...formData,
      questions: [
        ...formData.questions,
        {
          question_text: '',
          question_type: 'multiple_choice',
          choices: [
            { choice_text: '', is_correct: false },
            { choice_text: '', is_correct: false },
            { choice_text: '', is_correct: false },
            { choice_text: '', is_correct: false }
          ]
        }
      ]
    })
  }

  const updateQuestion = (index, field, value) => {
    const newQuestions = [...formData.questions]
    newQuestions[index][field] = value
    setFormData({ ...formData, questions: newQuestions })
  }

  const updateChoice = (qIndex, cIndex, field, value) => {
    const newQuestions = [...formData.questions]
    newQuestions[qIndex].choices[cIndex][field] = value
    setFormData({ ...formData, questions: newQuestions })
  }

  return (
    <div className="max-w-4xl mx-auto">
      <Card className="border-purple-100 bg-white/80 backdrop-blur-sm shadow-xl">
        <CardHeader>
          <CardTitle className="text-3xl bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
            新しいクイズを作成
          </CardTitle>
          <CardDescription>推しに関するマニアックなクイズを作成しましょう</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">タイトル</label>
              <input
                type="text"
                value={formData.title}
                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                className="w-full px-4 py-3 border border-purple-200 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">説明</label>
              <textarea
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                className="w-full px-4 py-3 border border-purple-200 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                rows="3"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">推しタグ</label>
                <select
                  value={formData.oshi_tag_id}
                  onChange={(e) => setFormData({ ...formData, oshi_tag_id: parseInt(e.target.value) })}
                  className="w-full px-4 py-3 border border-purple-200 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  required
                >
                  <option value="">選択してください</option>
                  {tags.map(tag => (
                    <option key={tag.id} value={tag.id}>{tag.name}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">難易度</label>
                <select
                  value={formData.difficulty}
                  onChange={(e) => setFormData({ ...formData, difficulty: e.target.value })}
                  className="w-full px-4 py-3 border border-purple-200 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                >
                  <option value="beginner">初級</option>
                  <option value="intermediate">中級</option>
                  <option value="advanced">上級</option>
                  <option value="mania">マニア級</option>
                </select>
              </div>
            </div>

            <div className="space-y-6 pt-4">
              <h3 className="text-xl font-bold text-gray-800">問題</h3>
              {formData.questions.map((question, qIndex) => (
                <Card key={qIndex} className="border-purple-200 bg-purple-50/50">
                  <CardHeader>
                    <CardTitle className="text-lg">問題 {qIndex + 1}</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">問題文</label>
                      <input
                        type="text"
                        value={question.question_text}
                        onChange={(e) => updateQuestion(qIndex, 'question_text', e.target.value)}
                        className="w-full px-4 py-3 border border-purple-200 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white"
                        required
                      />
                    </div>

                    <div className="space-y-3">
                      <label className="block text-sm font-medium text-gray-700">選択肢</label>
                      {question.choices.map((choice, cIndex) => (
                        <div key={cIndex} className="flex gap-3">
                          <input
                            type="text"
                            value={choice.choice_text}
                            onChange={(e) => updateChoice(qIndex, cIndex, 'choice_text', e.target.value)}
                            placeholder={`選択肢 ${cIndex + 1}`}
                            className="flex-1 px-4 py-3 border border-purple-200 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white"
                            required
                          />
                          <label className="flex items-center gap-2 px-4 py-3 bg-white border border-purple-200 rounded-xl cursor-pointer hover:bg-purple-50">
                            <input
                              type="checkbox"
                              checked={choice.is_correct}
                              onChange={(e) => updateChoice(qIndex, cIndex, 'is_correct', e.target.checked)}
                              className="w-5 h-5 text-purple-600 rounded focus:ring-purple-500"
                            />
                            <span className="text-sm font-medium text-gray-700">正解</span>
                          </label>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              ))}

              <Button
                type="button"
                onClick={addQuestion}
                variant="outline"
                className="w-full border-purple-300 text-purple-600 hover:bg-purple-50"
              >
                <Plus className="w-4 h-4 mr-2" />
                問題を追加
              </Button>
            </div>

            <Button
              type="submit"
              className="w-full h-14 text-lg bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white shadow-lg"
            >
              <Sparkles className="w-5 h-5 mr-2" />
              クイズを作成
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}

export default App

