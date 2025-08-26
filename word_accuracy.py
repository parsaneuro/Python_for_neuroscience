import math

def damerau_levenshtein(a, b):
    """
    Compute Damerau–Levenshtein distance between two strings.
    Allows insertion, deletion, substitution, and adjacent transposition.
    """
    n, m = len(a), len(b)
    if n == 0:
        return m
    if m == 0:
        return n

    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,      # deletion
                dp[i][j - 1] + 1,      # insertion
                dp[i - 1][j - 1] + cost  # substitution
            )
            if i > 1 and j > 1 and a[i - 1] == b[j - 2] and a[i - 2] == b[j - 1]:
                dp[i][j] = min(dp[i][j], dp[i - 2][j - 2] + 1)

    return dp[n][m]

def is_blank(x):
    """Check if input is None, NaN, or empty string."""
    if x is None:
        return True
    if isinstance(x, float) and math.isnan(x):
        return True
    if isinstance(x, str) and x.strip() == "":
        return True
    return False

def get_accuracy(target, response):
    """
    Compute keyword accuracy between target and response.
    Returns a dict with correct, total, and accuracy %.
    """
    target_words = target.lower().split()

    # Empty or invalid response -> 0 correct
    if is_blank(response):
        return {"correct": 0, "total": len(target_words), "accuracy": 0.0}

    response_words = str(response).lower().split()
    correct = 0
    used = [False] * len(target_words)

    for resp in response_words:
        available = [i for i, u in enumerate(used) if not u]
        if not available:
            break

        # find best match among unused target words
        distances = [damerau_levenshtein(resp, target_words[i]) for i in available]
        best_idx = available[distances.index(min(distances))]
        best_dist = min(distances)

        longest = max(len(resp), len(target_words[best_idx])) or 1
        normalized = best_dist / longest

        if best_dist <= 2 and normalized <= 0.25:
            used[best_idx] = True
            correct += 1

    total = len(target_words)
    accuracy = round(100.0 * correct / total, 1) if total > 0 else 0.0
    return {"correct": correct, "total": total, "accuracy": accuracy}

# --- Example usage ---
if __name__ == "__main__":
    examples = [
        ("quick brown fox", "quik brwn fx"),
        ("neural network models", "neural netwrok modal"),
        ("data science", None),
        ("data science", ""),
        ("kitten sitting", "sitting kitten"),
    ]
    for tgt, rsp in examples:
        print(tgt, rsp, "->", get_accuracy(tgt, rsp))
