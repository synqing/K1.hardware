# MCP servers

This folder carries MCP servers that still live inside `K1.hardware`.

Extracted servers move to standalone SpectraSynq repositories and become canonical there. The monorepo should consume those extracted servers by repository reference rather than keeping a second editable copy.

Current extraction:

- `mcp/mcp-lcsc` -> `https://github.com/SpectraSynq/mcp-lcsc`

