# 図2-1 仕様書：真偽判定プロトコル（`__bool__`／`__len__`）の判定フロー

## 1. 用途と配置

- **用途：** 本文中の図解（表紙ではない）。
- **配置：** `manuscript/02-object-model.md` 2.4節「真偽判定は`__bool__`・
  `__len__`のプロトコルに従う」の`pycon`出力ブロック（`SizedContainer`・
  `AlwaysTruthy`の実行結果）の直後、「Javaの`if (obj != null)`や
  C#の同種の書き方に慣れていると」で始まる段落の直前に、単独ブロックとして
  配置する（requirements.md T-6 #8）。
- **対応する本文コード：** `SizedContainer`・`AlwaysTruthy`と、
  `bool(SizedContainer(0))`等の実行結果。

## 2. 目的（この図で何を伝えたいか）

2.4節の文章は「`__bool__`を探し、なければ`__len__`を探し、どちらもなければ
常に`True`」という判定手順を1文で説明しているが、他言語の「`null`か
どうかだけを見る」単純な規則に慣れた読者には、手順が線形の文章のままだと
記憶に残りにくい。この図は`if obj:`が評価される瞬間の判定手順を
フローチャートとして視覚化し、「特別なハードコードではなくプロトコルに
従っている」ことを、分岐の形で一目で追えるようにする。

## 3. 対象読者

`requirements.md` 2.1節のペルソナ全員。とくに「参照が`null`でなければ真」
という単純な規則に慣れているP1（Java/C#）に効果が大きい（2.10節の対応表
でもP1の最初の注目節として2.4を指定済み）。

## 4. 構図（AI画像生成用の指示）

- 標準的なフローチャート（開始ノード→判定ノード（ひし形）→終了ノード
  （角丸長方形）の組み合わせ）。上から下へ流れる縦方向のレイアウト。
- ノード構成：
  1. 開始：「`if obj:` が評価される」
  2. 判定1（ひし形）：「`obj.__bool__()` は定義されているか？」
     - Yes → 終了ノード「その戻り値（`True`/`False`）を採用」
     - No → 判定2へ
  3. 判定2（ひし形）：「`obj.__len__()` は定義されているか？」
     - Yes → 判定3へ
     - No → 終了ノード「常に`True`」
  4. 判定3（ひし形）：「`len(obj) == 0` か？」
     - Yes → 終了ノード「`False`」
     - No → 終了ノード「`True`」
- 各終了ノードの右側（または下側の余白）に、本文コード例のどの呼び出しが
  その経路を通るかの対応例を小さく添える余地を空けておく（例：
  `SizedContainer(0)` → 判定1No・判定2Yes・判定3Yes経路、
  `AlwaysTruthy()` → 判定1No・判定2No経路）。これは生成後にレイアウト
  ソフトでテキストを差し替える前提の空白でよい。
- スタイル：フラットなベクターインフォグラフィック。線画中心、写実表現は
  避ける。装飾アイコンを使う場合はFontAwesomeのような細線・単色のライン
  アイコン様式に限定し、絵文字調は使用しない。

## 5. グレースケール対応（重要）

- 「Yes」の矢印と「No」の矢印は、色ではなく矢印線の線種（Yes＝実線、
  No＝破線）とラベル文字（「Yes」「No」を必ず併記）の両方で区別する
  （requirements.md T-6 #10）。
- 判定ノード（ひし形）と終了ノード（角丸長方形）は形状そのもので役割が
  区別できるようにし、塗り色の違いだけに依存しない。

## 6. AI画像生成プロンプト（記録用・実行はこのリポジトリの作業環境では未実施）

```
A flat vector flowchart, black and white line-art friendly (must remain
legible when converted to grayscale), for a programming book chapter
explaining Python's truthiness protocol. Top-to-bottom flow with a start
node, three diamond-shaped decision nodes, and rounded-rectangle end
nodes:

1. Start node: "if obj: is evaluated"
2. Decision 1: "Is obj.__bool__() defined?" -> Yes goes to an end node
   "use its return value (True/False)"; No continues to Decision 2.
3. Decision 2: "Is obj.__len__() defined?" -> Yes continues to Decision 3;
   No goes to an end node "always True".
4. Decision 3: "Is len(obj) == 0?" -> Yes goes to an end node "False"; No
   goes to an end node "True".

Distinguish "Yes" branches from "No" branches using BOTH a solid arrow
line for Yes and a dashed arrow line for No, plus explicit "Yes"/"No" text
labels on every branch, so the distinction survives grayscale conversion
and does not rely on color alone. Decision nodes are diamonds, end nodes
are rounded rectangles, start node is a plain rectangle or stadium shape —
shape alone should communicate node type. Leave small open space near
each end node for example annotations to be added separately (e.g. which
example object takes which path). No photorealistic people, no colorful
cartoon/emoji-style icons; if icons are used, keep them thin line-icons in
a FontAwesome-like monochrome style. Portrait or square orientation
acceptable given the top-to-bottom flow, suitable for a reflowable EPUB
figure (bold enough line weights to survive downscaling on e-readers).
```

## 7. キャプション（本文掲載用）

> 図2-1　`if obj:`が評価されるときの判定手順。`__bool__`が定義されて
> いればその戻り値を、なければ`__len__`の結果が0かどうかを、どちらも
> なければ常に`True`を採用する。組み込み型の「空なら偽」も、この
> プロトコルの結果にすぎない。

## 8. CRAPレビュー（仕様段階）

| 観点 | 確認内容 | 判定 |
|---|---|---|
| 対比（Contrast） | 判定ノード（ひし形）と終了ノード（角丸長方形）が形状で明確に区別されているか | 仕様に明記済み。本番画像生成後に再確認 |
| 反復（Repetition） | 3つの判定ノードが同一サイズ・同一フォントで統一されているか | 仕様に明記済み。本番画像生成後に再確認 |
| 整列（Alignment） | 上から下への一直線の流れが保たれ、矢印が交差して読みにくくなっていないか | 仕様に明記済み。本番画像生成後に再確認 |
| 近接（Proximity） | Yes／Noラベルが対応する矢印のすぐ近くに配置されているか | 仕様に明記済み。本番画像生成後に再確認 |

## 9. ファイル仕様（本番画像）

- 形式：PNG（またはJPEG）。EPUB配信コスト対策のため圧縮・解像度最適化を
  ビルド時に行う（requirements.md T-6 #12）。
- 比率：縦長〜正方形（フローチャートの流れの都合上、図1-1・図1-2の横長とは
  異なってよい）。Kindleリフロー型のため左右位置に意味を持たせない前提で、
  単独ブロックとして中央配置する。
- ファイル名：`figure-01-truthiness-protocol.png`（プレースホルダーと
  同名の拡張子違いに置き換える）。
