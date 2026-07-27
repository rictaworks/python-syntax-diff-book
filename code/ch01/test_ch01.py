"""第1章「他言語との差分マップ」掲載コードリストの検証テスト。

各テストは本文の実行ログと一致する出力・例外だけを確認する。
"""
import pytest
from list_01_indent_error import (
    build_mis_indented_source,
    compile_snippet,
)
from list_02_truthy_none import classify_truthiness
from list_03_assignment_binding import append_and_share
from list_04_type_hint_not_enforced import add
from list_05_list_comprehension import squares_under
from list_06_for_else import find_first_negative
from list_07_self_and_instance_dict import Counter
from list_08_eafp_key_error import price_or_default


def test_mis_indented_block_raises_indentation_error():
    source = build_mis_indented_source()
    with pytest.raises(IndentationError) as exc_info:
        compile_snippet(source)
    expected = "unindent does not match any outer"
    assert expected in str(exc_info.value)


def test_classify_truthiness_treats_zero_empty_and_none_as_false():
    values = [0, "", [], None, 1, "a", [0]]
    assert classify_truthiness(values) == [
        False,
        False,
        False,
        False,
        True,
        True,
        True,
    ]


def test_none_is_singleton_and_not_equal_to_false():
    assert (None is None) is True
    assert (None == False) is False  # noqa: E711,E712


def test_append_and_share_mutates_through_both_names():
    origin = [1, 2]
    alias = origin
    result = append_and_share(alias, 3)
    assert origin == [1, 2, 3]
    assert alias == [1, 2, 3]
    assert result is origin
    assert alias is origin


def test_type_hint_is_not_enforced_at_runtime():
    assert add("foo", "bar") == "foobar"
    assert add.__annotations__ == {
        "a": int,
        "b": int,
        "return": int,
    }


def test_list_comprehension_builds_squares_in_one_line():
    assert squares_under(5) == [0, 1, 4, 9, 16]


def test_for_else_runs_else_only_without_break():
    assert find_first_negative([1, 2, 3]) == "no negative value"
    assert find_first_negative([1, -2, 3]) == "found: -2"


def test_self_is_explicit_and_attributes_live_in_dict():
    counter = Counter(10)
    counter.bump()
    assert counter.__dict__ == {"value": 11}


def test_eafp_tries_first_and_handles_key_error():
    prices = {"apple": 100}
    assert price_or_default(prices, "apple") == 100
    assert price_or_default(prices, "banana") == 0


def test_second_import_reuses_cached_module_without_rerun():
    import list_09_import_runs_once as first
    import list_09_import_runs_once as second

    assert second is first
    assert second.import_log == ["executed"]
