"""Draw the GitHub stats card from the owner's own token, so PRs and contributions in private repos count too.
STATS_TOKEN (classic PAT: repo, read:user) -> stats_card.py OUT.svg"""
import json, os, sys, urllib.request

Q = """{viewer{login name pullRequests{totalCount} issues{totalCount}
 repositoriesContributedTo(includeUserRepositories:true,contributionTypes:[COMMIT,PULL_REQUEST,ISSUE,REPOSITORY]){totalCount}
 contributionsCollection{totalCommitContributions}
 repositories(ownerAffiliations:OWNER,first:100,isFork:false){nodes{stargazerCount}}}}"""
req = urllib.request.Request("https://api.github.com/graphql", json.dumps({"query": Q}).encode(),
                             {"Authorization": "bearer " + os.environ["STATS_TOKEN"]})
v = json.load(urllib.request.urlopen(req))["data"]["viewer"]
c = v["contributionsCollection"]
rows = [("Total Stars Earned", sum(r["stargazerCount"] for r in v["repositories"]["nodes"])),
        ("Total Commits (last year)", c["totalCommitContributions"]),
        ("Total PRs", v["pullRequests"]["totalCount"]),
        ("Total Issues", v["issues"]["totalCount"]),
        ("Contributed to", v["repositoriesContributedTo"]["totalCount"])]
lines = "".join(f'<text x="25" y="{80 + 25 * i}" class="t">{k}:</text><text x="245" y="{80 + 25 * i}" class="t b">{n}</text>'
                for i, (k, n) in enumerate(rows))
svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="467" height="195" viewBox="0 0 467 195">
<style>.h{{font:600 18px 'Segoe UI',Ubuntu,sans-serif;fill:#9745f5}}.t{{font:600 14px 'Segoe UI',Ubuntu,sans-serif;fill:#fff}}.b{{font-weight:700}}</style>
<rect x="0.5" y="0.5" width="466" height="194" rx="4.5" fill="#000" stroke="#e4e2e2"/>
<text x="25" y="35" class="h">{(v["name"] or v["login"]).split()[0]}'s GitHub Stats</text>{lines}
</svg>"""
open(sys.argv[1], "w", encoding="utf-8").write(svg)
print(dict(rows))
