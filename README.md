Create a new repository: git init
Clone a repository: git clone [respository URL]
Add a remote repository: git remote add [name] [repository URL]
Fetch changes from a remote repository: git fetchPull
changes from a remote repository: git pull Push
changes to a remote repository: git push Use
branching and merging
Branching and merging are powerful features of Git that allow you to work on multiple
versions of your code simultaneously, without interfering with each other’s work. By using
branching and merging effectively, your team can work on different features or bug fixes in
parallel, without causing conflicts.
Create a new branch: git branch [name]Switch
to a branch: git checkout [name]Merge a
branch: git merge [name] Resolve merge
conflicts: git mergetool Delete a branch: git
branch -d [name]

33

Use Pull requests
Pull requests are a great way to review and merge changes from differentteam members
before they are merged into the main codebase. By using pull requests, you can ensure that
your code is reviewed and tested before it is merged into the main branch, which can help
prevent bugs and other issues.
Create a new pull request: git request-pull [branch] [repository URL]
Review and merge a pull request: git pull-request
Close a pull request: git request-pull -C [branch] [repository URL]

Use IssueTracking
Issue tracking is a great way to keep track of bugs, feature requests, and other issues that
need to be addressed in your code. By using an issue tracking system like GitHub Issues, you can
assign tasks to team members, track progress, and ensure that all issues are addressed in a timely
manner.
Create a new issue: git commit -m “[issue number] [commit message]”
Assign an issue to a team member: git assign [username]
Clone an issue: git clone [issue number] Reopen an
issue: git reopen [issue number]Communicate
Effectively
Effective communication is key to collaboration, especially in a remote
team setting. Use tools like Slack or Microsoft Teams to stay in touch with yourteam members,
and use video calls or screen sharing to discuss code changes or work on problems together.
Start a video call: git video-call [username]
Share yourscreen: gitscreen-share
Send a message: git message [username] [message]
Use Git hooks
Git hooks are scripts that Git runs automatically at certain points in the Gitworkflow. You
can use Git hooks to automate repetitive tasks, enforce coding standards, or perform other tasks
that are important to your team’s workflow.

34
Install a git hook: git init [hook name]
Write a git hook script: nano.git/hooks/[hook name]
Make the Git hook script executable: chmod +x .git/hooks/[hook name]
Use Gitsubmodules
Git submodules are repositories that are embedded inside other repositories. You can use
Git submodules to manage dependencies, or to includeshared code in multiple projects.
Add a Git submodule: git submodule add [repository URL]
Update a Gitsubmodule: gitsubmodule update
Remove a Gitsubmodule: gitsubmodule deinit [submodule path]
Use Git aliases
Git aliases are shortcuts for commonly used Git commands. You can useGit aliases to save
time and improve your productivity when working with Git.
Set up a Git alias: git config –global alias.[alias name] ‘[Git command]’
Use a Git alias: git [alias name]