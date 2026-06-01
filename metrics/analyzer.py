"""
metrics/analyzer.py

Coleta métricas do repositório via PyGithub e gera docs/scrum/metrics.json.

Variáveis de ambiente obrigatórias:
  GITHUB_TOKEN       — token de acesso
  GITHUB_REPOSITORY  — ex: "org/repo-name" (injetado automaticamente pelo Actions)

Seções geradas:
  issues_per_week          — issues abertas e fechadas por semana
  commit_message_histogram — distribuição de tamanho das mensagens de commit
  coauthors_per_week       — co-autores encontrados nos commits por semana
  commit_heatmap           — contagem de commits por dia da semana × hora
  top_committers           — top 10 por número de commits
  top_pr_authors           — top 10 por número de PRs abertas
  top_issue_contributors   — top 10 por issues abertas + fechadas
"""

import json
import os
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from github import Auth, Github, GithubException

WEEKS_BACK = 12
TOP_N = 10
OUTPUT_PATH = Path("docs/scrum/metrics.json")

HISTOGRAM_BUCKETS = [
    ("0-20",   0,   20),
    ("21-50",  21,  50),
    ("51-100", 51,  100),
    ("101-200",101, 200),
    ("200+",   201, float("inf")),
]

COAUTHOR_RE = re.compile(r"Co-authored-by:[^\n]+", re.IGNORECASE)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _utc(dt: datetime) -> datetime:
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def _week_label(dt: datetime) -> str:
    return dt.strftime("%Y-W%V")


def _ordered_weeks(weeks: int) -> list[str]:
    from datetime import timedelta
    now = datetime.now(timezone.utc)
    return [_week_label(now - timedelta(weeks=i)) for i in range(weeks - 1, -1, -1)]


# ---------------------------------------------------------------------------
# Mineração
# ---------------------------------------------------------------------------

def mine_issues(repo, since: datetime) -> tuple[list, list, list]:
    """
    Retorna:
      issues_per_week     — [{"week": str, "opened": int, "closed": int}]
      top_contributors    — dict {username: {"name": str, "opened": int, "closed": int}}
    """
    weeks = _ordered_weeks(WEEKS_BACK)
    opened_by_week = defaultdict(int, {w: 0 for w in weeks})
    closed_by_week = defaultdict(int, {w: 0 for w in weeks})
    contributors: dict[str, dict] = defaultdict(lambda: {"name": "", "opened": 0, "closed": 0})

    try:
        for issue in repo.get_issues(state="all", since=since):
            if issue.pull_request:
                continue

            username = issue.user.login if issue.user else "ghost"
            name = (issue.user.name or username) if issue.user else "ghost"

            created = _utc(issue.created_at)
            if created >= since:
                label = _week_label(created)
                if label in opened_by_week:
                    opened_by_week[label] += 1
                contributors[username]["name"] = name
                contributors[username]["opened"] += 1

            if issue.state == "closed" and issue.closed_at:
                closed_at = _utc(issue.closed_at)
                if closed_at >= since:
                    label = _week_label(closed_at)
                    if label in closed_by_week:
                        closed_by_week[label] += 1
                    # Atribui o fechamento ao usuário que fechou, se disponível
                    closer = issue.closed_by
                    closer_login = closer.login if closer else username
                    closer_name = (closer.name or closer_login) if closer else name
                    contributors[closer_login]["name"] = closer_name
                    contributors[closer_login]["closed"] += 1

    except GithubException as exc:
        print(f"[WARN] Falha ao coletar issues: {exc}", file=sys.stderr)

    issues_per_week = [
        {"week": w, "opened": opened_by_week[w], "closed": closed_by_week[w]}
        for w in weeks
    ]

    top_issue_contributors = sorted(
        [
            {
                "username": u,
                "name": d["name"] or u,
                "opened": d["opened"],
                "closed": d["closed"],
                "total": d["opened"] + d["closed"],
            }
            for u, d in contributors.items()
        ],
        key=lambda x: x["total"],
        reverse=True,
    )[:TOP_N]

    return issues_per_week, top_issue_contributors


