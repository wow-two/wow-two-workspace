#!/bin/bash
# UserPromptSubmit hook: short style line every turn, FULL response-style.md every Nth turn.
# Counters long-session attention fade: the per-turn line keeps recency, the periodic
# full reinject restores the complete ruleset into recent context.
N=10

cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0

input=$(cat)
sid=$(printf '%s' "$input" | sed -n 's/.*"session_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')
sid=${sid:-global}
f="${TMPDIR:-/tmp}/claude-style-turns-${sid}"
n=$(( $(cat "$f" 2>/dev/null || echo 0) + 1 ))
printf '%s' "$n" > "$f"

if [ $(( n % N )) -eq 0 ] && [ -f .claude/rules/response-style.md ]; then
  echo "STYLE RECHARGE (turn $n -- full ruleset, re-read and apply):"
  cat .claude/rules/response-style.md
else
  echo 'STYLE (enforce): verdict = line 1. Findings / analysis / progress -> bullet atoms: 1 claim per line, MAX ~15 words / 1 clause per bullet -- over that, split or cut. No em-dash appositive that restates the clause before it. No narrating own reasoning quality ("my claim was wrong because", "I asserted X I hadn'"'"'t earned") -- state the corrected fact only. Front-load the keyword, split "and" chains, compact each bullet (drop linkers / given subjects / motive windups), no pre-action narration, <=1 bold per section. Prose only for <=2-sentence conversational answers. Backtick every identifier. No agreement openers, praise inflation ("brilliant"), headline labels ("Bottom line:"), importance superlatives ("the most important..."), good/bad-news framing, minimizers ("just"), hedge stacks, unverified completion claims ("should now work"). A reply with >=2 sections -> a ### header per section AND a --- rule between; 1 topic -> tight bullets, no header. Close <=1 line, 1 question max. Expand only when asked.'
fi
