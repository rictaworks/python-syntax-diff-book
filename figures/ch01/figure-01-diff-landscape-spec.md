# 図1-1 仕様書：他言語出身者の躓きポイント地図

## 1. 用途と配置

- **用途：** 本文中の図解（表紙ではない）。
- **配置：** `manuscript/01-diff-map.md` 1.2節「12の差分マップ」の表の直後に、
  単独ブロックとして配置する（requirements.md T-6 #8：図版が本文の左右の
  位置関係に意味を持たせない形で単独ブロック配置されていること）。
- **対応する本文表：** 1.2節の12項目の表（# 1〜12、差分の核心、参照章）。

## 2. 目的（この図で何を伝えたいか）

1.2節の表はすでに12の差分と参照章を文字で列挙しているが、初読の読者
（他言語経験者）が「自分に関係が深い差分はどれか」を1分以内に直感的に
把握できるようにする。表を置き換えるのではなく、表の情報を地図の比喩で
視覚的に要約する補助図とする。

## 3. 対象読者

`requirements.md` 2.1節のペルソナ全員（P1: Java/C#、P2: JS/TS、
P3: Ruby/PHP、P4: Go/Rust）。P0（未経験者）は対象外。

## 4. 構図（AI画像生成用の指示）

- 全体は「地図」または「地形図」の比喩。中央に1本の道（Pythonの学習パス）
  があり、道沿いに12個の地点（waypoint）が並ぶ。各地点には1〜12の番号を
  大きく振る（1.2節の表の#列と対応させる）。
- 道の脇から4本の支線が伸び、それぞれJava/C#・JavaScript/TypeScript・
  Ruby/PHP・Go/Rustの4つの前提言語グループを表す。各支線は、その言語
  グループが最初に合流する地点（1.8節の対応表：P1→#1・#7・#8、
  P2→#2・#3・#11、P3→#1・#4、P4→#2・#9）に接続する。
- スタイル：フラットなベクターインフォグラフィック。線画中心で、
  写実的な人物・写真的表現は避ける。装飾アイコンを使う場合は
  FontAwesomeのような細線・単色のラインアイコン様式に限定し、
  絵文字調（カラフルな丸みを帯びたキャラクター的表現）は使用しない。
- 文字要素（章番号・言語グループ名）は生成後にレイアウトソフトで
  差し替え可能なよう、ラベル位置を明確に空けておく。

## 5. グレースケール対応（重要）

- 4本の支線は色だけで区別せず、線種（実線・破線・点線・一点鎖線）でも
  区別できるようにする（requirements.md T-6 #10、E Inkはグレースケール
  表示のため）。
- 12個の地点は同一の図形（円）・同一サイズで統一し、番号の可読性を
  白黒反転でも確保する。

## 6. AI画像生成プロンプト（記録用・実行はこのリポジトリの作業環境では未実施）

```
A flat vector infographic in the style of a simple trail map, black and
white line-art friendly (must remain legible when converted to
grayscale), for a programming book chapter introducing 12 syntax
differences between Python and other languages (Java/C#, JavaScript/
TypeScript, Ruby/PHP, Go/Rust) to experienced programmers switching to
Python. One central path with 12 numbered waypoints (circles labeled 1
to 12) in a single row. Four side trails branch off toward the path,
each using a visually distinct line pattern (solid, dashed, dotted,
dash-dot) rather than color alone, so the four language groups remain
distinguishable in grayscale. No photorealistic people, no colorful
cartoon/emoji-style icons; if icons are used, keep them thin
line-icons in a FontAwesome-like monochrome style. Leave clear open
space near each waypoint and trail label for text to be added
separately. Landscape orientation, suitable for a reflowable EPUB
figure (will be scaled down on e-readers, so keep line weights bold
enough to survive downscaling).
```

## 7. キャプション（本文掲載用）

> 図1-1　4つの前提言語グループが、Pythonの12の差分ポイントのどこで
> 最初に合流するかを示した地図。番号は1.2節の表の#列に対応する。

## 8. CRAPレビュー（仕様段階）

| 観点 | 確認内容 | 判定 |
|---|---|---|
| 対比（Contrast） | 12個の地点番号が背景・道より視覚的に強調されているか（太字円・十分なサイズ） | 仕様に明記済み。本番画像生成後に再確認 |
| 反復（Repetition） | 12地点すべてが同一の図形・同一サイズ・同一の番号フォントで統一されているか | 仕様に明記済み。本番画像生成後に再確認 |
| 整列（Alignment） | 12地点が1本の道沿いに一直線または単一グリッドに整列し、散らばって配置されていないか | 仕様に明記済み。本番画像生成後に再確認 |
| 近接（Proximity） | 各支線のラベル（言語グループ名）が、その支線が合流する地点の近くに配置されているか | 仕様に明記済み。本番画像生成後に再確認 |

## 9. ファイル仕様（本番画像）

- 形式：PNG（またはJPEG）。EPUB配信コスト対策のため圧縮・解像度最適化を
  ビルド時に行う（requirements.md T-6 #12）。
- 比率：横長（例：16:9〜4:3程度）。Kindleリフロー型のため左右位置に
  意味を持たせない前提で、単独ブロックとして中央配置する。
- ファイル名：`figure-01-diff-landscape.png`（プレースホルダーと同名の
  拡張子違いに置き換える）。
