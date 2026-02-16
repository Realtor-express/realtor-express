# Realtor Express (Agent Network MVP)

Realtor Express is a **B2B platform for NYC real estate agents** that accelerates deal collaboration by enabling **one-click borough-based broadcasts** to hundreds of agents—while keeping contacts private by default.

This MVP is **Agent-first** (community + broadcast + subscription). Client Mode and intelligent client matching are planned for later versions.

---

## Core Concept (MVP)

### Agent Network
- Verified agents join a single community by borough (Manhattan, Brooklyn, Queens, Bronx, Staten Island)
- Agents can broadcast requests to a selected borough in one click
- Quick response templates replace full chat in MVP

### Privacy & Trust
- Contacts are hidden by default
- License verification is **manual** (admin approval workflow)
- Contact visibility and agent directory access are controlled by subscription tier

---

## Key Features (MVP Scope)

### Agent Onboarding
- Registration: name, email, phone
- Service areas: borough selection
- License upload (PDF/JPG/PNG)
- Status flow: **Under Review → Verified / Rejected**
- Email/push notification on approval (optional in MVP)

### Broadcast System (Core Feature)
- Create a broadcast: borough(s) + subject + message
- Send to all eligible agents in selected borough(s)
- Quick templates (e.g., “Interested”, “I have a buyer”, “Call me”)
- Basic feed of broadcasts by borough

### Subscription & Access Control
- Free tier: view broadcasts + limited responses, contacts hidden
- Pro tier: unlock **agent directory** + **contact visibility** + unlimited broadcast

### Admin Panel (Internal)
- Review applications, approve/reject licenses
- Moderate broadcasts/users (basic tools)

---

## Monetization Model (Draft)

| Plan | What you get |
|------|--------------|
| Free | View broadcasts, limited replies, contacts hidden |
| Pro  | Agent directory + contact visibility + unlimited broadcasts |

---

## Tech Stack (Proposed)

- **Mobile App:** Flutter (Dart) — iOS + Android
- **Backend API:** Python (FastAPI)
- **Database:** PostgreSQL
- **Admin Panel:** React.js (minimal for MVP)
- **Payments:** Stripe Subscriptions
- **Infrastructure:** TBD (Railway / Render / Vercel)

---

## Product Status

🚧 Active Development — MVP Planning Phase  
Target: **Agent Network Beta (Borough Broadcast + Subscription)**

---

## Team & Contacts

- Product Owner: Umarova Shahodat
- Tech Lead / Backend: Majidov Sherzod

---

## Design (Figma)

https://www.figma.com/make/jHhLojHL03rqBkp2spb5lU/Real-Estate-B2B2C-Platform
