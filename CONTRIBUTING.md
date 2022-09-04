# Contributing to SP2137 bot
This repository uses Feature Branch Workflow for contributions. Presented below is the step-by-step guide to working on an issue.
1. Pick an open issue from "Issues" tab that you would like to work on. Make sure the issue isn't already assigned to anyone else.
2. Assign the issue to yourself.
3. Go to the local clone of the repository on your disk and pull the latest version of code: 
```bash
git checkout master
git fetch origin
git reset --hard origin/master
```
4. Create your working branch. The name of this branch should start with the number of the issue you're working on and contain a short description of the new feature e.g. "1-contribution-guideline":
```bash
git checkout -b <branch-name>
```
5. Update the label in the issue to "state: in progress"
6. Implement and test your changes then add and commit and push them:
```bash
git status
git add <some-file>
git commit
git push -u origin <branch-name>
```
7. After pushing all of your changes go to "Pull requests" tab on github and create a new pull request. As a "base:" branch select "master" and as a "compare:" branch select your <branch-name>. Click create pull request. Put the name of the issue as the pull request title. In the comment describe your changes, at the end of the comment after one empty line include the link to the issue. Put the same title and description as a merge title/description. Go to the issue you're working on and update the status: remove "state: in progress" label and add the "state: review".
8. Wait for the pull request to be reviewed. Make improvements to the code if they are necessary and repeats steps 5-6.
9. Finally the pull request will be approved and merged into the master branch. After this is done close the issue and remove the "state: review" label from it.
