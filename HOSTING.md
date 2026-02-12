Option A — Deploy backend to Fly.io and frontend to Vercel/Cloudflare Pages, then point a free Freenom domain through Cloudflare DNS

Overview
- Backend: `flask_app.py` (Gunicorn) -> container build via `Dockerfile` -> deploy to Fly.io (free tier).
- Frontend: `frontend/` (React) -> deploy to Vercel or Cloudflare Pages (static build).
- Domain: register free domain at Freenom, add the domain to Cloudflare, then add DNS records that point to Fly/Vercel and enable HTTPS via Cloudflare (or let host manage certificates).

Prerequisites
- Create accounts: Fly (fly.io), Vercel (or Cloudflare Pages), Cloudflare, Freenom
- Install CLIs: `flyctl` (for Fly), `vercel` (optional), `git`, `docker` (optional but useful)

Backend (Fly.io)
1. Install and login: `curl -L https://fly.io/install.sh | sh` then `flyctl auth login`
2. From the repo root, test locally (optional):
   - Build and run Docker locally: `docker build -t sleepdisorder .` then `docker run -p 8080:8080 sleepdisorder`
3. Create and deploy to Fly (recommended flow):
   - `flyctl launch` — follow prompts and choose generated app name (or supply `--name sleepdisorder`) and select a region. When asked to deploy now, accept.
   - If you prefer to control the image: `flyctl deploy --remote-only` or `flyctl deploy` (uses `Dockerfile`).
4. After deploy, your app will be reachable at `https://<appname>.fly.dev`.

Frontend (Vercel or Cloudflare Pages)
- Vercel (easy):
  1. Push `frontend/` to GitHub and import the repo in Vercel dashboard.
  2. Set build command: `npm run build` and output dir: `build`.
  3. Deploy — Vercel provides `https://<project>.vercel.app`.
- Cloudflare Pages (static):
  1. Connect the GitHub repo to Cloudflare Pages and set build command `npm run build` and output folder `build`.

Domain registration (Freenom) and Cloudflare DNS
1. Register free domain at Freenom (choose .tk/.ml/.ga/.cf/.gq) and claim it.
2. In Cloudflare, add site -> enter Freenom domain -> choose free plan -> Cloudflare will provide nameservers.
3. In Freenom, edit the domain's Nameservers and set them to Cloudflare's nameservers (from previous step). Wait for propagation.
4. In Cloudflare DNS:
   - To point root and `www` to Fly backend: create `CNAME www` -> target `<appname>.fly.dev`. For root (`@`) use an ALIAS/ANAME if Cloudflare supports it, otherwise add an `A` record pointing to Fly's assigned IP (Fly typically uses `CNAME`/managed DNS; if Fly gives an IP, add that `A` record). Alternatively, point root to Vercel if frontend is main site.
   - To point `www` or a subdomain to Vercel: create `CNAME www` -> `cname.vercel-dns.com` (Vercel gives exact target when adding a custom domain).
5. In Cloudflare SSL/TLS settings: enable `Full (strict)` if the hosts have valid certs, enable `Always Use HTTPS` and `Automatic HTTPS Rewrites`.

Notes and recommended mapping
- Typical mapping: Use Fly for API/backend on `api.yourdomain.com` and Vercel/Pages for frontend on `yourdomain.com` and `www.yourdomain.com`. This keeps static content fast and backend separated.
- Example DNS entries (recommended):
  - `A @` -> Cloudflare Pages/Vercel recommends using their verified configuration (follow the provider's instructions).
  - `CNAME www` -> `cname.vercel-dns.com` (for Vercel) OR `CNAME www` -> `<appname>.fly.dev` (if hosting frontend on backend host).
  - `CNAME api` -> `<appname>.fly.dev` (for backend API)

Post-deploy verification
1. Visit the frontend URL (Vercel/Pages) and verify it loads and can call backend API at `https://api.yourdomain.com` (update frontend config to use that URL).
2. Check HTTPS lock icon and test pages.
3. If CORS issues appear, add correct CORS headers in `flask_app.py` or use a proxy configuration on the frontend.

Troubleshooting
- If Fly returns a dynamic IP that changes, prefer CNAME to `*.fly.dev` or use Fly's custom domain docs to add the domain via `flyctl certs create` and DNS instructions.
- If Cloudflare shows `DNS only` vs `Proxied`, set to `Proxied` (orange cloud) to use Cloudflare SSL and CDN — but if the origin needs client IP or special headers, use `DNS only` and enable HTTPS on origin.

Quick commands summary
```
# Backend (Fly)
flyctl auth login
flyctl launch --name sleepdisorder
flyctl deploy

# Frontend (local test)
cd frontend
npm install
npm run build

# Push frontend to GitHub and connect to Vercel or Cloudflare Pages
```

If you want, I can:
- (A) generate `fly.toml` for you and commit it (you'll still run `flyctl launch` to bind the domain),
- (B) prepare a `frontend/.vercelignore` and sample Vercel project settings, or
- (C) walk through an interactive `flyctl launch` from your terminal (you'll need to authorize). Tell me which next step you prefer.
