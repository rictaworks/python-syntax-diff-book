# 図2-4 仕様書：浅いコピーと深いコピーの構造図

## 1. 用途と配置

- **用途：** 本文中の図解（表紙ではない）。
- **配置：** `manuscript/02-object-model.md` 2.9節「不変は『浅い』——
  tupleと、浅いコピー・深いコピー」の`pycon`出力ブロック（`shallow_copy_
  nested_list`・`deep_copy_nested_list`の実行結果）の直後、「`copy.copy()`
  （浅いコピー）は、一番外側のlistだけを新しく作り」で始まる段落の直前に、
  単独ブロックとして配置する（requirements.md T-6 #8）。
- **対応する本文コード：** `shallow_copy_nested_list`・
  `deep_copy_nested_list`と、`original[0].append("shared")`後の
  `shallow[0]`・`deep[0]`の実行結果。

## 2. 目的（この図で何を伝えたいか）

2.9節の`pycon`出力は、`original`に変更を加えた後で`shallow[0]`だけが
変化し`deep[0]`が変化しないことを示すが、これは「なぜそうなるか」を
言葉で説明されて初めて納得できる結果であり、出力だけを見ても構造の違いが
直感的には伝わりにくい。この図は`original`・`shallow`・`deep`の3つの
listを、外側の箱と内側の箱（入れ子のlist）に分けて描き、浅いコピーが
外側の箱だけを複製して内側の箱を**共有**すること、深いコピーが内側の箱
まで複製して**独立**させることを、矢印の共有・非共有として視覚化する。
tupleの「浅い不変性」（1つ目の要素は差し替え不可だが2つ目の要素である
listの中身は変更できる）と同じ「浅さ」の概念であることも、キャプションで
明示的に橋渡しする。

## 3. 対象読者

`requirements.md` 2.1節のペルソナ全員。とくに「不変」「コピー」という
言葉の意味範囲が言語ごとに異なるP1（Java/C#、`null`以外は真という単純な
規則からの類推で誤解しやすい）に効果が大きい（2.10節の対応表でP1の最初の
注目節の1つとして2.9を指定済み）。

## 4. 構図（AI画像生成用の指示）

3つの列を左から右に並べる：「original」「shallow（浅いコピー）」
「deep（深いコピー）」。各列は「外側の箱」（listを表す大きな角丸長方形）
の中に、2つの「内側の箱」（入れ子のlistを表す小さめの角丸長方形、
それぞれ`[1, 2]`・`[3, 4]`に相当するトークンを持つ）への参照を、外側の
箱から内側の箱へ伸びる矢印2本で表す。

- **original列：** 外側の箱1つと、そこから伸びる2本の矢印がそれぞれ
  固有の内側の箱A・Bを指す。
- **shallow列：** 別の（新しい）外側の箱が描かれるが、そこから伸びる2本の
  矢印は、original列の内側の箱A・Bと**同じ箱**を指す（列をまたいで矢印を
  伸ばし、「共有」を明示する。矢印は破線ではなく実線だが、original列と
  shallow列の間で1本にまとまる合流点を描いてもよい）。
- **deep列：** 別の新しい外側の箱と、そこから伸びる2本の矢印が、
  original列とは独立した**新しい**内側の箱A'・B'（内容はA・Bと同じだが
  別個体であることを示すため、破線の輪郭または軽いハッチングで
  「複製」であることを示す）を指す。
- 図の下部に、「originalの内側の箱に変更を加えると」という注記とともに、
  shallow列の対応する内側の箱にも変化が伝播する矢印（点線の波及矢印）を
  加え、deep列には波及しないことを示す「×」または遮断線を添える余地を
  空けておく。
- スタイル：フラットなベクターインフォグラフィック。線画中心、写実表現は
  避ける。装飾アイコンを使う場合はFontAwesomeのような細線・単色のライン
  アイコン様式に限定し、絵文字調は使用しない。

## 5. グレースケール対応（重要）

- 「共有されている内側の箱」（shallow列がoriginal列の箱を指す）と
  「複製された内側の箱」（deep列の新しい箱）は、色ではなく実線／破線＋
  ハッチングの有無で区別する（requirements.md T-6 #10）。
