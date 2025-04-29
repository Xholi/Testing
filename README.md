# WebPulse AI – Website Generator for Offline Businesses

**WebPulse AI** is a platform that scrapes businesses without websites, auto-generates branded one-page or full websites, emails them to clients, and tracks project progression.

## 🔧 Features

- Google Maps scraper for businesses without a website
- One-page website generator with theming
- Email delivery of site demo with built-in sales pitch
- CRM dashboard to track leads, payments, approvals
- Admin authentication and role control
- API-ready backend (FastAPI)
- Frontend: Static GitHub Pages (see `/frontend`)

## 🚀 Quick Start

```bash
git clone https://github.com/Xholi/webpulse-ai.git
cd webpulse-ai
pip install -r requirements.txt
uvicorn backend.main:app --reload
