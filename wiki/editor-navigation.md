---
id: DOC-EDITOR-NAVIGATION
type: guide
status: current
updated: 2026-10-09
access: neutral
---

# Reading the wiki in Neovim

The local Neovim configuration now enables Markdown navigation and rendering.
Open the appropriate role's index; analyst/maintainer example from the repo root:

```sh
nvim wiki/index.md
```

Restart an existing Neovim session to load the configuration. Normal mode displays
formatted headings, lists, tables and links. The cursor line exposes its source;
insert mode returns to raw Markdown for editing. This is in-editor decoration,
not a browser renderer for images, arbitrary HTML or diagrams.

| Normal-mode key | Action |
| --- | --- |
| `s` / `S`, then two characters | Leap forward / backward to matching text |
| Enter or `gf` | Follow the link under the cursor, including local heading anchors |
| Backspace | Previous page in Markdown navigation history |
| Delete | Forward in Markdown navigation history |
| Tab / Shift-Tab | Next / previous link |
| `]]` / `[[` | Next / previous heading |
| Space, then `m`, then `r` | Toggle formatted/raw display |

`:RenderMarkdown toggle` also toggles rendering. Link paths resolve relative to
the current document. The navigation setup does not automatically create missing
pages or directories. External links open in the system browser when followed.
Existing editing mappings remain in effect; these navigation mappings apply only
to Markdown buffers. Editor navigation does not enforce clean-room access rules.

## Configuration and portability

Configuration lives in the user's separate dotfiles checkout:
`~/.config/nvim/init.lua` declares the two plugins with pinned commits and loads
`~/.config/nvim/lua/markdown_reading.lua`. The project itself needs no special
Markdown syntax or generated links. Cloning this project does not install the
editor configuration.

- [render-markdown.nvim](https://github.com/MeanderingProgrammer/render-markdown.nvim/tree/245956d67572c137df375dbf256e96bdb07e0937)
  supplies rendering, pinned to `245956d67572c137df375dbf256e96bdb07e0937`.
- [Mkdnflow](https://github.com/jakewvincent/mkdnflow.nvim/tree/272148c4bd1996380b9b540540758d57667e59c4)
  supplies navigation, pinned to `272148c4bd1996380b9b540540758d57667e59c4`.

Both are installed under `~/.local/share/nvim/plugged/` and declared through the
existing vim-plug configuration. Neovim 0.11.3 already supplied the `markdown`
and `markdown_inline` Tree-sitter parsers; no parser build was required here.
Another host must supply those parsers and install the declared plugins.

## Validation

A headless smoke run using the real user configuration followed the research
index link, returned, followed the runtime-escalation heading anchor, returned,
and checked that render-markdown created buffer decorations. All checks passed.
This validates navigation and rendering activation, not terminal font appearance.
Startup also emits an existing unrelated fuzzy.nvim warning about a missing
fuzzy-search executable; it did not prevent these checks. Plain Vim configuration
was left unchanged after the user selected Neovim.

## Leap startup mapping repair

The existing `VimEnter` call to `require('leap').set_default_keymaps()` skipped
`s` and `S`: the installed helper checks `hasmapto`, which finds Leap's own
compatibility aliases and concludes the target is already mapped. The keys were
unbound after startup in both ordinary and Markdown buffers. Evidence: installed
Leap revision `c4a215a`, `lua/leap/user.lua` function `set_default_keymaps`, and
`plugin/init.lua` deprecated alias entries. The Markdown configuration does not
map these keys.

The dotfiles `init.lua` now explicitly binds normal/visual `s` and `S` to
`<Plug>(leap-forward)` and `<Plug>(leap-backward)`. A one-off headless check after
`VimEnter` failed with `s missing in n` before the change, then passed for both
normal/visual bindings, actual `sxy` forward and `Saa` backward cursor movement,
and coexistence with the Markdown Enter binding. This covers startup that the
earlier Markdown smoke check did not exercise. Restart Neovim to load the fix.
