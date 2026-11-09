MedAgentX: Git Branching and Merging

Separate guide: create a feature branch, commit, push, and merge
Assumption: the repository is already connected to a remote named origin and the default branch is main. If your default branch has another name, substitute it.

1. Prepare before branching
   git status
   git branch
   git switch main
   git pull origin main
   If you have uncommitted changes, commit or stash them before switching branches. The active branch has an asterisk in git branch output.

2. Create a feature branch
   git switch -c feature/add-specialist-agents
   git branch
   Use a descriptive name, for example feature/neurology-agent. Check that the feature branch is active before editing.

3. Code and test in that branch
   git status
   git diff
   python -m app.main
   Make changes, run tests, and review the diff. Never commit .env, API keys, venv/.venv, or cache files.

4. Stage and commit
   git add app/main.py app/prompts.py app/specialists/
   git status
   git commit -m "Add remaining specialist agents"
   Adjust git add paths to match the files actually changed. Check git status before committing.

5. Push the branch to GitHub
   git push -u origin feature/add-specialist-agents
   The -u option is normally needed on the first push of a new branch. Later pushes from that branch usually use git push.

6. Recommended merge: GitHub Pull Request
7. Open the repository on GitHub.
8. Create a Pull Request: base = main, compare = feature/add-specialist-agents.
9. Review the files changed and test results; request teammate review if appropriate.
10. Merge the Pull Request only after checks pass.
11. Delete the remote feature branch on GitHub if it is no longer needed.

12. Alternative: merge locally
    git switch main
    git pull origin main
    git merge --no-ff feature/add-specialist-agents
    python -m app.main
    git push origin main
    Use this method only if your team permits direct merges to main. Do not push main until the merge and tests succeed.

13. Resolve merge conflicts
    git status

# Open each conflicted file and resolve:

# <<<<<<<, =======, >>>>>>>

git add <resolved-file>
git commit
Preserve the intended changes from both branches, remove all conflict markers, and rerun tests. To cancel an in-progress merge, use git merge --abort.

9. Clean up after merging
   git switch main
   git pull origin main
   git branch -d feature/add-specialist-agents

# Optional: delete remote branch if it still exists

git push origin --delete feature/add-specialist-agents

Common mistakes
• src refspec main does not match any: make at least one commit before pushing and verify the branch name.
• Accidentally working on main: check git branch before coding.
• Accidentally committed .env: remove it from tracking and rotate the exposed API key; .gitignore does not erase history.
• Merge conflict: resolve carefully, run tests, then finish the merge.
Quick workflow
git switch main
git pull origin main
git switch -c feature/my-change

# edit and test

git add <changed-files>
git commit -m "Describe the change"
git push -u origin feature/my-change

# create and merge Pull Request on GitHub

git switch main
git pull origin main
git branch -d feature/my-change
