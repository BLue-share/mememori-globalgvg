import React, { useEffect, useState } from "react";
import axios from "axios";

// キャッスルのリストと番号をマッピング
const castleNames = [
    "ブラッセル", "ウィスケルケー", "モダーヴ", "シメイ", "グラベンスティン", "カンブル", "クインティヌス", "ランベール", "サンジャック",
    "ミヒャエル", "ナミュール", "シャルルロア", "アルゼット", "エノー", "ワーヴル", "モンス", "クリストフ", "コルトレイク", "イーペル",
    "サルヴァトール", "バーフ"
];

function App() {
    const [data, setData] = useState(null);
    const [guildsList, setGuildsList] = useState([]);

    const fetchData = () => {
        axios.get("http://127.0.0.1:8000/guild/status/")
            .then((response) => {
                setData(response.data);

                // guilds と castles をリストに整理
                const guilds = response.data.data.guilds;
                const castles = response.data.data.castles;

                // GuildId と CastleId を組み合わせたリストを作成
                const updatedGuildsList = castles.map((castle) => {
                    const guildName = guilds[castle.GuildId]; // GuildIdに基づいてギルド名を取得
                    const castleId = castle.CastleId;
                    const castleName = castleNames[castleId - 1]; // CastleIdを使って名前に変換 (配列は0始まりなので-1)
                    return { castleId: castleName, guildName };
                });

                setGuildsList(updatedGuildsList); // リストを更新
            })
            .catch((error) => console.error("API呼び出しエラー:", error));
    };

    useEffect(() => {
        const updateInterval = () => {
            const now = new Date();
            const jstNow = new Date(now.toLocaleString("en-US", { timeZone: "Asia/Tokyo" }));
            const hours = jstNow.getHours();
            const minutes = jstNow.getMinutes();

            // 20:45 ～ 21:30 の間は 2秒更新、それ以外は 30分更新
            if ((hours === 20 && minutes >= 45) || (hours === 21 && minutes < 30)) {
                return 2000; // 2秒
            }
            return 1800000; // 30分 (1800000ミリ秒)
        };

        let intervalTime = updateInterval();
        fetchData();

        const scheduleUpdate = () => {
            setTimeout(() => {
                fetchData();
                intervalTime = updateInterval();
                scheduleUpdate();
            }, intervalTime);
        };

        scheduleUpdate();

        return () => clearTimeout(scheduleUpdate);
    }, []);

    return (
        <div>
            <h1>Guild War Status</h1>
            {data ? (
                <div>
                    <h2>ギルドとキャッスルのリスト</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Castle Name</th>
                                <th>Guild Name</th>
                            </tr>
                        </thead>
                        <tbody>
                            {guildsList.map((item, index) => (
                                <tr key={index}>
                                    <td>{item.castleId}</td>
                                    <td>{item.guildName}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            ) : (
                <p>Loading...</p>
            )}
        </div>
    );
}

export default App;
