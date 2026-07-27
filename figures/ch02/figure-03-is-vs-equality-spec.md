# 図2-3 仕様書：`is`と`==`——同一性と等価性の違い

## 1. 用途と配置

- **用途：** 本文中の図解（表紙ではない）。
- **配置：** `manuscript/02-object-model.md` 2.8節「`is`と`==`——そして
  小さいintのキャッシュ」の末尾、`AlwaysEqual`クラスの`pycon`出力ブロック
  （`left == right` → `True`、`left is right` → `False`）の直後、節の
  区切り線（`---`）の直前に、単独ブロックとして配置する
  （requirements.md T-6 #8）。
- **対応する本文コード：** `create_two_ints_via_separate_compilations`
  （小さいintのキャッシュ）・`AlwaysEqual`（`__eq__`の独自定義）。

## 2. 目的（この図で何を伝えたいか）

2.8節は「`==`は値が等しいか、`is`は同一のオブジェクトかを尋ねる」という
原則に加え、（a）CPythonの小さいintキャッシュという実装詳細による例外的な
`True`、（b）`__eq__`の独自定義によって`==`と`is`が乖離する例、という2つの
具体例を扱う。文章だけでは「`==`と`is`は独立した別の質問である」という
結論が、intのキャッシュという例外的な挙動の陰に隠れてしまいやすい。この図は
「同じ箱を指しているか（is）」と「箱の中身が等しいか（==）」を空間的に
分けて描くことで、2つの問いが独立していることを一目で示し、小さいintの
キャッシュはあくまで例外的な実装詳細であることを注記する。

## 3. 対象読者

`requirements.md` 2.1節のペルソナ全員。とくに`if (x = 5)`のような式と
文の混同や、値の同一性チェックの習慣が異なるP2（JavaScript/TypeScript）に
効果が大きい（2.10節の対応表でP2の最初の注目節として2.8を指定済み）。

## 4. 構図（AI画像生成用の指示）

2枚のパネルを上下または左右に並べる。

- **パネルA「`==`（値の等価性）」：** 2つの独立した箱（別々の位置に描画、
  それぞれ矢印の先端が独立していることを明示）が、それぞれ同じ内容
  （例：`AlwaysEqual`のインスタンスを表す共通の模様、または`200`という
  トークン）を持つ。2つの箱の間に「`==`」の記号と「True」の結果を示す
  接続線を引く。箱そのものは別々のままであることを明示するため、2つの箱
  の輪郭・位置は明確に離す。
- **パネルB「`is`（同一性）」：** 2つのケースを並べる。
  - ケース1：1つの箱に2本の矢印（ラベル`a`・`b`相当、または`left`・`right`
    に相当する2つの参照点）が刺さり、「同じ箱」であることを強調する
    枠線や二重の矢印起点で表現。結果は「True」。
  - ケース2：パネルAと同じく独立した2つの箱に、それぞれ1本ずつ矢印が
    刺さる。結果は「False」。
- パネルBの下（または脇）に、注記ボックスとして「CPythonの実装詳細：
  -5〜256の整数はキャッシュされ、独立した場所で生成しても`is`が`True`に
  なることがある（言語仕様ではない）」という趣旨のテキストを入れる余地を
  空けておく。注記であることが視覚的に分かるよう、破線の枠で囲むなど
  本文の判定図と区別する。
- スタイル：フラットなベクターインフォグラフィック。線画中心、写実表現は
  避ける。装飾アイコンを使う場合はFontAwesomeのような細線・単色のライン
  アイコン様式に限定し、絵文字調は使用しない。

## 5. グレースケール対応（重要）

- 「同じ箱」と「別々の箱（内容だけ同じ）」は、色ではなく箱の輪郭線の太さ
  ・二重線の有無で区別する（requirements.md T-6 #10）。
- 注記ボックス（実装詳細の注意書き）は破線の枠、本体の判定結果ボックスは
  実線の枠、というように線種で役割を区別する。
- 「True」「False」の結果ラベルは必ず文字で明記し、色（緑＝True／赤＝
  False等）だけに依存しない。

## 6. AI画像生成プロンプト（記録用・実行はこのリポジトリの作業環境では未実施）

```
A flat vector infographic, black and white line-art friendly (must remain
legible when converted to grayscale), for a programming book chapter
explaining the difference between Python's == (equality) and is
(identity) operators. Two stacked panels on one image.

Panel A, titled "== (equality)": two clearly SEPARATE boxes drawn apart
from each other, each containing the same visual token/pattern
(representing equal values or equal-by-__eq__ objects), connected by a
line labeled "==" with a result label "True". The separation of the two
boxes must be visually unambiguous — they are two different objects that
merely compare equal.

Panel B, titled "is (identity)": two side-by-side cases.
- Case 1: ONE single box with two arrows pointing into it from two
  reference points labeled like variable names, with a result label
  "True" — emphasize this is the SAME box via a bold or double outline.
- Case 2: two clearly separate boxes (same style as Panel A), each with
  one arrow from one reference point, result label "False".

Below Panel B, leave a distinct dashed-outline note box (visually
different from the solid-outline result boxes above) for an annotation
about a CPython implementation detail: small integers from -5 to 256 are
cached, so is can unexpectedly return True for them even when created
independently — text to be added separately, just leave the space and the
dashed frame.

Distinguish "same box" from "separate boxes" using outline weight/double
line, not color. Distinguish the note box from result boxes using dashed
vs solid outlines, not color. Always label True/False results with text,
not color alone. No photorealistic people, no colorful cartoon/emoji-style
icons; if icons are used, keep them thin line-icons in a FontAwesome-like
monochrome style. Landscape or portrait orientation acceptable, suitable
for a reflowable EPUB figure (bold enough line weights to survive
downscaling on e-readers).
```

## 7. キャプション（本文掲載用）

> 図2-3　`==`は「箱の中身が等しいか」を、`is`は「同じ箱を指しているか」を
> 尋ねる、独立した2つの質問である。CPythonの小さいintキャッシュは
> `is`が`True`になる例外的な実装詳細であり、言語仕様として保証された
> 挙動ではない。

## 8. CRAPレビュー（仕様段階）

| 観点 | 確認内容 | 判定 |
|---|---|---|
| 対比（Contrast） | 「同じ箱（二重線）」と「別々の箱（単線）」の差、注記の破線枠と結果の実線枠の差が明確か | 仕様に明記済み。本番画像生成後に再確認 |
| 反復（Repetition） | パネルA・パネルBの箱の描き方（サイズ・線幅）が共通ルールで統一されているか | 仕様に明記済み。本番画像生成後に再確認 |
| 整列（Alignment） | パネルAとパネルBが同じ幅・同じ基準線で上下に整列しているか | 仕様に明記済み。本番画像生成後に再確認 |
| 近接（Proximity） | 結果ラベル（True/False）が対応する箱・接続線のすぐ近くに配置されているか | 仕様に明記済み。本番画像生成後に再確認 |

## 9. ファイル仕様（本番画像）

- 形式：PNG（またはJPEG）。EPUB配信コスト対策のため圧縮・解像度最適化を
  ビルド時に行う（requirements.md T-6 #12）。
- 比率：横長〜正方形。Kindleリフロー型のため左右位置に意味を持たせない
  前提で、単独ブロックとして中央配置する。
- ファイル名：`figure-03-is-vs-equality.png`（プレースホルダーと同名の
  拡張子違いに置き換える）。
