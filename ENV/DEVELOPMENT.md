# 開発環境

## 対象バージョン

- Python 3.13.14（パッチバージョンまで固定）
- 固定箇所は2か所：
  1. `.devcontainer/devcontainer.json`（`ghcr.io/devcontainers/features/python:1` フィーチャーで `3.13.14` を指定）
  2. `pyproject.toml` の `requires-python = "==3.13.14"`
- 依存パッケージ（pytest・ruff）のバージョンは `requirements-lock.txt` に固定している（`pyproject.toml` から `pip-compile` で生成）。

## devcontainer / Codespaces

- Codespacesでリポジトリを開くと、`.devcontainer/devcontainer.json` に基づき自動的にコンテナがビルドされ、Python 3.13.14が使用可能になる。
- コンテナ作成後、`postCreateCommand` により `requirements-lock.txt` の内容（pytest・ruff）が自動インストールされる。
- 再ビルド後、以下を実行してバージョンが一致することを確認する。

  ```sh
  python --version
  # => Python 3.13.14
  ```

- CI（`.github/workflows/ci.yml`）は `actions/setup-python@v5` で `python-version: "3.13"` を指定しており、3.13系の最新パッチが解決される。devcontainerの固定パッチ（3.13.14）とCIが解決するパッチにズレが生じた場合は、本ファイルとdevcontainer側のバージョンを見直す。

## 依存パッケージの更新手順

1. `pyproject.toml` の `[project.dependencies]` を編集する。
2. 以下を実行し `requirements-lock.txt` を再生成する（Python 3.13環境で実行することを推奨）。

   ```sh
   pip install pip-tools
   pip-compile --output-file=requirements-lock.txt pyproject.toml
   ```

3. devcontainerを再ビルドし、`pip install --no-cache-dir -r requirements-lock.txt` が正常に完了することを確認する。

## 現在の実行環境（旧・参考情報）

- devcontainer整備前は、このCodespace上のPythonが `3.12.1` であり対象バージョン（3.13系）と異なっていた。
- devcontainer整備（本ドキュメント記載の内容）により解消済み。今後はCodespaces起動時に3.13.14へ統一される。
