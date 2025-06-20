# soft-engg-project-may-2025-se-May-20

## How to Run the Project (Frontend & Backend Together)

A script `run_all.sh` is provided to automate setup and run both backend and frontend servers.

### Steps:
1. Open a terminal in the project root directory.
2. Make the script executable (first time only):
   ```bash
   chmod +x run_all.sh
   ```
3. Run the script:
   ```bash
   ./run_all.sh
   ```

- This will set up Python and Node.js dependencies, start the backend (Flask) and frontend (Vite) servers.
- The backend will be available at `http://127.0.0.1:5000` and the frontend at `http://localhost:5173` by default.
- When you stop the frontend server, the backend server will also stop automatically.

---

## Developer Notes : 
1. Always make sure working branch is upto date with `main` branch
  -  `git fetch --all` # it will fetch latest code from github
  -  `git pull origin main` # it will merge main branch code to the working branch.
  -  (if there is conflict between merge, manually resolve it)
2. Make sure files that not to be pushed to github added in .gitignore
3. Update README.md file with instructions to run the project locally for any of the members. (both frontend and backend)
