# 図1-2 仕様書：読者タイプ別の推奨ルート（トレイルマップ）

## 1. 用途と配置

- **用途：** 本文中の図解（表紙ではない）。
- **配置：** `manuscript/01-diff-map.md` 1.8節「読者タイプ別の読み進め方」の
  2つの表（動機→推奨ルート表、ID→前提言語→最初に見るべき番号表）の直後に、
  単独ブロックとして配置する（requirements.md T-6 #8）。
- **対応する本文表：** 1.8節の2つの表。

## 2. 目的（この図で何を伝えたいか）

1.8節はすでに「動機別の推奨ルート」と「ペルソナ別の最初に見るべき番号」を
2つの表で示しているが、両者は別々の表であるため、読者が自分のペルソナ
（P1〜P4）から実際の章の並び順を1つの視覚的な経路として追いにくい。
本図は両方の情報を1枚の路線図（トレイルマップ）に統合し、「自分はP1だから
2章→5章→7章→6章の順で読めばよい」という到達経路を一目で確認できるように
する。

## 3. 対象読者

`requirements.md` 2.1節のペルソナ全員（P1〜P4）。特に「特定の差分だけを
引きたい」「通読する時間がない」という飛ばし読み志向の読者に有効。

## 4. 構図（AI画像生成用の指示）

- 4本の水平な「路線」（レーン）を上から順にP1・P2・P3・P4として並べる。
- 各路線上に、その読者タイプの推奨ルート（`SPEC/`の読者導線図・
  `requirements.md` 10節の`graph LR`と同じ経路データ）に沿って、
  章番号を書いた駅（ストップ）を順番に配置する。
  - P1: 1章→2章→5章→7章→6章
  - P2: 1章→2章→3章→10章→6章
  - P3: 1章→2章→3章→9章→5章
  - P4: 1章→2章→8章→6章→7章
- 4本の路線は先頭（1章・2章）で合流し、そこから分岐する「乗換駅」の
  ような構図にする（1章・2章がデモ版収録範囲であることを示唆する）。
- スタイル：フラットなベクターインフォグラフィック。路線図（鉄道路線図）
  の比喩を使うが、実在の路線図・企業ロゴを模倣しない。装飾アイコンを
  使う場合は細線・単色のラインアイコン様式（FontAwesome的な見た目）に
  限定し、絵文字調の表現は使用しない。

## 5. グレースケール対応（重要）

- 4本の路線は色だけで区別せず、線の太さ・線種（実線・破線・点線・
  二重線）でも区別できるようにする（requirements.md T-6 #10）。
- 各路線の左端にP1〜P4のラベルを明記し、色に依存せず路線を識別できる
  ようにする。

## 6. AI画像生成プロンプト（記録用・実行はこのリポジトリの作業環境では未実施）

```
A flat vector infographic in the style of a simple subway/trail route
map, black and white line-art friendly (must remain legible when
converted to grayscale), for a programming book chapter that helps
experienced programmers (four personas: Java/C# background, JavaScript
/TypeScript background, Ruby/PHP background, Go/Rust background) pick a
recommended reading order across book chapters. Four horizontal lanes,
one per persona, each lane a distinct line style (solid, dashed,
dotted, double-line) rather than relying on color alone. All four
lanes converge at a shared starting interchange representing the first
two chapters, then branch into different chapter sequences. Chapter
numbers are shown as labeled stops along each lane. No photorealistic
people, no real transit-system branding, no colorful cartoon/emoji-
style icons; if icons are used, keep them thin line-icons in a
FontAwesome-like monochrome style. Leave clear open space for text
labels to be added separately. Landscape orientation, suitable for a
reflowable EPUB figure, bold enough line weights to survive downscaling
on e-readers.
```

## 7. キャプション（本文掲載用）

> 図1-2　読者タイプ（P1〜P4）別の推奨章ルートを路線図として統合した図。
> 1章・2章で合流したのち、動機に応じて経路が分岐する。

## 8. CRAPレビュー（仕様段階）

| 観点 | 確認内容 | 判定 |
|---|---|---|
| 対比（Contrast） | 現在地（1章・2章、デモ版収録範囲）と、その先の未収録章が視覚的に区別されているか | 仕様に明記済み。本番画像生成後に再確認 |
| 反復（Repetition） | 4本の路線すべてが同じ「駅」の図形・同じラベル配置ルールで統一されているか | 仕様に明記済み。本番画像生成後に再確認 |
| 整列（Alignment） | 4本の路線が水平に整列し、駅の位置が縦方向にもグリッドに沿っているか | 仕様に明記済み。本番画像生成後に再確認 |
| 近接（Proximity） | 各路線のP1〜P4ラベルが、対応する路線の起点に近接して配置されているか | 仕様に明記済み。本番画像生成後に再確認 |

## 9. ファイル仕様（本番画像）

- 形式：PNG（またはJPEG）。EPUB配信コスト対策のため圧縮・解像度最適化を
  ビルド時に行う（requirements.md T-6 #12）。
- 比率：横長。単独ブロックとして中央配置する。
- ファイル名：`figure-02-reader-routes.png`（プレースホルダーと同名の
  拡張子違いに置き換える）。
