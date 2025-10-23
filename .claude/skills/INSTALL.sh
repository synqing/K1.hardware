#!/bin/bash
# Claude Code Skills Installation Script for PRISM.unified
# Date: 2025-10-22
# This script documents external plugin installations
# (Actual installation happens via Claude Code commands, not bash)

set -e

echo "════════════════════════════════════════════════════════════"
echo "  PRISM.unified - Claude Code Skills Installation"
echo "════════════════════════════════════════════════════════════"
echo ""

# External Plugins (install via Claude Code /plugin commands)
echo "EXTERNAL PLUGINS (Install in Claude Code):"
echo "─────────────────────────────────────────"
echo ""
echo "1. Superpowers - TDD, debugging, collaboration"
echo "   Command: /plugin marketplace add obra/superpowers-marketplace"
echo "   Then:    /plugin install superpowers@superpowers-marketplace"
echo ""
echo "2. Claude Code Plugins Plus - 236 production skills"
echo "   Command: /plugin marketplace add jeremylongshore/claude-code-plugins-plus"
echo ""
echo "3. Agent Skill Creator - Auto-generate test/diagnostic agents"
echo "   Command: /plugin marketplace add FrancyJGLisboa/agent-skill-creator"
echo ""
echo "4. Awesome Claude Skills - Discovery and reference"
echo "   Bookmark: https://github.com/travisvn/awesome-claude-skills"
echo ""

# Built-in Skills (already in .claude/skills/)
echo ""
echo "BUILT-IN SKILLS (Already deployed):"
echo "────────────────────────────────────"
echo ""
ls -1 .claude/skills/ | grep -v "^_" | grep -v "\.md$" | while read skill; do
  if [ -f ".claude/skills/$skill/SKILL.md" ]; then
    echo "✓ $skill"
  fi
done
echo ""

# Custom Skills to Create
echo ""
echo "CUSTOM SKILLS TO CREATE (High priority):"
echo "──────────────────────────────────────────"
echo ""
echo "1. Audio DSP Patterns"
echo "   Path: .claude/skills/audio-dsp-patterns/"
echo "   Purpose: FFT, beat detection, audio-reactive LED patterns"
echo "   Status: [PENDING]"
echo ""
echo "2. TypeScript Advanced Patterns"
echo "   Path: .claude/skills/typescript-advanced/"
echo "   Purpose: Advanced types, generics, Zustand patterns"
echo "   Status: [PENDING]"
echo ""
echo "3. M5Stack Tab5 UI Components"
echo "   Path: .claude/skills/m5stack-tab5-ui/"
echo "   Purpose: Touch gestures, display primitives, components"
echo "   Status: [PENDING]"
echo ""
echo "4. FreeRTOS Task Synchronization"
echo "   Path: .claude/skills/freertos-synchronization/"
echo "   Purpose: Queues, semaphores, mutexes, real-time patterns"
echo "   Status: [PENDING]"
echo ""

echo "════════════════════════════════════════════════════════════"
echo "Next: Run external plugin installations in Claude Code"
echo "════════════════════════════════════════════════════════════"
