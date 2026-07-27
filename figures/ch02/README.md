# figures/ch02/ 第2章の図版

第2章「構文の外形とオブジェクトモデル」用の図版4点（`requirements.md` 4節
「目次構成表」で第2章の図版点数は4点と定義済み。GitHub Issue #7対応）。

本書の図版方針（CLAUDE.md「画像・図版方針」／`.claude/agents/designer.md`）に従い、
表紙・図版はAI生成画像を用いる方針である。本ディレクトリはその実行環境上の制約
（このリポジトリの作業環境には画像生成ツールが接続されていない）を踏まえ、
第1章（`figures/ch01/`）と同じ2段構成で管理する。

1. **仕様書**（`figure-XX-*-spec.md`）：構図・目的・対象読者・生成プロンプト・
   CRAPレビュー・グレースケール確認の記録。実際にAI画像生成ツールを使う担当者が
   このプロンプトをそのまま使って本番画像を生成できるようにする。
2. **プレースホルダー**（`figure-XX-*-placeholder.svg`）：本番のAI生成画像に
   差し替えるまでの仮画像。単純な枠線・線種と注記のみで構成し、FontAwesome
   アイコンや絵文字などの装飾は含めない（プレースホルダーである旨を混同させ
   ないため）。本文からはこのSVGを参照しており、本番画像に差し替える際は
   同じファイル名・同じアスペクト比のPNG/JPGに置き換えること。

## 図版一覧

| # | ファイル（spec） | ファイル（placeholder） | 章内の参照箇所 | 内容 |
|---|---|---|---|---|
| 図2-1 | `figure-01-truthiness-protocol-spec.md` | `figure-01-truthiness-protocol-placeholder.svg` | 2.4節「真偽判定は`__bool__`・`__len__`のプロトコルに従う」の出力直後 | `if obj:`評価時に`__bool__`→`__len__`→常に`True`の順で判定するフローチャート |
| 図2-2 | `figure-02-name-binding-spec.md` | `figure-02-name-binding-placeholder.svg` | 2.6節「代入は名前の束縛である」末尾 | 変数は値を格納する箱ではなくオブジェクトに貼るラベルであることを、連鎖代入（1つの箱に3枚のラベル）と累算代入（不変intの再束縛／可変listのその場での変更）の2パネルで示す |
| 図2-3 | `figure-03-is-vs-equality-spec.md` | `figure-03-is-vs-equality-placeholder.svg` | 2.8節「`is`と`==`——そして小さいintのキャッシュ」末尾 | `==`（値の等価性・別々の箱でも成立）と`is`（同一性・同じ箱かどうか）を対比し、小さいintキャッシュを実装詳細として注記する |
| 図2-4 | `figure-04-shallow-deep-copy-spec.md` | `figure-04-shallow-deep-copy-placeholder.svg` | 2.9節「不変は『浅い』——tupleと、浅いコピー・深いコピー」の出力直後 | original・shallow・deepの3列で、浅いコピーが内側のlistを共有し深いコピーが複製して独立させる構造を示す |

## 未実施の確認事項（本番画像差し替え後に必ず実施）

- `.claude/CRAP.md`（対比・反復・整列・近接）に基づく本番画像のレビュー
  （本ドキュメントでは仕様段階のレビュー観点のみ記録済み。本番画像そのものの
  レビューは画像が生成され次第あらためて実施する）。
- グレースケール変換時に、色のみに意味を持たせている箇所がないことの確認
  （requirements.md T-6 #10）。
- E Ink実機（Kindle Previewer）での可読性確認は、デモ版の方針
  （requirements.md 6節）に従い簡易確認にとどめる。
