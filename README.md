# link-shortener (in development)
A FastAPI link-shortener **learning project** with persistent storage.

---

# project's overview
The project is based on the following idea:
- the site receives an URL (in /link-shortener/url/{URL} f.e.) and creates a 5 - 7 random string to attach to the given URL.
- link and string are stored in a DB
- to access the shortened link, you just access "/link-shortener/{string}", then the API redirect's you to the corresponding URL for that string (if it exists) 
- the admin can edit those URLs in the db by accessing "/link-shortener/admin/{DELETE,ADD,EDIT}"
- I intend on adding cybersec features such as:
    > Integrated Threat Intelligence (check if the URL that will be shortened is safe using the python's **requests** library and **VirusTotal** API)
    > Build a "Un-shortener" (Basically check the shortened URL without the need to access it)
    > Layer 7 DoS Mitigation (Just prevent a single IP to make lots of requests to the API)


#### Development Roadmap
##### Just show how I intend on doing this project (if you're interested on knowing)

- **Phase 1 & 2: Core API** - Built a functional URL shortener MVP using FastAPI and SQLite.
- **Phase 3: DoS Mitigation** - Implement IP-based rate limiting to prevent API abuse and resource exhaustion.
- **Phase 4: Threat Intelligence** - Integrate the VirusTotal API to scan and block known malicious URLs before shortening.
- **Phase 5: Security Auditing** - Add structured logging to track allowed and blocked actions for SOC visibility.
- **Phase 6: Safe Preview** - Create an "un-shorten" endpoint to allow people to inspect links safely without triggering redirects.


#### Final Thoughts

This is a relatively simple project, but it serves its purpose well. It is still in an early stage of development, so you may come across test files, experimental code, or features that are still being refined. I have chosen to keep some of these elements visible as they reflect my learning process and the project's evolution over time.

If you have suggestions, feedback, or would like to contribute, feel free to reach out to me through my LinkedIn profile.

---

### Configuring .env
```
#~/link-shortener/.env

ENV_NAME="[Choose a name]"
BASE_URL="[URL to the link shortener]"
DB_URL="[you db url]"
```
you can leave those empty or simply not have anything on .env, but make shure your .env file exists and it's at /link-shortener/.env