Cloudflare Pages deploy notes

1. Push this frontend code to GitHub and connect the repository in Cloudflare Pages.
2. Set the Build command to `npm run build` and the Build output directory to `build`.
3. In Cloudflare Pages, after deploy, add your custom domain and follow the instructions; Cloudflare will provide verification records or nameserver guidance.
4. For API calls, set an environment variable `REACT_APP_API_URL` in the Pages project to `https://api.yourdomain.com`.
