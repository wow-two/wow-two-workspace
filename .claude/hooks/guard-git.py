#!/usr/bin/env python3
"""wow-two git guard — PreToolUse(Bash) hook.

Hard-blocks agent-run history/publish ops so the human stays the ONLY one who
commits + pushes. Agents stage (`git add` / `git restore --staged`) and hand the
commit message to the human in chat. Rationale + protocol:
conventions/development/repo/version-control/git.md.

Blocks: git push, git reset --hard/--merge/--keep, git stash drop/clear/pop.
Allows: git add, git commit, git restore --staged, git reset (plain/soft), status/diff/log.
`commit` is permitted because it rewrites nothing that cannot be amended; asking
before committing stays a CLAUDE.md rule, since a hook sees a shell string and
never whether the developer requested it. `push` is what leaves the machine.
Parses each git invocation (skips `-c key=val` / `-C dir` global opts, splits on
&& || ; | ) so `git -c ... push` can't slip through.
"""
import json
import shlex
import sys

DENY = (
    "BLOCKED — wow-two git protocol (conventions/development/repo/version-control/git.md).\n"
    "Agents never run `git {sub}` — the human is the only one who commits + pushes.\n"
    "Instead: stage with `git add` / `git restore --staged`, then print the commit\n"
    "message in chat and STOP. The human reviews, commits, and pushes."
)

GLOBAL_OPTS_WITH_VALUE = {"-c", "-C", "--git-dir", "--work-tree", "--namespace", "--exec-path", "--super-prefix"}
SEPARATORS = {"&&", "||", ";", "|", "&", "(", ")", "{", "}", "\n"}


def git_subcommands(cmd):
    """Yield (subcommand, args) for every `git ...` invocation in a shell string."""
    try:
        toks = shlex.split(cmd, posix=True)
    except ValueError:  # unbalanced quotes etc. — degrade to a permissive split
        toks = cmd.replace("&&", " ; ").replace("||", " ; ").replace("|", " ; ").split()
    out, i, expect_cmd = [], 0, True
    while i < len(toks):
        t = toks[i]
        if t in SEPARATORS:
            expect_cmd = True
            i += 1
            continue
        if expect_cmd:
            if ("=" in t) and not t.startswith("-"):  # VAR=value assignment prefix
                i += 1
                continue
            if t == "git" or t.endswith("/git"):
                j = i + 1
                while j < len(toks):  # skip git's global options to reach the subcommand
                    a = toks[j]
                    if a in GLOBAL_OPTS_WITH_VALUE:
                        j += 2
                        continue
                    if a.startswith("-"):
                        j += 1
                        continue
                    break
                if j < len(toks):
                    out.append((toks[j].lower(), toks[j + 1:]))
            expect_cmd = False
        i += 1
    return out


def commit_allowed(cwd, cmd):
    """No exception. The guard is unconditional, in every repo, always.

    Two earlier shapes were tried and both dropped. A hardcoded repo allow-list
    goes stale silently. Reading the rough-track doc for `In-Progress` re-armed
    itself, but a guard that opens files to decide is a guard whose behaviour
    depends on a document's wording — it breaks the first time a heading is
    reworded, and it fails in the direction that permits rather than blocks.

    A rough track is rare enough that the cost of blocking one is smaller than
    the cost of a guard nobody can predict.
    """
    return False


def blocked_reason(cmd, cwd=""):
    for sub, args in git_subcommands(cmd):
        if sub == "push":
            return sub
        if sub == "reset" and any(a in ("--hard", "--merge", "--keep") for a in args):
            return "reset --hard"
        if sub == "stash" and any(a in ("drop", "clear", "pop") for a in args):
            return "stash " + next(a for a in args if a in ("drop", "clear", "pop"))
    return None


def main():
    try:
        data = json.loads(sys.stdin.read())
    except Exception:
        return 0  # not a payload we understand — stay out of the way
    if data.get("tool_name") != "Bash":
        return 0
    cmd = (data.get("tool_input") or {}).get("command") or ""
    sub = blocked_reason(cmd, data.get("cwd") or "")
    if sub:
        sys.stderr.write(DENY.format(sub=sub))
        return 2  # exit 2 → PreToolUse blocks the call, stderr is fed back to the agent
    return 0


if __name__ == "__main__":
    sys.exit(main())
