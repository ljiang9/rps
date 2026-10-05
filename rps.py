"""rps —— 终端石头剪刀布。

和电脑对战，支持中文/英文/拼音输入，记分，可设固定局数。
纯标准库，纯本地。
"""

import argparse
import secrets
import sys

MOVES = ("石头", "剪刀", "布")

# 输入别名：中文、英文、拼音
ALIASES = {
    "石头": "石头", "拳头": "石头", "rock": "石头", "r": "石头", "shitou": "石头",
    "剪刀": "剪刀", "scissors": "剪刀", "s": "剪刀", "jiandao": "剪刀",
    "布": "布", "paper": "布", "p": "布", "bu": "布",
}

# BEATS[x] = x 能赢的招式
BEATS = {"石头": "剪刀", "剪刀": "布", "布": "石头"}

VERSION = "0.1.0"


def decide(player, computer):
    """判定一局。返回 'win' / 'lose' / 'draw'（站在玩家角度）。"""
    if player == computer:
        return "draw"
    return "win" if BEATS[player] == computer else "lose"


def normalize(text):
    """把用户输入归一化为标准招式；无法识别返回 None。"""
    if text is None:
        return None
    key = text.strip().lower()
    return ALIASES.get(key)


def random_move():
    return secrets.choice(MOVES)


def play_interactive(rounds=None):
    """交互对战。rounds 为 None 时无限局直到 q 退出。"""
    wins = losses = draws = 0
    played = 0
    target = f"（共 {rounds} 局）" if rounds else "（输入 q 退出）"
    print(f"===== 石头剪刀布 {target} =====")
    print("输入：石头/剪刀/布（也可用 rock/scissors/paper 或拼音），q 退出")
    while True:
        if rounds is not None and played >= rounds:
            break
        try:
            raw = input(f"\n第 {played + 1} 局，你出：")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if raw.strip().lower() == "q":
            break
        move = normalize(raw)
        if move is None:
            print("看不懂，请输入 石头/剪刀/布（或 rock/scissors/paper），q 退出。")
            continue
        cpu = random_move()
        result = decide(move, cpu)
        played += 1
        if result == "win":
            wins += 1
            verdict = "🎉 你赢了！"
        elif result == "lose":
            losses += 1
            verdict = "😅 电脑赢了。"
        else:
            draws += 1
            verdict = "🤝 平局。"
        print(f"你：{move}　电脑：{cpu}　{verdict}")
        print(f"比分 你 {wins} : {losses} 电脑（平 {draws}）")
    print(f"\n===== 结束：你 {wins} 胜 {losses} 负 {draws} 平 =====")
    if wins > losses:
        print("🏆 总比分你赢了！")
    elif losses > wins:
        print("💻 总比分电脑赢了，再接再厉！")
    else:
        print("🤝 总比分打平！")
    return 0 if wins >= losses else 1


def play_auto(n):
    """电脑内战 n 局，打印统计。理论上胜/负/平各约 1/3。"""
    wins = losses = draws = 0
    for _ in range(n):
        r = decide(random_move(), random_move())
        if r == "win":
            wins += 1
        elif r == "lose":
            losses += 1
        else:
            draws += 1
    print(f"电脑内战 {n} 局：")
    print(f"  先手胜：{wins}（{wins / n:.1%}）")
    print(f"  后手胜：{losses}（{losses / n:.1%}）")
    print(f"  平局：{draws}（{draws / n:.1%}）")
    return {"win": wins, "lose": losses, "draw": draws}


def build_parser():
    p = argparse.ArgumentParser(
        prog="rps",
        description="终端石头剪刀布：和电脑对战。",
    )
    p.add_argument("--version", action="version", version=f"rps {VERSION}")
    p.add_argument("--rounds", type=int, default=None,
                   help="固定局数（默认无限局，q 退出）")
    p.add_argument("--auto", type=int, default=None, metavar="N",
                   help="电脑内战 N 局并打印统计（非交互）")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.auto is not None:
        if args.auto <= 0:
            print("error: --auto 需要正整数", file=sys.stderr)
            return 2
        play_auto(args.auto)
        return 0
    if args.rounds is not None and args.rounds <= 0:
        print("error: --rounds 需要正整数", file=sys.stderr)
        return 2
    return play_interactive(args.rounds)


if __name__ == "__main__":
    sys.exit(main())