- 波及する変更（shallow列）と遮断される変更（deep列）は、波及矢印の
  有無と「×」記号（文字・記号として明示）で区別し、色だけに依存しない。
- 3列の外側の箱・内側の箱は同一の図形・同一サイズで統一し、列ごとの
  違いは「箱の複製有無」のみで表現する。

## 6. AI画像生成プロンプト（記録用・実行はこのリポジトリの作業環境では未実施）

```
A flat vector infographic, black and white line-art friendly (must remain
legible when converted to grayscale), for a programming book chapter
explaining the difference between Python's shallow copy (copy.copy) and
deep copy (copy.deepcopy) of a nested list. Three columns left to right,
labeled "original", "shallow copy", "deep copy".

Each column shows one large rounded-rectangle outer box (representing the
outer list) with two arrows pointing to two smaller rounded-rectangle
inner boxes (representing two nested lists, holding tokens like "[1, 2]"
and "[3, 4]").

- "original" column: one outer box, two arrows to two unique inner boxes
  A and B.
- "shallow copy" column: a NEW outer box, but its two arrows point to the
  SAME inner boxes A and B from the original column (draw the arrows
  crossing over to the original column's boxes, or show a merge point
  between the two columns, to make the sharing unmistakable).
- "deep copy" column: a NEW outer box AND two brand-new inner boxes A'
  and B' (same content as A and B but drawn as separate boxes, marked
  with a dashed outline or light hatching to indicate "duplicated, not
  shared").

At the bottom, leave space for an annotation: an arrow showing a change
propagating from original's inner box A into shallow copy's box (since
it's the same box), marked with a dotted "ripple" arrow, versus an "X" or
a blocking line showing the change does NOT propagate to deep copy's box
A'.

Distinguish "shared box" from "duplicated box" using solid vs dashed
outline and hatching, not color. Distinguish "change propagates" from
"change is blocked" using an explicit ripple arrow vs an X symbol, not
color alone. All three columns must use the same box shapes and sizes,
differing only in whether boxes are shared or duplicated. No
photorealistic people, no colorful cartoon/emoji-style icons; if icons
are used, keep them thin line-icons in a FontAwesome-like monochrome
style. Landscape orientation, suitable for a reflowable EPUB figure (bold
enough line weights to survive downscaling on e-readers).
```

## 7. キャプション（本文掲載用）

> 図2-4　`copy.copy()`（浅いコピー）は外側のlistだけを複製し、内側の
> listは元のオブジェクトと共有される。`copy.deepcopy()`（深いコピー）
> は内側のlistまで再帰的に複製し、元との共有を断ち切る。tupleの要素は
> 差し替えられないが要素自身の中身は変更できるという「浅い不変性」
> （2.9節前半）と、根っこにある考え方は同じである。

## 8. CRAPレビュー（仕様段階）

| 観点 | 確認内容 | 判定 |
|---|---|---|
| 対比（Contrast） | 「共有された箱（実線・合流矢印）」と「複製された箱（破線・ハッチング）」の差が一目で分かるか | 仕様に明記済み。本番画像生成後に再確認 |
| 反復（Repetition） | 3列すべての外側・内側の箱が同一の図形・サイズで統一されているか | 仕様に明記済み。本番画像生成後に再確認 |
| 整列（Alignment） | 3列が同じ基準線・同じ間隔で横に整列しているか | 仕様に明記済み。本番画像生成後に再確認 |
| 近接（Proximity） | 波及矢印・遮断記号が対応する列の箱のすぐ近くに配置されているか | 仕様に明記済み。本番画像生成後に再確認 |

## 9. ファイル仕様（本番画像）

- 形式：PNG（またはJPEG）。EPUB配信コスト対策のため圧縮・解像度最適化を
  ビルド時に行う（requirements.md T-6 #12）。
- 比率：横長（例：16:9〜4:3程度、3列構成のため横長が扱いやすい）。
  Kindleリフロー型のため左右位置に意味を持たせない前提で、単独ブロック
  として中央配置する。
- ファイル名：`figure-04-shallow-deep-copy.png`（プレースホルダーと
  同名の拡張子違いに置き換える）。
