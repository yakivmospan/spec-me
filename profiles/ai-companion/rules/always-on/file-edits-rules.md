# File edits

Always-on. Change and create files with the agent's own file-editing tool — Edit or Write in Claude
Code — never through a shell command: no `sed -i`, no heredoc, no short `python` script that rewrites
a file.

Only an edit made that way shows up as a diff in the editor. A shell edit lands invisibly, so the
change cannot be reviewed, and a wrong one is found later by accident.

Content you author always goes through the editing tool. A command's own output may be redirected to
a file, and creating a directory is not a file edit.

This holds for scratch files and files in a throwaway worktree too, and even where a session's own
harness guidance asks for shell-first editing.

The shell stays right for running and reading: git, the forge's command-line tool, builds, tests, searches, and reading a
file.
