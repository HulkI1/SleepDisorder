Vercel deploy notes

1. Push this `archive_removed/frontend` directory to a GitHub repo (or the monorepo root) and connect it in the Vercel dashboard.
2. In Vercel project settings set:
   - Framework Preset: `Create React App` (or leave auto-detected)
   - Build Command: `npm run build`
   - Output Directory: `build`
3. Add Environment Variables (if your frontend needs to call the API):
   - `REACT_APP_API_URL` -> `https://api.yourdomain.com` (or the Fly app URL)
4. Deploy; Vercel will provide `https://<project>.vercel.app`. Add your custom domain in Vercel and follow Vercel's DNS instructions to point it via Cloudflare.
