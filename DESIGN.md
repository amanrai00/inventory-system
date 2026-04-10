# DESIGN.md

## 1. Visual Theme & Atmosphere

Internal operations dashboard for a small business inventory system.

The interface should feel:
- calm
- efficient
- trustworthy
- desktop-first
- optimized for repeated daily use

Avoid marketing-site styling, oversized hero sections, playful gradients, or consumer-app aesthetics. This is an authenticated staff tool, not a public landing page.

The current app uses Flask, Jinja2 templates, Bootstrap/AdminLTE structure, and Font Awesome icons. Preserve that general application-shell pattern unless there is a strong reason to change it.

## 2. Product Intent

Primary user goals:
- sign in quickly
- review inventory health at a glance
- find low-stock and out-of-stock items immediately
- manage products with minimal friction
- record sales fast and safely
- read tables and forms without visual clutter

The design should prioritize clarity over novelty. Every screen should communicate operational status quickly.

## 3. Color Palette & Semantic Roles

Use a restrained neutral foundation with strong semantic status colors.

Core palette:
- App background: `#F3F6F8`
- Surface: `#FFFFFF`
- Surface alt: `#F8FAFC`
- Primary text: `#111827`
- Secondary text: `#6B7280`
- Border: `#D9E2EC`
- Sidebar background: `#1F2937`
- Sidebar active: `#2563EB`
- Sidebar text: `#E5E7EB`
- Sidebar muted text: `#9CA3AF`
- Primary action: `#2563EB`
- Primary action hover: `#1D4ED8`

Semantic colors:
- Success / normal stock: `#059669`
- Warning / low stock: `#D97706`
- Danger / out of stock / destructive actions: `#DC2626`
- Info / neutral metrics: `#0F766E`

Usage rules:
- Reserve saturated colors for actions, status, and KPI emphasis.
- Most surfaces should remain white or very light gray.
- Never use more than one accent color in the same local component unless status colors require it.
- Low stock and out of stock states must be visually distinct in badges, alerts, and table rows.

## 4. Typography Rules

Use a clean sans-serif stack suitable for admin software.

Preferred stack:
- `"Inter", "Segoe UI", "Helvetica Neue", Arial, sans-serif`

Type hierarchy:
- Page title: 28px, semibold
- Section title: 20px to 22px, semibold
- Card title: 16px to 18px, semibold
- Body text: 14px to 16px, regular
- Table text: 14px, regular
- Form labels: 13px to 14px, medium
- KPI numbers: 28px to 36px, bold, tight line-height
- Sidebar labels: 14px to 15px, medium

Rules:
- Keep line-height generous for body copy and compact for numeric metrics.
- Use heavier weight for counts and inventory status, not for long paragraphs.
- Avoid decorative or display fonts.

## 5. Layout Principles

The app should use a stable admin shell:
- left sidebar for primary navigation
- top navbar for user context and global actions
- main content area with a consistent page header

Spacing system:
- 4px base unit
- common gaps: 8px, 12px, 16px, 24px, 32px

Layout behavior:
- Sidebar width should feel fixed and dependable, around 240px to 280px.
- Main content should breathe, with 24px padding on desktop.
- Cards, tables, and forms should align to a simple grid.
- Dense data views are acceptable, but never cramped.
- On mobile, stack cards vertically and reduce padding before shrinking text.

## 6. Shell Components

### Sidebar

The sidebar is dark, quiet, and utility-focused.

Rules:
- Brand at top with simple product name: "Inventory System"
- Use clear icons paired with labels
- Active item should have a solid blue highlight or strong contrast state
- Hover state should be visible but subtle
- Navigation groups should remain short and scannable

### Top Navbar

The navbar should be light and unobtrusive.

Rules:
- Keep the menu toggle on the left
- Keep user name and logout action on the right
- Avoid adding noisy widgets or unnecessary badges

### Footer

Minimal. Light presence. No heavy decoration.

## 7. Card Design

Cards are the default content container for dashboard summaries, forms, and supporting sections.

