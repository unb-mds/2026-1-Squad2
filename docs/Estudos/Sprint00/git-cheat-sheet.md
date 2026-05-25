# Git Cheat Sheet

Git is the free and open source distributed version control system that's responsible for everything GitHub related that happens locally on your computer. This cheat sheet features the most important and commonly used Git commands for easy reference.

---

## Installation & GUIs

With platform specific installers for Git, GitHub also provides the ease of staying up-to-date with the latest releases of the command line tool while providing a graphical user interface for day-to-day interaction, review, and repository synchronization.

- **GitHub for Windows** — <https://windows.github.com>
- **GitHub for Mac** — <https://mac.github.com>

For Linux and Solaris platforms, the latest release is available on the official Git web site.

- **Git for All Platforms** — <http://git-scm.com>

---

## Setup

Configuring user information used across all local repositories.

```bash
git config --global user.name "[firstname lastname]"
```
Set a name that is identifiable for credit when reviewing version history.

```bash
git config --global user.email "[valid-email]"
```
Set an email address that will be associated with each history marker.

```bash
git config --global color.ui auto
```
Set automatic command line coloring for Git for easy reviewing.

---

## Setup & Init

Configuring user information, initializing and cloning repositories.

```bash
git init
```
Initialize an existing directory as a Git repository.

```bash
git clone [url]
```
Retrieve an entire repository from a hosted location via URL.

---

## Stage & Snapshot

Working with snapshots and the Git staging area.

```bash
git status
```
Show modified files in working directory, staged for your next commit.

```bash
git add [file]
```
Add a file as it looks now to your next commit (stage).

```bash
git reset [file]
```
Unstage a file while retaining the changes in working directory.

```bash
git diff
```
Diff of what is changed but not staged.

```bash
git diff --staged
```
Diff of what is staged but not yet committed.

```bash
git commit -m "[descriptive message]"
```
Commit your staged content as a new commit snapshot.

---

## Branch & Merge

Isolating work in branches, changing context, and integrating changes.

```bash
git branch
```
List your branches. A `*` will appear next to the currently active branch.

```bash
git branch [branch-name]
```
Create a new branch at the current commit.

```bash
git checkout
```
Switch to another branch and check it out into your working directory.

```bash
git merge [branch]
```
Merge the specified branch's history into the current one.

```bash
git log
```
Show all commits in the current branch's history.

---

## Share & Update

Retrieving updates from another repository and updating local repos.

```bash
git remote add [alias] [url]
```
Add a git URL as an alias.

```bash
git fetch [alias]
```
Fetch down all the branches from that Git remote.

```bash
git merge [alias]/[branch]
```
Merge a remote branch into your current branch to bring it up to date.

```bash
git push [alias] [branch]
```
Transmit local branch commits to the remote repository branch.

```bash
git pull
```
Fetch and merge any commits from the tracking remote branch.

---

## Tracking Path Changes

Versioning file removes and path changes.

```bash
git rm [file]
```
Delete the file from project and stage the removal for commit.

```bash
git mv [existing-path] [new-path]
```
Change an existing file path and stage the move.

```bash
git log --stat -M
```
Show all commit logs with indication of any paths that moved.

---

## Temporary Commits

Temporarily store modified, tracked files in order to change branches.

```bash
git stash
```
Save modified and staged changes.

```bash
git stash list
```
List stack-order of stashed file changes.

```bash
git stash pop
```
Write working from top of stash stack.

```bash
git stash drop
```
Discard the changes from top of stash stack.

---

## Rewrite History

Rewriting branches, updating commits and clearing history.

```bash
git rebase [branch]
```
Apply any commits of current branch ahead of specified one.

```bash
git reset --hard [commit]
```
Clear staging area, rewrite working tree from specified commit.

---

## Inspect & Compare

Examining logs, diffs and object information.

```bash
git log
```
Show the commit history for the currently active branch.

```bash
git log branchB..branchA
```
Show the commits on `branchA` that are not on `branchB`.

```bash
git log --follow [file]
```
Show the commits that changed file, even across renames.

```bash
git diff branchB...branchA
```
Show the diff of what is in `branchA` that is not in `branchB`.

```bash
git show [SHA]
```
Show any object in Git in human-readable format.

---

## Ignoring Patterns

Preventing unintentional staging or committing of files.

```bash
git config --global core.excludesfile [file]
```
System wide ignore pattern for all local repositories.

Save a file with desired patterns as `.gitignore` with either direct string matches or wildcard globs:

```
logs/
*.notes
pattern*/
```

---

*GitHub Education — <education.github.com> — <education@github.com>*

*Teach and learn better, together. GitHub is free for students and teachers. Discounts available for other educational uses.*
