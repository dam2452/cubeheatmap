"""cubeheatmap.presets — domain-specific helpers for building heatmaps.

Each submodule provides parsers and builders that produce
:class:`~cubeheatmap.CubeHeatmap` objects for a specific data domain.
"""

from . import citations
from . import dependencies
from . import pipeline
from . import webgraph
from . import social
