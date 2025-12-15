"""
Living Glossary Module

Single source of truth for DDJ character analysis.
Supports dual-hypothesis tracking (standard vs. agricultural decompositions),
full version history, and integration with CHUBS validation.
"""

from .manager import GlossaryManager

__all__ = ['GlossaryManager']
