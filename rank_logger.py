import requests
import subprocess

API_URL = "https://api.the-finals-leaderboard.com/v1/leaderboard/s7/crossplay?name=Soul%236810".replace("#", "%23")
FILE_PATH = "docs/latest_rank.txt"

def get_rank_info():
    try:
        resp = requests.get(API_URL)
        data = resp.json()

        if "data" in data and isinstance(data["data"], list) and data["data"]:
            player = data["data"][0]
            score = player.get("rankScore")
            rank = player.get("rank")
            return score, rank
    except Exception as e:
        print("Error:", e)
    return None, None

def log_and_push_info():
    score, rank = get_rank_info()
    if score and rank:
        message = f"Rank Score: {score:,} | Rank: #{rank}"
        with open(FILE_PATH, "w") as f:
            f.write(message)
        print("Updated:", message)

        subprocess.run(["git", "add", FILE_PATH])
        subprocess.run(["git", "commit", "-m", "Update rank info"])
        subprocess.run(["git", "push"])
    else:
        print("Rank or score not found.")

if __name__ == "__main__":
    log_and_push_info()