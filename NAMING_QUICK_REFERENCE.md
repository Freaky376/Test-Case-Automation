# Quick Reference: Screenshot Naming Convention

## Basic Structure

```
Main Screens          →  1.png, 2.png, 3.png
Scrollable Pages      →  1a.png, 1b.png, 1c.png    (same screen, scrolled)
Sub-components        →  1.1.png, 1.2.png          (modals, dialogs, dropdowns)
Nested Components     →  1.1.1.png, 1.1.2.png      (components within components)
```

## Visual Example

```
┌─────────────────────────┐
│   1.png                 │  ← Dashboard (top section)
│   [Dashboard Header]    │
│   [Navigation]          │
│   [Content Area]        │
└─────────────────────────┘
         ↓ SCROLL DOWN
┌─────────────────────────┐
│   1a.png                │  ← Same dashboard, scrolled (middle)
│   [More Content]        │
│   [Charts/Tables]       │
└─────────────────────────┘
         ↓ SCROLL DOWN
┌─────────────────────────┐
│   1b.png                │  ← Same dashboard, scrolled (bottom)
│   [Footer Content]      │
│   [Settings Panel]      │
└─────────────────────────┘
         ↓ CLICK BUTTON
┌─────────────────────────┐
│  ╔═══════════════════╗  │
│  ║  1.1.png          ║  │  ← Modal opened FROM dashboard
│  ║  [Create Form]    ║  │     (DIFFERENT component)
│  ║  [Submit Button]  ║  │
│  ╚═══════════════════╝  │
└─────────────────────────┘
```

## Decision Tree

```
Is this a new main screen?
├─ YES → Use number (1.png, 2.png, 3.png)
└─ NO
   │
   Is it the same screen, just scrolled?
   ├─ YES → Use letter (1a.png, 1b.png, 1c.png)
   └─ NO
      │
      Is it a component (modal/dialog/dropdown)?
      ├─ YES → Use decimal (1.1.png, 1.2.png)
      └─ NO
         │
         Is it nested inside another component?
         └─ YES → Use more decimals (1.1.1.png, 1.1.2.png)
```

## Common Scenarios

| Scenario | Naming | Example |
|----------|--------|---------|
| Full-page screenshot | `1.png` | Dashboard main view |
| Same page, scrolled down | `1a.png`, `1b.png` | Long dashboard with scroll |
| Modal/Dialog | `1.1.png` | "Create Event" modal |
| Dropdown menu | `1.2.png` | Settings dropdown |
| Modal on scrolled page | `1a.1.png` | Modal from middle section |
| Nested dialog | `1.1.1.png` | Confirmation in modal |

## Tips

✅ **DO:**
- Use `1a.png`, `1b.png` for vertically scrolling the SAME screen
- Use `1.1.png`, `1.2.png` for DIFFERENT UI components
- Keep main screens sequential (1, 2, 3, 4...)

❌ **DON'T:**
- Mix letters and decimals incorrectly
- Skip numbers in sequence
- Use random naming
