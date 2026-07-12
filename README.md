# K1.hardware

Agent-driven KiCad and PCB automation for K1-Lightwave hardware.

This repository contains public tooling, MCP servers, reference material, and prototype automation used around the K1-Lightwave hardware workflow. Product PCB files, fabrication outputs, BOMs, and private design documents are not published in the public HEAD of this repository.

> [!NOTE]
> This public surface is being cleaned up for transfer into the SpectraSynq organisation. Some legacy prototype tooling is preserved for reference, but it should not be treated as a stable package API until it is extracted into a dedicated tool repository.

## Quickstart

```bash
git clone https://github.com/synqing/K1.hardware.git
cd K1.hardware
python3 mcp/verify-servers.py
python3 mcp/test_rag.py
```

For Claude Code MCP setup, run:

```bash
python3 mcp/configure_claude.py
```

Some integrations need your own API credentials. See [SETUP_CREDENTIALS.md](docs/internal/legacy-root/SETUP_CREDENTIALS.md) for provider setup notes.

## What is here

- **MCP servers** in [mcp/](mcp/) for KiCad CLI automation, KiKit, KiBot, SKiDL, FreeRouting, component sourcing, fab operations, and local RAG.
- **Agent modules** in [agent/](agent/) for DFM checks, KiCad helpers, routing, impedance, thermal modelling, and orchestration.
- **Tool prototypes** in [tools/](tools/), including the KiCad footprint hunter and the preserved Elite PCB Designer prototype.
- **Reference docs** in [docs/](docs/) for public tooling notes, vendor references, datasheets, and legacy implementation notes.

## Repository layout

```text
K1.hardware/
|-- agent/                         Python modules for PCB automation workflows
|-- docs/                          Public references and legacy notes
|-- mcp/                           MCP servers used by agent-driven EDA workflows
|-- plugins/                       KiCad plugin experiments
|-- tools/
|   |-- elite-pcb-designer/        Prototype routing, placement, and validation tooling
|   `-- kicad-footprint-hunter/    Footprint discovery and board update utilities
|-- .github/                       Workflow definitions retained for review
|-- .gitignore
|-- LICENSE
`-- README.md
```

## Working with the tools

Use [mcp/verify-servers.py](mcp/verify-servers.py) to check local dependencies and MCP server availability. Use [mcp/test_rag.py](mcp/test_rag.py) to confirm the local RAG index can answer tooling queries.

The legacy Elite PCB Designer prototype now lives under [tools/elite-pcb-designer/legacy-pipeline/](tools/elite-pcb-designer/legacy-pipeline/). Run those scripts from that directory, and expect to provide your own KiCad input files.

## Community and support

- [Issues](../../issues) for bugs, cleanup findings, and extraction candidates.
- [Discord](https://discord.gg/8y8rXegU8j) for SpectraSynq build discussion.

## Licence

Code is licensed under Apache-2.0; see [LICENSE](LICENSE). Documentation is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) unless a source document states otherwise.
