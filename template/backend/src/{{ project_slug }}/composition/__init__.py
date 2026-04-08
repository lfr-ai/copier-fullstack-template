"""Composition root -- wires concrete adapters to core port interfaces.

This is the outermost layer in clean architecture: the single place
where concrete classes are selected and injected.  No other layer
should reference this package except the application entry point.
"""