def mine_commits(repo, since: datetime) -> tuple[list, list, list, list]:
    """
    Retorna:
      commit_message_histogram — [{"range": str, "count": int}]
      coauthors_per_week       — [{"week": str, "count": int}]
      commit_heatmap           — [{"day": int, "hour": int, "count": int}]
      top_committers           — [{"username": str, "name": str, "commits": int}]
    """
    weeks = _ordered_weeks(WEEKS_BACK)
    coauthors_by_week: dict[str, int] = defaultdict(int, {w: 0 for w in weeks})
    heatmap: dict[tuple[int, int], int] = defaultdict(int)
    committers: dict[str, dict] = defaultdict(lambda: {"name": "", "commits": 0})

    hist_counts = {b[0]: 0 for b in HISTOGRAM_BUCKETS}

    try:
        for commit in repo.get_commits(since=since):
            author = commit.author
            username = author.login if author else (commit.commit.author.name or "ghost")
            name = (author.name or username) if author else (commit.commit.author.name or "ghost")

            committers[username]["name"] = name
            committers[username]["commits"] += 1

            # Histograma de tamanho da mensagem
            msg = commit.commit.message or ""
            first_line = msg.split("\n")[0]
            length = len(first_line)
            for label, lo, hi in HISTOGRAM_BUCKETS:
                if lo <= length <= hi:
                    hist_counts[label] += 1
                    break

            # Co-autores
            coauthor_matches = COAUTHOR_RE.findall(msg)
            valid_coauthors = 0
            for match in coauthor_matches:
                # Formato válido: "Co-authored-by: Name <email>"
                if "<" in match and ">" in match:
                    valid_coauthors += 1
            if valid_coauthors:
                dt = _utc(commit.commit.author.date)
                label = _week_label(dt)
                if label in coauthors_by_week:
                    coauthors_by_week[label] += valid_coauthors

            # Heatmap: day=0 (segunda) ... day=6 (domingo)
            dt = _utc(commit.commit.author.date)
            day = dt.weekday()   # 0 = segunda
            hour = dt.hour
            heatmap[(day, hour)] += 1

    except GithubException as exc:
        print(f"[WARN] Falha ao coletar commits: {exc}", file=sys.stderr)

    commit_message_histogram = [
        {"range": label, "count": hist_counts[label]}
        for label, _, _ in HISTOGRAM_BUCKETS
    ]

    coauthors_per_week = [
        {"week": w, "count": coauthors_by_week[w]}
        for w in weeks
    ]

    commit_heatmap = [
        {"day": day, "hour": hour, "count": count}
        for (day, hour), count in sorted(heatmap.items())
    ]

    top_committers = sorted(
        [
            {"username": u, "name": d["name"] or u, "commits": d["commits"]}
            for u, d in committers.items()
        ],
        key=lambda x: x["commits"],
        reverse=True,
    )[:TOP_N]

    return commit_message_histogram, coauthors_per_week, commit_heatmap, top_committers


def mine_pull_requests(repo, since: datetime) -> list:
    """
    Retorna top_pr_authors — [{"username": str, "name": str, "prs_opened": int}]
    """
    pr_authors: dict[str, dict] = defaultdict(lambda: {"name": "", "prs_opened": 0})

    try:
        for pr in repo.get_pulls(state="all", sort="created", direction="desc"):
            created = _utc(pr.created_at)
            if created < since:
                break
            user = pr.user
            username = user.login if user else "ghost"
            name = (user.name or username) if user else "ghost"
            pr_authors[username]["name"] = name
            pr_authors[username]["prs_opened"] += 1
    except GithubException as exc:
        print(f"[WARN] Falha ao coletar PRs: {exc}", file=sys.stderr)

    return sorted(
        [
            {"username": u, "name": d["name"] or u, "prs_opened": d["prs_opened"]}
            for u, d in pr_authors.items()
        ],
        key=lambda x: x["prs_opened"],
        reverse=True,
    )[:TOP_N]


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

def main() -> None:
    token = os.environ.get("GITHUB_TOKEN")
    repo_name = os.environ.get("GITHUB_REPOSITORY")

    if not token:
        sys.exit("[ERROR] GITHUB_TOKEN não definido.")
    if not repo_name:
        sys.exit("[ERROR] GITHUB_REPOSITORY não definido.")

    g = Github(auth=Auth.Token(token))
    try:
        repo = g.get_repo(repo_name)
    except GithubException as exc:
        sys.exit(f"[ERROR] Não foi possível acessar '{repo_name}': {exc}")

    from datetime import timedelta
    since = datetime.now(timezone.utc) - timedelta(weeks=WEEKS_BACK)
    print(f"[INFO] Repositório : {repo_name}")
    print(f"[INFO] Janela      : {WEEKS_BACK} semanas (desde {since.date()})")

    print("[INFO] Coletando issues...")
    issues_per_week, top_issue_contributors = mine_issues(repo, since)

    print("[INFO] Coletando commits...")
    commit_message_histogram, coauthors_per_week, commit_heatmap, top_committers = mine_commits(repo, since)

    print("[INFO] Coletando pull requests...")
    top_pr_authors = mine_pull_requests(repo, since)

    payload = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "repository": repo_name,
        "issues_per_week": issues_per_week,
        "commit_message_histogram": commit_message_histogram,
        "coauthors_per_week": coauthors_per_week,
        "commit_heatmap": commit_heatmap,
        "top_committers": top_committers,
        "top_pr_authors": top_pr_authors,
        "top_issue_contributors": top_issue_contributors,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[INFO] metrics.json gerado em: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()