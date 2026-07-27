"""第2章「構文の外形とオブジェクトモデル」掲載コードリストの検証テスト。

各テストは本文の実行ログと一致する出力・例外だけを確認する。
"""
import copy

import pytest
from list_01_tab_space_and_continuation import (
    build_tab_space_mixed_source,
    compile_snippet,
    sum_across_continued_lines,
)
from list_02_assignment_is_not_expression import (
    build_assignment_in_condition_source,
    evaluate_with_walrus,
)
from list_03_truthiness_protocol import AlwaysTruthy, SizedContainer
from list_04_none_identity_and_default import get_none_identity_pair, greet
from list_05_chained_and_augmented_assignment import (
    append_and_track_identity,
    bind_same_list_to_three_names,
    increment_and_track_identity,
)
from list_06_argument_rebind_vs_mutate import mutate_in_place, rebind_only
from list_07_small_int_cache_and_custom_eq import (
    AlwaysEqual,
    create_two_ints_via_separate_compilations,
)
from list_08_tuple_with_mutable_element import (
    append_to_tail,
    build_point_with_mutable_tail,
    reassign_first_element,
)
from list_09_shallow_vs_deep_copy import deep_copy_nested_list, shallow_copy_nested_list


def test_tab_space_mixing_raises_tab_error():
    source = build_tab_space_mixed_source()
    with pytest.raises(TabError) as exc_info:
        compile_snippet(source)
    assert "inconsistent use of tabs and spaces" in str(exc_info.value)


def test_implicit_line_continuation_sums_without_backslash():
    assert sum_across_continued_lines(4, 5, 6) == 15


def test_assignment_inside_condition_is_syntax_error():
    source = build_assignment_in_condition_source()
    with pytest.raises(SyntaxError) as exc_info:
        compile_snippet(source)
    message = str(exc_info.value)
    assert "invalid syntax" in message
    assert "':='" in message


def test_walrus_operator_binds_and_returns_value_in_condition():
    assert evaluate_with_walrus(6) == 12
    assert evaluate_with_walrus(3) is None


def test_len_zero_object_is_falsy_even_without_bool():
    assert bool(SizedContainer(0)) is False
    assert bool(SizedContainer(3)) is True


def test_plain_object_without_len_or_bool_is_always_truthy():
    assert bool(AlwaysTruthy()) is True


def test_none_is_a_stable_singleton():
    first_id, second_id = get_none_identity_pair()
    assert first_id == second_id


def test_default_none_argument_idiom():
    assert greet(None) == "hello, world"
    assert greet("Python") == "hello, Python"


def test_chained_assignment_binds_one_object_to_three_names():
    a, b, c = bind_same_list_to_three_names()
    assert a is b
    assert b is c
    a.append(1)
    assert b == [1]
    assert c == [1]


def test_augmented_assignment_on_int_creates_new_object():
    result, same_object = increment_and_track_identity(10)
    assert result == 11
    assert same_object is False


def test_augmented_assignment_on_list_mutates_same_object():
    result, same_object = append_and_track_identity([1, 2], 3)
    assert result == [1, 2, 3]
    assert same_object is True


def test_rebind_inside_function_does_not_affect_caller():
    x = 5
    assert rebind_only(x) == 6
    assert x == 5


def test_mutate_in_place_is_visible_to_caller():
    items = [1, 2]
    mutate_in_place(items)
    assert items == [1, 2, 99]


def test_small_int_cache_range_is_shared_but_257_is_not():
    cached_a, cached_b = create_two_ints_via_separate_compilations(200)
    assert cached_a is cached_b

    uncached_a, uncached_b = create_two_ints_via_separate_compilations(257)
    assert uncached_a is not uncached_b


def test_custom_eq_can_diverge_from_identity():
    left = AlwaysEqual()
    right = AlwaysEqual()
    assert (left == right) is True
    assert (left is right) is False


def test_tuple_item_assignment_raises_type_error():
    point = build_point_with_mutable_tail()
    with pytest.raises(TypeError) as exc_info:
        reassign_first_element(point, 99)
    assert "does not support item assignment" in str(exc_info.value)


def test_tuple_allows_mutation_of_contained_list():
    point = build_point_with_mutable_tail()
    updated = append_to_tail(point, 4)
    assert updated == (1, [2, 3, 4])


def test_shallow_copy_shares_nested_objects():
    original = [[1, 2], [3, 4]]
    shallow = shallow_copy_nested_list(original)
    original[0].append("shared")
    assert shallow[0] == [1, 2, "shared"]
    assert shallow[0] is original[0]


def test_deep_copy_does_not_share_nested_objects():
    original = [[1, 2], [3, 4]]
    deep = deep_copy_nested_list(original)
    original[0].append("shared")
    assert deep[0] == [1, 2]
    assert deep[0] is not original[0]


def test_stdlib_copy_module_used_directly_matches_helpers():
    original = [[1, 2]]
    assert copy.copy(original)[0] is original[0]
    assert copy.deepcopy(original)[0] is not original[0]
