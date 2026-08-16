# check-style — message text + per-workspace config

*Last updated: 2026-08-15*

> Read by `.claude/hooks/check-style.py`. The script holds no user-facing prose;
> every word it emits comes from a `## section` below.
> Sections are parsed by exact `## name` headers — rename one and the script
> degrades to a bare findings list plus a loud stdout line.

## header
STYLE CHECK — mechanical measurement of your PREVIOUS reply against `.claude/rules/response-style.md`.
Advisory: nothing was blocked, the reply already shipped. Apply the fix to THIS turn's reply.

## footer
Counting rule: the bullet's own text, backticks included, `- ` marker excluded — `awk '{print length($0)-2}'`.
The compression floor outranks the cap: keep scope / causality / negation words and run over rather than collapse into a noun stack.
A finding here can be wrong — exemptions the checker cannot see (a verbatim quote, a deliverable) win over its count.

## walkthrough-markers
