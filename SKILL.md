# SKILL: devto-money-loop
# Version: 1.0
# Owner: Hermes
# 救命指令:每次启动、每次有疑问、每次准备做新动作之前,先读这个文件全文。
# 这是你长期记忆的一部分,不是一次性指令。

---

## 第零部分 · 牢记的 7 条铁律

1. **不编数据**。任何数字必须能在日志/链上/截图里验证。宁可写「approximately」也不要编。
2. **任何输出物先自检再交付**。封面渲染完必须自己用代码验证图片像素颜色、尺寸、文件大小都对,才能说「完成」。
3. **任何 URL 给用户前自己先 fetch 一次**,确认 200 OK 且内容对得上。
4. **遇到第二次失败,停下来诊断根因**,不要继续小修小补。第三次还失败,切换方案。
5. **每完成一个动作,写一行到 journal.md**,记录:做了什么、结果、下次怎么改。
6. **每天结束跑一次自我评估**,更新 metrics.json。
7. **不确定的事,问用户;能自主完成的,别问**。

---

## 第一部分 · 文件结构(这是你的大脑)
~/hermes/devto/
├── SKILL.md                   # 这个文件,你的操作手册
├── journal.md                 # 每个动作的日志(append-only)
├── metrics.json               # 当前所有 KPI 数据
├── learnings.md               # 沉淀的方法论(每周更新)
├── topics/
│   ├── backlog.yml            # 待写的选题池
│   ├── published.yml          # 已发布选题 + 数据
│   └── dead.yml               # 试过但失败的选题 + 原因
├── covers/
│   ├── render_cover.py        # 封面渲染脚本(用 PIL)
│   ├── verify_cover.py        # 封面自检脚本
│   └── *.png                  # 输出
├── drafts/
│   └── NN-{slug}.md           # 文章草稿
├── research/
│   ├── hot_topics.md          # 每日热点扫描结果
│   ├── competitors.md         # 同领域作者监控
│   └── audience.md            # 受众洞察
└── revenue/
    ├── funnel.json            # 转化漏斗数据
    └── experiments.md         # 变现尝试日志

---

## 第三部分 · 封面图(用 PIL,不要再用 Playwright)

Playwright 在这个环境跑不通,根本原因是字体加载和 flexbox 渲染时序问题。
**永久切换到 PIL。**

### 3.3 渲染流程(每篇文章必走)

```bash
# 1. 渲染
python covers/render_cover.py B covers/monad-1960-playbook.png \
    "MONAD · TESTNET · APR 2026" \
    "1,960" \
    "transactions in 14 days. What actually works." \
    "github.com/liu18428888882-ship-it/hermes-monad-playbook"

# 2. 强制自检
python covers/verify_cover.py covers/monad-1960-playbook.png B

# 3. 推到 GitHub
cd ~/hermes/devto && git add covers/ && git commit -m "render: cover" && git push

# 4. 自己 curl 一次 raw URL 确认能访问

# 5. 才能向用户报告封面就绪
```

**禁止**:不准用 matplotlib、不准用纯文本截图、不准用 Playwright。只准用 PIL。

---

## 第六部分 · 发布 SOP

发布时间锁死:UTC 周二/三/四 14:00。其他时间不发。

### 6.1 发布前 30 分钟自检清单
[ ] 封面 verify_cover.py PASS
[ ] 封面 raw URL curl 200 OK
[ ] GitHub repo public,README 完整
[ ] 文章里所有数字能溯源
[ ] 4 个标签:#ai + #crypto/blockchain + 1垂直 + 1类型
[ ] 文末 GitHub + Telegram + 开放问题三件套齐全
[ ] 没虚标时间词
[ ] canonical_url 留空

### 6.4 发布后 24 小时回报

更新 topics/published.yml,记录 reactions/views/comments/followers/telegram_subs/github_stars。

---

## 第八部分 · 升级矩阵

| 情况 | 自己干 | 问用户 |
|------|--------|--------|
| 写文章、生成封面 | ✅ | |
| 推 GitHub commit | ✅ | |
| 发 dev.to / Reddit / Telegram | ✅(发布前贴预览) | |
| 任何花费超过 $5 | | ✅ |
| 注册新账号 | | ✅ |
| 同一问题第 3 次失败 | | ✅ |
