"""
metrics/analyzer.py

Minera commits, issues e PRs do repositório via PyGithub e gera
metrics/output/index.html com os dados embutidos (build-time injection).

Variáveis de ambiente obrigatórias:
  GITHUB_TOKEN       — token de acesso (github.token do Actions é suficiente)
  GITHUB_REPOSITORY  — ex: "org/repo-name" (setada automaticamente pelo Actions)
"""

import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from github import Auth, Github, GithubException

# Janela de análise em semanas
WEEKS_BACK = 12

# ---------------------------------------------------------------------------
# Helpers de tempo
# ---------------------------------------------------------------------------

def _utc(dt: datetime) -> datetime:
    """Garante que o datetime tenha tzinfo UTC."""
    if dt is None:
        return None
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def _week_label(dt: datetime) -> str:
    """Rótulo ISO week: '2024-W03'."""
    return dt.strftime("%Y-W%V")


def _ordered_week_buckets(weeks: int) -> dict[str, int]:
    """Dicionário ordenado das últimas `weeks` semanas, valores zerados."""
    now = datetime.now(timezone.utc)
    return {
        _week_label(now - timedelta(weeks=i)): 0
        for i in range(weeks - 1, -1, -1)
    }


# ---------------------------------------------------------------------------
# Mineração
# ---------------------------------------------------------------------------

def mine_commits(repo, since: datetime) -> dict[str, int]:
    buckets = _ordered_week_buckets(WEEKS_BACK)
    try:
        for commit in repo.get_commits(since=since):
            dt = _utc(commit.commit.author.date)
            label = _week_label(dt)
            if label in buckets:
                buckets[label] += 1
    except GithubException as exc:
        print(f"[WARN] Falha ao coletar commits: {exc}", file=sys.stderr)
    return buckets


def mine_issues(repo, since: datetime) -> dict:
    opened = _ordered_week_buckets(WEEKS_BACK)
    closed = _ordered_week_buckets(WEEKS_BACK)
    volumes: list[dict] = []

    try:
        for issue in repo.get_issues(state="all", since=since):
            # Issues da API do GitHub incluem PRs; ignorar.
            if issue.pull_request:
                continue

            created = _utc(issue.created_at)
            if created >= since:
                label = _week_label(created)
                if label in opened:
                    opened[label] += 1
                volumes.append({
                    "number": issue.number,
                    "title": (issue.title or "")[:60],
                    "body_len": len(issue.body or ""),
                })

            if issue.state == "closed" and issue.closed_at:
                closed_at = _utc(issue.closed_at)
                if closed_at >= since:
                    label = _week_label(closed_at)
                    if label in closed:
                        closed[label] += 1

    except GithubException as exc:
        print(f"[WARN] Falha ao coletar issues: {exc}", file=sys.stderr)

    # Ordena por body_len desc para o gráfico de volume ficar legível
    volumes.sort(key=lambda x: x["body_len"], reverse=True)

    return {"opened": opened, "closed": closed, "volumes": volumes[:30]}


def mine_pull_requests(repo, since: datetime) -> dict:
    opened = _ordered_week_buckets(WEEKS_BACK)
    merged = _ordered_week_buckets(WEEKS_BACK)
    rejected = _ordered_week_buckets(WEEKS_BACK)

    try:
        for pr in repo.get_pulls(state="all", sort="created", direction="desc"):
            created = _utc(pr.created_at)
            # PRs são retornados em ordem decrescente; para quando sai da janela.
            if created < since:
                break

            label = _week_label(created)
            if label in opened:
                opened[label] += 1

            if pr.merged_at:
                label_m = _week_label(_utc(pr.merged_at))
                if label_m in merged:
                    merged[label_m] += 1
            elif pr.closed_at:
                label_r = _week_label(_utc(pr.closed_at))
                if label_r in rejected:
                    rejected[label_r] += 1

    except GithubException as exc:
        print(f"[WARN] Falha ao coletar PRs: {exc}", file=sys.stderr)

    return {"opened": opened, "merged": merged, "rejected": rejected}


# ---------------------------------------------------------------------------
# Injeção estática
# ---------------------------------------------------------------------------

def _safe_json(payload: dict) -> str:
    """
    Serializa para JSON e escapa `</` para evitar que o parser HTML
    interprete `</script>` dentro de um bloco <script>.
    """
    raw = json.dumps(payload, ensure_ascii=False)
    return raw.replace("</", "<\\/")


def inject_and_write(template_path: Path, output_path: Path, payload: dict) -> None:
    template = template_path.read_text(encoding="utf-8")
    if "__DATA_PAYLOAD__" not in template:
        raise ValueError(
            f"Placeholder '__DATA_PAYLOAD__' não encontrado em {template_path}."
        )
    html = template.replace("__DATA_PAYLOAD__", _safe_json(payload), 1)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")


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
        sys.exit(f"[ERROR] Não foi possível acessar o repositório '{repo_name}': {exc}")

    since = datetime.now(timezone.utc) - timedelta(weeks=WEEKS_BACK)
    print(f"[INFO] Repositório : {repo_name}")
    print(f"[INFO] Janela      : últimas {WEEKS_BACK} semanas (desde {since.date()})")

    commits_data = mine_commits(repo, since)
    issues_data = mine_issues(repo, since)
    prs_data = mine_pull_requests(repo, since)

    weeks = list(commits_data.keys())
    has_any_activity = any([
        any(commits_data.values()),
        any(issues_data["opened"].values()),
        any(issues_data["closed"].values()),
        any(prs_data["opened"].values()),
    ])

    payload = {
        "generated_at": datetime.now(timezone.utc).strftime("%d/%m/%Y às %H:%M UTC"),
        "repo": repo_name,
        "has_activity": has_any_activity,
        "weeks": weeks,
        "commits": list(commits_data.values()),
        "issues_opened": list(issues_data["opened"].values()),
        "issues_closed": list(issues_data["closed"].values()),
        "issue_volumes": issues_data["volumes"],
        "prs_opened": list(prs_data["opened"].values()),
        "prs_merged": list(prs_data["merged"].values()),
        "prs_rejected": list(prs_data["rejected"].values()),
    }

    script_dir = Path(__file__).parent
    template_path = script_dir / "template.html"
    output_path = script_dir / "output" / "index.html"

    inject_and_write(template_path, output_path, payload)
    print(f"[INFO] Dashboard gerado em: {output_path}")


if __name__ == "__main__":
    main()