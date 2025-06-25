# How to use Github

1. Create a repository in github.com, give access to whoever needed
2. Copy the address of the repository
3. From your CLI, git clone (address), it copies the repository as a folder to your computer
4. Git yourself to your dev branch (git branch dev, git checkout dev)
5. copy this structure to the new repository folder
6. Start coding
7. When finished: git add .
8. git commit -m "my new added stuff"
9. git push origin dev
10. Go to the github and do the pull request (pull dev to main)
11. When others do changes to the code, decide who does pull request checks
12. When updated code is in main, go to the main branch locally: git checkout main
13. Pull the updated code to your computer: git pull
14. Go to your working branch: Git checkout dev
15. Pull the updated code from main branch to your working branch: git merge main
16. Start coding again