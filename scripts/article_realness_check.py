"""文章发布前真实感检查。低于 80 分不能发。"""
import sys, re

def check(md_path):
    text = open(md_path).read().lower()
    score = 100
    issues = []

    death_words = [
        ('hermes', -50), ('as an ai', -50), ('revolutioniz', -30),
        ('game-chang', -30), ('leverag', -10), ('delv', -10),
        ('in conclusion', -20), ("it's important to note", -20),
        ('unlock the power', -30), ('seamlessly', -10),
        ('cutting-edge', -20), ('robust', -5), ('comprehensive', -5),
        ('paradigm', -20), ('synergy', -30), ('ecosystem', -5),
    ]
    for word, penalty in death_words:
        count = text.count(word)
        if count > 0:
            score += penalty * count
            issues.append(f"'{word}' x{count} ({penalty * count})")

    raw = open(md_path).read()
    needed = {
        '具体时间锚点': r'\b(?:[12]?[0-9])(?::[0-5][0-9])?\s*(?:am|pm)\b',
        '货币金额': r'\$\d+',
        '第一人称我': r'\bi\s+(?:was|am|tried|failed|spent|lost|built|wrote|broke|fucked|messed)\b',
        '失败/错误词': r'\b(failed|fucked|messed|broke|wrong|stupid|dumb|mistake|error|bug)\b',
        '不确定表态': r'\b(i think|i\'m not sure|maybe|probably|could be wrong|might be)\b',
    }
    for name, pattern in needed.items():
        matches = len(re.findall(pattern, raw, re.I))
        if matches == 0:
            score -= 15
            issues.append(f"缺失:{name} (-15)")
        elif matches < 3:
            score -= 5
            issues.append(f"过少:{name} {matches}次 (-5)")

    paragraphs = [p for p in text.split('\n\n') if len(p.strip()) > 0 and not p.startswith('#')]
    if paragraphs:
        lens = [len(p.split()) for p in paragraphs]
        short_count = sum(1 for l in lens if l < 20)
        long_count = sum(1 for l in lens if l > 80)
        if short_count < 3:
            score -= 10
            issues.append(f"短段(<20词)过少: {short_count} (-10)")
        if long_count < 1:
            score -= 5
            issues.append(f"长段(>80词)缺失 (-5)")

    title_match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', open(md_path).read(), re.M | re.I)
    if title_match:
        title = title_match.group(1).lower()
        bad = ['is changing', 'the future of', 'why everyone', 'revolutioniz', 'introducing', 'unleash', 'mastering']
        for b in bad:
            if b in title:
                score -= 25
                issues.append(f"标题含死亡模式 '{b}' (-25)")

    wc = len(text.split())
    if wc < 1000:
        score -= 20
        issues.append(f"字数过少 {wc} (-20)")
    if wc > 2500:
        score -= 10
        issues.append(f"字数过多 {wc} (-10)")

    print(f"\n=== Realness Score: {score}/100 ===\n")
    for issue in issues:
        print(f"  - {issue}")
    print()

    if score < 80:
        print("FAIL")
        sys.exit(1)
    else:
        print("PASS")
        sys.exit(0)

if __name__ == "__main__":
    check(sys.argv[1])
