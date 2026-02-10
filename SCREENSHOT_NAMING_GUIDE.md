# Screenshot Naming Convention Guide

## Overview
Use a hierarchical naming system to organize screenshots based on UI navigation flow. This helps the AI understand relationships between screens and generate more accurate, organized test cases.

## Naming Structure

### Format
```
<main>.<sub>.<nested>.png
<main><letter>.png  (for scrollable pages)
```

### Examples

#### Main Screens (Top Level)
- `1.png` - Dashboard
- `2.png` - User Management
- `3.png` - Reports
- `4.png` - Settings

#### Scrollable Pages (Long Content)
When a screen is too long and requires scrolling to capture all content:
- `1a.png` - Dashboard (top section)
- `1b.png` - Dashboard (middle section - scrolled down)
- `1c.png` - Dashboard (bottom section - scrolled to end)
- `2a.png`, `2b.png` - User Management page (scrolled sections)

**Note:** Use letter suffixes (a, b, c, d...) for scroll sections of the **same screen**. These represent vertical continuation, not separate UI components.

#### Sub-components (Modals, Dialogs, Dropdowns)
- `1.1.png` - Modal opened from Dashboard
- `1.2.png` - Dropdown menu on Dashboard
- `1.3.png` - Side panel from Dashboard
- `2.1.png` - Add User modal from User Management
- `2.2.png` - Edit User modal from User Management

#### Nested Components (Components within components)
- `1.1.1.png` - Confirmation dialog within Dashboard modal
- `1.1.2.png` - Form validation error in Dashboard modal
- `2.1.1.png` - Datepicker in Add User modal

## Real-World Example

```
1.png        → Dashboard (main view - top section)
1a.png       → Dashboard (scrolled - middle section) 
1b.png       → Dashboard (scrolled - bottom section)
1.1.png      → "Create Event" modal on Dashboard
1.1.1.png    → Date picker in "Create Event" modal
1.1.2.png    → Time picker in "Create Event" modal
1.2.png      → "Filter" dropdown on Dashboard
1.3.png      → "Export" confirmation dialog on Dashboard

2.png        → Event List page (fits in one screen)
2.1.png      → Event details modal
2.1.1.png    → Delete confirmation in event details
2.2.png      → Bulk actions dropdown

3.png        → User Profile page
3a.png       → User Profile (scrolled to show more fields)
3.1.png      → Edit profile modal
3.2.png      → Change password modal
```

**Key Distinction:**
- **Letters (a, b, c)** = Same screen, scrolled down (vertical continuation)
- **Decimals (.1, .2, .3)** = Different component (modal, dropdown, dialog)

## Benefits

1. **Clear UI Hierarchy** - Instantly see parent-child relationships
2. **Better Test Organization** - Group test cases by main screen
3. **Accurate Test Flows** - AI understands navigation paths
4. **Easy Maintenance** - Quickly identify which screen a test case covers

## Tips

- Keep main screens sequential (1, 2, 3...)
- Use decimals for all sub-components
- Document your naming in a spreadsheet or notes file
- Be consistent across the entire application

## Test Case ID Correlation

You can optionally reference the screenshot number in test case titles:

```json
{
    "id": "202602GEN-0101",
    "title": "[Screen 1.1] Verify Create Event modal opens correctly",
    "steps": "1. Navigate to Dashboard (1.png)\n2. Click Create Event button\n3. Modal appears (1.1.png)"
}
```
