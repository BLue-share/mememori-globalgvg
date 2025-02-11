# バッチから渡されたカレントディレクトリを変数に格納
$currentDir = $args[0]

# 仮想環境をアクティブにする
$venvActivateScript = "$currentDir\global_guild_war_status\venv\Scripts\Activate.ps1"

# PowerShellスクリプト実行ポリシーを変更して仮想環境をアクティブ化
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force

# 仮想環境のアクティベーション
& $venvActivateScript

# global_guild_war_status ディレクトリに移動してから backend フォルダに移動
cd "$currentDir\global_guild_war_status\backend"

# Djangoサーバーを起動
Start-Process powershell -ArgumentList "-NoExit", "python manage.py runserver"


# Reactサーバー起動
# Reactサーバーを起動する時に 'y' を入力してください。（この後すぐです）"
cd "$currentDir\global_guild_war_status\frontend"
Start-Process powershell -ArgumentList "-NoExit", "npm start"

# HTTPサーバー起動（別ウィンドウ）
cd "$currentDir\global_guild_war_status\frontend\build"
Start-Process powershell -ArgumentList "-NoExit", "python -m http.server 5000"
