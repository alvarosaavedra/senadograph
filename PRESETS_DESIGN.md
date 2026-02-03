# Filter Presets - Visual Design & UX Improvements

## Design Overview

The preset selector has been completely redesigned from a simple dropdown to an interactive card-based layout with rich visual elements.

## Visual Features

### 1. Card-Based Layout
Each preset is displayed as a clickable card with:
- **Icon**: Large emoji icon for quick identification
- **Title**: Preset name (ES/EN support)
- **Description**: Two-line truncated description visible on hover
- **Active State**: Gradient background with border when selected
- **Hover Effects**: Scale and shadow animations

### 2. Color Scheme
- **Unselected State**: White background, dark text, transparent border
- **Selected State**: Gradient primary background, white text, primary border
- **Container**: Subtle gradient background (primary-5) with light border

### 3. Interaction Design
- Click to select/deselect preset
- Only one preset can be selected at a time
- Apply button appears when preset is selected
- Apply button includes checkmark icon

## Preset Cards

### ⚡ Polarización Partidista (Partisan Polarization)
**ES**: Visualice cómo los partidos votan de manera diferente e identifique los límites entre partidos
**EN**: Visualize how parties vote differently and identify party boundaries

**Visual**: Lightning bolt icon (⚡) - quick reference to "shocking" polarization

---

### 🤝 Alianzas Transpartidistas (Cross-Party Allies)
**ES**: Encuentre senadores que colaboran a través de las líneas partidistas a pesar de diferentes afiliaciones
**EN**: Find senators who collaborate across party lines despite different affiliations

**Visual**: Handshake emoji (🤝) - represents cooperation across parties

---

### 🏛️ Mediadores de Poder (Power Brokers)
**ES**: Identifique los senadores más influyentes a través de leyes autorizadas, comités y conexiones
**EN**: Identify most influential senators through authored laws, committees, and connections

**Visual**: Building emoji (🏛️) - represents institutional power

---

### 💼 Influencia Industrial (Industry Influence)
**ES**: Revele qué industrias/lobistas influyen en qué senadores
**EN**: Reveal which industries/lobbyists influence which senators

**Visual**: Briefcase emoji (💼) - represents business/corporate influence

---

### 📜 Colaboración Legislativa (Legislative Collaboration)
**ES**: Muestre patrones de colaboración a través de la autoría de leyes y patrones de votación
**EN**: Show collaboration patterns through law authorship and voting patterns

**Visual**: Scroll emoji (📜) - represents legislative documents

## Layout Structure

```
┌─────────────────────────────────────┐
│  🎨 Plantillas      [Reset ↻]  │  ← Title with reset button
├─────────────────────────────────────┤
│                                     │
│  ┌─────────────────────────────┐    │
│  │ ⚡ Polarización Partidista  │    │  ← Preset Card 1
│  │ Visualice cómo los partidos  │    │
│  │ votan de manera diferente  │    │
│  └─────────────────────────────┘    │
│                                     │
│  ┌─────────────────────────────┐    │
│  │ 🤝 Alianzas Transpartid. │    │  ← Preset Card 2
│  │ Encuentre senadores que    │    │
│  │ colaboran a través de...  │    │
│  └─────────────────────────────┘    │
│                                     │
│  [ ✓ Apply ]  ← Appears when card selected
│                                     │
└─────────────────────────────────────┘
```

## Styling Details

### Card Styling
```css
- Border-radius: 12px (rounded-xl)
- Border width: 2px
- Padding: 12px
- Transition: all 300ms
- Hover: scale(1.02), shadow-lg
- Active: gradient background, primary border
```

### Container Styling
```css
- Background: linear-gradient (primary/5)
- Border: primary-200/50
- Padding: 16px
- Border-radius: 12px
- Margin-bottom: 16px
```

### Apply Button
```css
- Background: gradient-primary
- Text: white, font-semibold
- Padding: 12px 16px
- Border-radius: 12px
- Hover: shadow-glow, scale(1.02)
- Active: scale(0.95)
- Icon: checkmark (✓) + "Apply" text
```

## Accessibility

- Semantic button elements for all interactions
- Keyboard navigation support
- Clear visual feedback for all states
- Readable text contrast ratios
- ARIA labels for screen readers

## Responsive Design

Cards stack vertically on mobile
Single column layout works well on all screen sizes
Touch-friendly tap targets (44px minimum)
Text truncation prevents overflow

## Browser Support

Modern browsers with CSS Grid support
IE11: Not supported (uses CSS grid, flexbox)
Graceful degradation for older browsers

## Performance

- No external dependencies for icons (emojis are native)
- CSS-only animations and transitions
- Efficient re-renders with Svelte's reactivity
- Minimal JavaScript overhead

## Future Enhancements

- Preset badges showing which filters are active
- Animated preset icons
- Preset preview showing filtered node count
- Custom preset creation from current filters
- Preset sharing via URL parameters
