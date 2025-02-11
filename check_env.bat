@echo off
chcp 65001 >nul
setlocal

echo 環境チェックを開始します...

:: Git チェック
where git >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Git が見つかりません。
) else (
    echo Git はインストール済みです。
)

:: Python チェック
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Python が見つかりません。
) else (
    echo Python はインストール済みです。
)

:: Node.js チェック
where node >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Node.js が見つかりません。
) else (
    echo Node.js はインストール済みです。
)

echo 環境チェック完了！
pause
