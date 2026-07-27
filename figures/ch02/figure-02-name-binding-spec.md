# 図2-2 仕様書：名前はラベル、代入はラベルの貼り替え

## 1. 用途と配置

- **用途：** 本文中の図解（表紙ではない）。
- **配置：** `manuscript/02-object-model.md` 2.6節「代入は名前の束縛である」の
  末尾、累算代入（`+=`）の説明が終わった直後・節の区切り線（`---`）の直前に、
  単独ブロックとして配置する（requirements.md T-6 #8：図版が本文の左右の
  位置関係に意味を持たせない形で単独ブロック配置されていること）。
- **対応する本文コード：** `bind_same_list_to_three_names`（連鎖代入）・
  `increment_and_track_identity`／`append_and_track_identity`（累算代入）。

## 2. 目的（この図で何を伝えたいか）

2.6節は「代入は値のコピーではなく名前の束縛である」という、本章全体
（2.11節の結論）の中核を最初に具体例で示す節である。文章だけでは
「同じオブジェクトを指す3つの名札」「不変オブジェクトへの`+=`は
再束縛、可変オブジェクトへの`+=`はその場での変更」という2つの事実を
一度に飲み込みにくい。この図は、変数を「値を格納する箱」ではなく
「オブジェクトに貼るラベル」として描き直すことで、連鎖代入と累算代入の
両方が同じ1つの規則（名前はラベル、代入はラベルの貼り替え）から
説明できることを視覚的に示す。

## 3. 対象読者

`requirements.md` 2.1節のペルソナ全員。とくにC・Java・Go・Rustのように
変数を「型付きのメモリ領域」として学んだP1（Java/C#）・P4（Go/Rust）に
効果が大きい。

## 4. 構図（AI画像生成用の指示）

2枚のパネルを左右に並べる（比較図であり、左右の位置関係自体に意味を
持たせるのではなく、1つの図の中の2つの独立した具体例として扱う）。

- **左パネル「連鎖代入」：** `a`・`b`・`c`という3枚のラベル（タグ形状）が、
  1つの箱（リストを表す角丸長方形、中身に`1`のトークンが1つ）から伸びる
  3本の線でそれぞれ接続される。ラベルは箱の外側に配置し、「箱の中に名前が
  入っている」ように見えないようにする（変数は値の容器ではない、という
  誤解を図自体が助長しないため）。
- **右パネル「累算代入」：** 上下2段構成。
  - 上段（不変・int）：`value`ラベルが「10」の箱を指している状態から、
    矢印で「11」という**新しい**箱を指す状態へ遷移する2コマ。元の「10」の
    箱は後段に残るが、ラベルはもうそこを指していないことを示す（バツ印や
    薄い破線で「もう参照されていない」ことを表現）。
  - 下段（可変・list）：`items`ラベルが指す箱は1つのまま変わらず、箱の
    **中身**が「[1, 2]」から「[1, 2, 3]」に書き換わる2コマ（箱自体の位置・
    形は変えず、中のトークンだけが増える）。
- 2コマの遷移は左→右の矢印で表現し、「時間の経過」であることを明示する。
- スタイル：フラットなベクターインフォグラフィック。線画中心、写実表現は
  避ける。装飾アイコンを使う場合はFontAwesomeのような細線・単色のライン
  アイコン様式に限定し、絵文字調は使用しない。
- 文字要素（ラベル名・値）は生成後にレイアウトソフトで差し替え可能なよう、
  配置位置を明確に空けておく。

## 5. グレースケール対応（重要）

- 「新しい箱」と「もう参照されていない元の箱」は色ではなく、実線と破線
  （もしくは網掛けの有無）で区別する（requirements.md T-6 #10）。
- 不変（int）パネルと可変（list）パネルは、箱の角の丸み（int＝角丸なし、
  list＝角丸あり等）のような形状差でも区別できるようにし、色だけに依存
  しない。
- ラベル（タグ）と箱は同一の線幅・同一のフォントで統一する。

## 6. AI画像生成プロンプト（記録用・実行はこのリポジトリの作業環境では未実施）

```
A flat vector infographic, black and white line-art friendly (must remain
legible when converted to grayscale), for a programming book chapter
explaining that in Python, variables are labels attached to objects, not
boxes that store values. Two side-by-side panels on one image.

Left panel, titled "chained assignment": three small tag-shaped labels
named a, b, c, each connected by a thin line to ONE rounded-rectangle box
containing a single token "1" (representing a shared list). The labels sit
outside the box, never inside it, to avoid implying variables are
containers.

Right panel, titled "augmented assignment", split into two rows shown as a
two-step left-to-right sequence (small arrow between step 1 and step 2):
- Top row (immutable int): a label "value" points to a box "10" in step 1;
  in step 2 the same label now points to a NEW box "11" drawn elsewhere,
  while the old box "10" remains but is marked as no longer referenced
  (dashed outline, faint hatching, no color reliance).
- Bottom row (mutable list): a label "items" points to one box in step 1
  containing "[1, 2]"; in step 2 the SAME box (unchanged position, solid
  outline) now contains "[1, 2, 3]" — only the content token changed, the
  box identity did not.

Distinguish "new/no-longer-referenced" boxes from "same box, changed
content" using line style (solid vs dashed) and shape cues, not color, so
the distinction survives grayscale conversion. No photorealistic people,
no colorful cartoon/emoji-style icons; if icons are used, keep them thin
line-icons in a FontAwesome-like monochrome style. Leave clear open space
near each label and box for text to be added separately. Landscape
orientation, suitable for a reflowable EPUB figure (bold enough line
weights to survive downscaling on e-readers).
```

## 7. キャプション（本文掲載用）

> 図2-2　変数は値を格納する箱ではなく、オブジェクトに貼るラベルである。
> 連鎖代入は1つの箱に3枚のラベルを同時に貼る操作であり、累算代入は
> 対象が不変か可変かでラベルの貼り替え（再束縛）か箱の中身の書き換え
> （その場での変更）かに分かれる。

## 8. CRAPレビュー（仕様段階）

| 観点 | 確認内容 | 判定 |
|---|---|---|
| 対比（Contrast） | 「新しい箱」と「同じ箱・中身だけ変化」が線種・配置ではっきり区別されているか | 仕様に明記済み。本番画像生成後に再確認 |
| 反復（Repetition） | ラベル（タグ）の形状・箱の角丸ルールが左右パネルで一貫しているか | 仕様に明記済み。本番画像生成後に再確認 |
| 整列（Alignment） | 左パネル（連鎖代入）と右パネル（累算代入の2段）が同じ基準線・同じ幅で整列しているか | 仕様に明記済み。本番画像生成後に再確認 |
| 近接（Proximity） | ラベルとそれが指す箱の距離が、無関係な要素との距離より明確に近いか | 仕様に明記済み。本番画像生成後に再確認 |

## 9. ファイル仕様（本番画像）

- 形式：PNG（またはJPEG）。EPUB配信コスト対策のため圧縮・解像度最適化を
  ビルド時に行う（requirements.md T-6 #12）。
- 比率：横長（例：16:9〜4:3程度）。Kindleリフロー型のため左右位置に
  意味を持たせない前提で、単独ブロックとして中央配置する。
- ファイル名：`figure-02-name-binding.png`（プレースホルダーと同名の
  拡張子違いに置き換える）。
