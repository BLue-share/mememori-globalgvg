from django.shortcuts import render, redirect
import logging
import requests

logger = logging.getLogger(__name__)

CASTLE_NAMES = ["アイン", "イエソド", "マルクト", "ケテル", "テフォレト", "クシェル", "シトリ", "トパズ", "メラル", "ペリド", "ファリア", "ラピス", "ラリマル", "マリン", "アメト", "ラベン", "ジルコン", "オニキス", "フロライト", "ガネット", "ルラ"]

def global_guild_form(request):
    """ギルド戦フォームを表示"""
    return render(request, "global_guild_form.html")

def global_guild_status(request):
    """APIからギルド戦情報を取得し、結果ページにリダイレクト"""
    if request.method == "POST":
        # リクエストデータを確認
        print(request.POST)  # デバッグ用にPOSTデータを表示

        server = request.POST.get("server", "1")
        world = request.POST.get("world", "").strip()
        class_type = request.POST.get("class", "1")
        block = request.POST.get("block", "0")
        group_id = request.POST.get("group_id", "")  # group_idを取得
    else:
        server = "1"
        world = ""
        class_type = "1"
        block = "0"
        group_id = ""  # 最初は空で設定

    # 送信されたgroup_idが空ならばデフォルトを設定
    if not group_id:
        group_id = "1"

    api_url = f"https://api.mentemori.icu/wg/{group_id}/globalgvg/{class_type}/{block}/latest"
    print(api_url)  # APIリクエストのURLをデバッグ用に表示

    try:
        response = requests.get(api_url)
        response.raise_for_status()

        data = response.json()
        guilds = data.get("data", {}).get("guilds", {})
        castles = data.get("data", {}).get("castles", [])

        formatted_castles = []
        for castle in castles:
            castle_id = castle.get("CastleId", 0)
            castle_name = CASTLE_NAMES[castle_id - 1] if 1 <= castle_id <= len(CASTLE_NAMES) else f"Unknown ({castle_id})"
            global_guild_id = str(castle.get("GuildId", ""))
            attacker_global_guild_id = str(castle.get("AttackerGuildId", ""))

            formatted_castles.append({
                "group_id": group_id,
                "castle_name": castle_name,
                "global_guild_name": guilds.get(global_guild_id, "Unknown Guild"),
                "attacker_global_guild_name": guilds.get(attacker_global_guild_id, "No Attacker"),
                "attack_party_count": castle.get("AttackPartyCount", 0),
                "defense_party_count": castle.get("DefensePartyCount", 0),
                "state": "Occupied" if castle.get("GvgCastleState", 0) == 1 else "Free",
                "ko_count": castle.get("LastWinPartyKnockOutCount", 0)
            })

        return render(request, "global_guild_status.html", {
            "castles": formatted_castles,
            "server": server,
            "world": world,
            "error": None
        })

    except Exception as err:
        logger.error(f"エラー発生: {err}")
        return render(request, "global_guild_status.html", {
            "castles": [],
            "server": server,
            "world": world,
            "error": "データ取得に失敗しました"
        })
