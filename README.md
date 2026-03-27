# GetQuiz

> AI-powered quiz generator — create quizzes instantly from any topic.

![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-8-646CFF?logo=vite&logoColor=white)
![React Router](https://img.shields.io/badge/React_Router-7-CA4245?logo=reactrouter&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)

---

## Overview

GetQuiz is a full-stack quiz platform where users can generate, manage, and take quizzes. The frontend is fully functional in offline/mock mode — no backend required to run locally.

---

## Project Structure

```
GetQuiz/
├── frontend/          # React + Vite SPA
│   ├── src/
│   │   ├── api/       # API client + endpoint helpers
│   │   ├── components/# Reusable UI components (Navbar, Hero, Features…)
│   │   ├── context/   # React context (AuthContext, ThemeContext)
│   │   ├── data/      # Shared mock data (mockQuizzes.js)
│   │   ├── pages/     # Route-level page components
│   │   └── styles/    # Per-feature CSS files
│   ├── public/
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
└── backend/           # (coming soon)
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| UI Framework | React 19 |
| Build Tool | Vite 8 |
| Routing | React Router 7 |
| Icons | Lucide React |
| Styling | Vanilla CSS (custom design system) |
| State | useState / useReducer / Context API |

---

## Getting Started

### Prerequisites

- **Node.js** ≥ 18 — [nodejs.org](https://nodejs.org)
- **npm** ≥ 9 (bundled with Node)

### 1. Clone the repository

```bash
git clone https://github.com/washedoutprogrammer/GetQuiz.git
cd GetQuiz
```

### 2. Install dependencies

```bash
cd frontend
npm install
```

### 3. Configure environment (optional)

The app works out-of-the-box with mock data — no backend needed. To connect a real backend, create `frontend/.env`:

```env
VITE_API_URL=http://localhost:8000
```

> If `VITE_API_URL` is not set, it defaults to `http://localhost:8000`. When the backend is unreachable, the app automatically falls back to shared mock quiz data.

### 4. Start the dev server

```bash
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

---

## Available Scripts

Run these from inside the `frontend/` directory:

| Command | Description |
|---|---|
| `npm run dev` | Start Vite dev server with HMR |
| `npm run build` | Build production bundle to `dist/` |
| `npm run preview` | Preview the production build locally |
| `npm run lint` | Run ESLint |

---

## Pages & Routes

| Route | Page | Description |
|---|---|---|
| `/` | Landing | Marketing homepage |
| `/login` | Login | User sign-in |
| `/register` | Register | User sign-up |
| `/dashboard` | Dashboard | Manage quizzes — create, view, delete |
| `/quiz/:quizId` | QuizSession | Take a quiz with countdown timer |
| `/results/:sessionId` | Results | Score summary and answer breakdown |

---

## Mock Mode (Offline Development)

When the backend API is unavailable, the app loads quiz data from `src/data/mockQuizzes.js`. This file is the single source of truth for all sample quizzes used across:

- **Dashboard** — populates the quiz cards
- **QuizSession** — loads the correct quiz by `quizId`

Three sample quizzes are included:

1. **JavaScript Fundamentals** — closures, arrays, async
2. **React Hooks Deep Dive** — useEffect, useMemo, useRef
3. **CSS Layout Mastery** — Flexbox, Grid, units

To add a new mock quiz, append an entry to the `MOCK_QUIZZES` array in `src/data/mockQuizzes.js`:

```js
{
  id: 4,                           // must be unique
  title: 'TypeScript Basics',
  description: 'Types, interfaces, and generics',
  createdAt: '2026-03-27',
  tags: ['TypeScript'],
  questions: [
    {
      id: 'ts-1', type: 'mcq',
      text: 'What keyword declares a type alias?',
      options: ['interface', 'type', 'class', 'enum'],
      correct_index: 1,            // 0-based index of correct option
    },
    {
      id: 'ts-2', type: 'tf',
      text: 'TypeScript is a superset of JavaScript.',
      correct_answer: true,        // boolean for True/False questions
    },
  ],
}
```

---

## API Integration

The frontend talks to a REST backend via `src/api/client.js`. All requests automatically attach the JWT from `localStorage` (`gq-token`).

### Endpoint modules

| File | Endpoints |
|---|---|
| `api/auth.js` | `POST /auth/login`, `POST /auth/register` |
| `api/quizzes.js` | `GET /quizzes/:id` |
| `api/sessions.js` | `POST /sessions`, `POST /sessions/:id/answers`, `POST /sessions/:id/finish` |

Every call returns `{ ok: boolean, data: any, error: string | null }` — the UI handles both success and failure states without throwing.

---

## Contributing

1. Fork the repo
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Commit with conventional commits: `git commit -m "feat: add X"`
4. Push and open a Pull Request

---

## License

MIT © [washedoutprogrammer](https://github.com/washedoutprogrammer)
