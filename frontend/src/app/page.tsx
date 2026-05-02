export default function Home() {
  return (
    <main className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full p-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">UniCore</h1>
          <p className="text-gray-600 mt-2">University Portal</p>
        </div>
        
        <div className="card p-6">
          <form className="space-y-4">
            <div>
              <label className="label" htmlFor="email">
                Email
              </label>
              <input
                id="email"
                type="email"
                className="input"
                placeholder="student@university.edu"
              />
            </div>
            
            <div>
              <label className="label" htmlFor="password">
                Password
              </label>
              <input
                id="password"
                type="password"
                className="input"
                placeholder="••••••••"
              />
            </div>
            
            <button type="submit" className="btn btn-primary w-full">
              Sign In
            </button>
          </form>
        </div>
        
        <p className="text-center text-sm text-gray-500 mt-4">
          Use your institutional credentials to login
        </p>
      </div>
    </main>
  )
}