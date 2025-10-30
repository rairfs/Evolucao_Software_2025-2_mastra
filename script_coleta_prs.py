import requests
import csv
import time
from datetime import datetime
from tqdm import tqdm
import os
from dotenv import load_dotenv

# ===== Carrega variáveis do .env ===== 
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# ===== CONFIG =====
OWNER = "mastra-ai"
REPO = "mastra"
NUM_PRS = 100
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ===== HELPERS =====
def gh_get(url, params=None):
    headers = {"Accept": "application/vnd.github+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    return resp.json()

def format_date(date_str):
    if not date_str:
        return "-"
    dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    return dt.strftime("%Y-%m-%d %H:%M:%S")

# ===== 1) Coletar últimos PRs fechados =====
print(f"Coletando os últimos {NUM_PRS} PRs fechados...")
prs_url = f"https://api.github.com/repos/{OWNER}/{REPO}/pulls"
params = {"state": "closed", "per_page": NUM_PRS, "sort": "updated", "direction": "desc"}
prs = gh_get(prs_url, params=params)
pr_numbers = [pr["number"] for pr in prs]

# ===== 2) Gerar CSV com info dos PRs =====
csv_pr_file = os.path.join(OUTPUT_DIR, "pull_requests.csv")
with open(csv_pr_file, "w", newline="", encoding="utf-8-sig") as csvfile:
    writer = csv.writer(csvfile, delimiter=";")
    writer.writerow(["Número", "Título", "Autor", "Status", "Fechado em", "Link"])
    for pr in prs:
        status = "Merged" if pr.get("merged_at") else "Closed"
        closed_date = format_date(pr.get("closed_at"))
        writer.writerow([
            pr["number"],
            pr["title"],
            pr["user"]["login"],
            status,
            closed_date,
            pr["html_url"]
        ])
print(f"Arquivo '{csv_pr_file}' criado com sucesso!")

# ===== 3) Gerar Markdown com info dos PRs =====
md_file = os.path.join(OUTPUT_DIR, "pull_requests.md")
md_lines = [
    f"# 🧾 Últimos {NUM_PRS} Pull Requests Fechados — {OWNER}/{REPO}\n",
    "| Nº | Título | Autor | Status | Fechado em | Link |",
    "|----|---------|--------|----------|------------|------|"
]
for pr in prs:
    status = "🟣 Merged" if pr.get("merged_at") else "🔴 Closed"
    closed_date = format_date(pr.get("closed_at"))
    md_lines.append(
        f"| #{pr['number']} | {pr['title']} | @{pr['user']['login']} | {status} | {closed_date} | [ver PR]({pr['html_url']}) |"
    )
with open(md_file, "w", encoding="utf-8") as f:
    f.write("\n".join(md_lines))
print(f"Arquivo '{md_file}' criado com sucesso!")

# ===== 4) Coletar comentários de cada PR =====
all_comments = []

for pr_number in tqdm(pr_numbers, desc="Coletando comentários"):
    comments = []
    # Issue comments
    try:
        ic_url = f"https://api.github.com/repos/{OWNER}/{REPO}/issues/{pr_number}/comments"
        ic = gh_get(ic_url)
        for c in ic:
            comments.append({
                "pr_number": pr_number,
                "user": c.get("user", {}).get("login", ""),
                "comment": c.get("body", "")
            })
    except Exception as e:
        print(f"Erro ao coletar issue comments do PR {pr_number}: {e}")
    # Review comments
    try:
        rc_url = f"https://api.github.com/repos/{OWNER}/{REPO}/pulls/{pr_number}/comments"
        rc = gh_get(rc_url)
        for c in rc:
            comments.append({
                "pr_number": pr_number,
                "user": c.get("user", {}).get("login", ""),
                "comment": c.get("body", "")
            })
    except Exception as e:
        print(f"Erro ao coletar review comments do PR {pr_number}: {e}")

    all_comments.extend(comments)
    time.sleep(0.5)  # evitar limite da API

# ===== 5) Salvar comentários em CSV =====
csv_comments_file = os.path.join(OUTPUT_DIR, "pr_comments.csv")
with open(csv_comments_file, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["pr_number", "user", "comment"], delimiter=";")
    writer.writeheader()
    for c in all_comments:
        writer.writerow(c)

print(f"Comentários coletados: {len(all_comments)}")
print(f"Arquivo CSV de comentários gerado em: {csv_comments_file}")
