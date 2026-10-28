"""Canonicalization of JAM strings for duplicate detection."""

from .canonical import (
    generate_group,
    canonical_key,
    canonical_key_fast,
    filter_duplicates,
    rot, transp, flip, sign,
    sort_cols,
    elements_S3,
    array_to_chain,
    chain_to_array,
)

__all__ = [
    "generate_group",
    "canonical_key",
    "canonical_key_fast",
    "filter_duplicates",
    "rot", "transp", "flip", "sign",
    "sort_cols",
    "elements_S3",
    "array_to_chain",
    "chain_to_array",
]

from .options import rows_for_option, base_sets_for_option, base_tokens_for_option
__all__ = [..., "rows_for_option", "base_sets_for_option", "base_tokens_for_option"]

__version__ = "1.2.0"
