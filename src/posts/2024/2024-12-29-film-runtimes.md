---
title: Have "critically acclaimed" films been getting longer?
date: 2024-12-29
---

---

If we take Cannes Palme d'Or winners as a proxy for "critically acclaimed"
films: yes.

<img class="figure" src="/posts/2024/static/cannes_chart.png" width=100%>


## Code


```py
import requests

def get_runtime(boxd_url: str) -> int:
    response = requests.get(boxd_url)
    if response.status_code != 200:
        print(f"Failed to retrieve the webpage for {boxd_url}")
        return -1

    try:
        lines = response.text.splitlines()
        for line in lines:
            if "&nbsp;mins" in line:
                runtime = int(line.removesuffix("&nbsp;mins &nbsp;"))
                return runtime
    except Exception as e:
        print(f"got error {e} for {boxd_url}")
        return -1
```