Card styling:
- white background
- 1px soft border
- subtle shadow
- 10px to 14px corner radius if customizing beyond AdminLTE defaults
- 16px to 24px internal padding

Cards should feel crisp, not glossy.

## 8. Dashboard Patterns

The dashboard is an operational overview, not an analytics deep-dive.

Priority content:
- total products
- low stock items
- out of stock items
- total sales

KPI cards should:
- display the number first
- use a short supporting label
- include a meaningful icon
- use semantic color only where it helps interpretation

Interpretation rules:
- Total Products: neutral or informational
- Low Stock: warning
- Out of Stock: danger
- Total Sales: success or neutral-positive

If additional sections are added later, prefer:
- low-stock table
- recent sales list
- quick actions panel

## 9. Table Design

Tables are critical in this product and must be easy to scan.

Rules:
- compact but readable row height
- strong header contrast
- subtle row separators
- numeric columns right-aligned when appropriate
- action buttons grouped consistently
- avoid heavy zebra striping; keep striping subtle if used

Recommended product table columns:
- product name
- SKU
- price
- stock quantity
- minimum stock level
- status
- actions

Status treatment:
- Normal: green badge
- Low Stock: amber badge
- Out of Stock: red badge

If useful, rows for out-of-stock items may also receive a faint red-tinted background.

## 10. Forms & Inputs

Forms should feel predictable and efficient.

Rules:
- labels always visible above inputs or clearly associated
- input height comfortable for repeated use
- border contrast must be sufficient
- focus state must be prominent and accessible
- required actions should be clear
- primary submit button should be visually dominant

Field patterns:
- product forms should emphasize name, SKU, price, stock quantity, and minimum stock level
- sales forms should prioritize speed and error prevention
- destructive or risky actions should never look identical to safe actions

Validation:
- inline error messages near fields
- red border and helper text for invalid fields
- success messages should appear as dismissible alerts

## 11. Alerts, Badges, and Feedback

System feedback should be immediate and easy to interpret.

Alert behavior:
- success: green-tinted background with darker text
- warning: amber-tinted background
- error: red-tinted background
- info: blue-tinted background

Badge rules:
- badges should be short, uppercase or title-case, and high contrast
- do not use too many badge variants beyond semantic inventory states

## 12. Buttons

Button hierarchy:
- Primary: save, submit, confirm
- Secondary: cancel, back, filter, non-critical actions
- Danger: delete, destructive confirmation

Style rules:
- medium radius
- medium font weight
- clear hover and focus states
- icon use is acceptable when paired with a text label

Avoid ghost buttons for primary actions in core flows.

## 13. Login Page

The login page should feel clean and focused.

Structure:
- centered login card
- simple product title
- short supporting sentence
- email and password fields with icons if desired
- one strong sign-in button

Visual direction:
- light neutral background
- single elevated card
- minimal distractions
- trustworthy enterprise tone

Do not add marketing copy, testimonials, or promotional illustrations.

## 14. Interaction Rules

All interactive elements must have:
- visible hover state
- visible focus state
- disabled state
- keyboard-accessible behavior

Operational rules:
- destructive actions require confirmation
- flash messages should appear near the top of the content area
- stock-related warnings should be visible without deep navigation

## 15. Accessibility & UX Guardrails

Requirements:
- maintain strong text contrast
- never rely on color alone for stock status; pair color with labels
- ensure forms are usable by keyboard
- keep headings and section order logical
- avoid tiny click targets

This application should feel reliable and low-stress for staff using it repeatedly during a workday.

## 16. Implementation Notes For This Project

When applying this design to the current codebase:
- keep the existing Flask route structure
- keep the Jinja template inheritance model
- preserve the current sidebar plus navbar shell in `templates/base.html`
- refine AdminLTE styling rather than fighting the framework everywhere
- add custom polish in `static/css/style.css`

Prioritize improvements to:
- `templates/login.html`
- `templates/base.html`
- `templates/dashboard.html`
- product list and form templates
- sales record and history templates
