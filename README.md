# python-syntax-diff-book

「差分で読むPython文法 — 他言語経験者のための最短ルート」電子書籍（Kindle・リフロー型EPUB）デモ版（試し読み版）の制作リポジトリ。

Webアプリケーションではないため、ログイン機能・画面（ページ）・APIは存在しない。

## 対象読者

Java/C#・JavaScript/TypeScript・Ruby/PHP・Go/Rustなど他言語経験者で、Pythonの文法を「差分」として最短で押さえたい人。プログラミング未経験者は対象外。

## 対象バージョン

Python 3.13系（パッチバージョンまでdevcontainerとロックファイルでピン留めする方針。詳細は `ENV/DEVELOPMENT.md` を参照）。

## 開発フロー

本文中のPythonコードリストは TDD（plan → red test → coding → green test）で作成する。詳細は `CLAUDE.md` を参照。

```sh
pytest
ruff check .
```

## ディレクトリ

| ディレクトリ | 役割 |
|---|---|
| `TASKS/` | タスク管理 |
| `DEBUG/` | バグ・不具合報告 |
| `CLIENT/` | 著者・編集からの要望 |
| `WORK/` | 作業報告 |
| `ENV/` | 開発環境・KDP公開要件 |
| `SPEC/` | 仕様書・図解（章依存図・編集ループ図） |
| `DELETE/` | ゴミ箱（削除予定ファイルの退避先） |
| `app-ui/` | 表紙・図版のデザインモック（参照専用） |

## 要件定義

詳細な要件・章構成・読者ペルソナは `requirements.md` を参照（同ファイルは非公開のため `.gitignore` 対象）。
