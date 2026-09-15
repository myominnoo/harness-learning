#!/usr/bin/env python3
"""Verification utilities for agent outputs."""

import re


def verify_response(response: str, expected_keywords: list) -> bool:
    """Verify the response contains expected keywords."""
    response_lower = response.lower()
    return all(keyword.lower() in response_lower for keyword in expected_keywords)


def verify_tokens(context: str, max_tokens: int) -> bool:
    """Verify context is within token limit."""
    # Rough estimate: 1 token ≈ 4 characters
    return len(context) < max_tokens * 4


def main():
    """Run verification tests."""
    test_context = "This is a test context with some tokens."
    result = verify_tokens(test_context, 16384)
    print(f"Token verification: {result}")


if __name__ == "__main__":
    main()
