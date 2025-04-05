import asyncio
import requests
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatEvent

# ===== CONSULTA DE RANK DO CF =====
def consultar_rank_cf(nickname):
    if not nickname:
        return "❌ Nickname não fornecido."

    url = "https://br.crossfire.z8games.com/rest/eloranking.json"
    params = {
        "startrow": 0,
        "endrow": 30,
        "name": nickname,
        "rankType": "user",
        "period": "all"
    }

    headers = {
        "accept": "*/*",
        "accept-language": "pt-BR,pt;q=0.9,en;q=0.8,es;q=0.7",
        "cache-control": "no-cache",
        "dnt": "1",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://br.crossfire.z8games.com/competitiveranking.html",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }

    cookies = {
        "dontaskregion": "1"
    }


    try:
        response = requests.get(url, headers=headers, cookies=cookies, params=params, timeout=10)
        if response.status_code == 200:
            dados = response.json()
            resultados = dados.get("ds_WEB_USER_ALLTIME_TM_Result")
            if resultados and len(resultados) > 0:
                jogador = resultados[0]
                ign = jogador.get("ign")
                patente = jogador.get("tier_group_name")
                pts = jogador.get("rank_score")
                rank = jogador.get("rank")
                wins = jogador.get("win_cnt")
                losses = jogador.get("lose_cnt")
                kd = jogador.get("kd")
                winrate = jogador.get("vit")

                return (f"📛 Nick: {ign} | 🏅 {patente} ({pts} pts) | 🔢 Rank: {rank}º | "
                        f"📈 Win Rate: {winrate} | ⚔️ K/D: {kd} | ✅ V: {wins} ❌ D: {losses}")
            else:
                return "❌ Jogador não encontrado ou sem ranking."
        else:
            return f"❌ Erro {response.status_code}: Não foi possível obter os dados."
    except requests.RequestException as e:
        return f"⚠️ Erro de conexão: {e}"

# ===== FUNÇÃO PRINCIPAL =====
async def main():
    client_id = 'hb9f5h5mjj1n0fcbv7rpirlo456io5'
    client_secret = 'k4geg3d23byw6alzpark9wns801dky'
    bot_nick = 'bot_cfal'

    canais = ['yuri_de_saogonsalo', 'paozin9']

    try:
        twitch = await Twitch(client_id, client_secret)
        auth = UserAuthenticator(twitch, [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT])
        token, refresh_token = await auth.authenticate()
        await twitch.set_user_authentication(token, [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT], refresh_token)

        chat = await Chat(twitch)

        async def on_ready(evt: EventData):
            for canal in canais:
                await chat.join_room(canal)
                print(f"✅ Bot entrou em #{canal} como {bot_nick}")

        async def on_message(msg: ChatMessage):
            if msg.text.startswith("!rank "):
                nickname = msg.text.split("!rank ", 1)[1].strip()
                resultado = consultar_rank_cf(nickname)
                await chat.send_message(msg.room.name, resultado[:450])

        chat.register_event(ChatEvent.READY, on_ready)
        chat.register_event(ChatEvent.MESSAGE, on_message)

        chat.start()

    except Exception as e:
        print(f"❌ Ocorreu um erro: {e}")

if __name__ == "__main__":
    asyncio.run(main())
