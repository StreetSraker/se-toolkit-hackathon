"""Generate SVG car placeholders for pre-tuned preset builds"""

import os

presets = [
    ('preset_drift_supra', '#1a0a0a', '#4a1a1a', '🏎️', 'Toyota Supra', 'Drift King — 700 HP', 'drift'),
    ('preset_track_skyline', '#0a0a2a', '#1a2a5a', '🏁', 'Nissan Skyline R34', 'Track Weapon — 800 HP', 'track'),
    ('preset_stance_rx7', '#2a1a0a', '#5a3a1a', '📸', 'Mazda RX-7 FD', 'Stance Build — 400 HP', 'stance'),
    ('preset_street_nsx', '#0a1a2a', '#1a3a5a', '🌃', 'Honda NSX', 'Street Elegance — 380 HP', 'street'),
    ('preset_drift_silvia', '#1a0a1a', '#4a1a3a', '💨', 'Nissan Silvia S15', 'Drift Missile — 600 HP', 'drift'),
    ('preset_street_chaser', '#0a0a0a', '#2a2a2a', '😴', 'Toyota Chaser JZX100', 'Street Sleeper — 500 HP', 'street'),
    ('preset_track_civic', '#1a1a0a', '#3a3a1a', '⏱️', 'Honda Civic EK9', 'Time Attack — 400 HP', 'track'),
    ('preset_rally_evo', '#0a1a0a', '#1a4a1a', '🏔️', 'Mitsubishi Evo VI', 'Rally Spec — 550 HP', 'rally'),
    ('preset_rally_impreza', '#0a0a1a', '#1a2a4a', '🪨', 'Subaru Impreza GC8', 'Gravel Rally — 450 HP', 'rally'),
    ('preset_touge_ae86', '#1a0a2a', '#3a1a5a', '🌙', 'Toyota AE86', 'Touge Legend — 220 HP', 'touge'),
]

svg_template = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" width="800" height="600">
  <defs>
    <linearGradient id="bg_{id}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{color1}"/>
      <stop offset="100%" style="stop-color:{color2}"/>
    </linearGradient>
    <filter id="shadow_{id}">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.5"/>
    </filter>
  </defs>

  <rect width="800" height="600" fill="url(#bg_{id})"/>

  <!-- Decorative racing stripes -->
  <rect x="0" y="520" width="800" height="8" fill="rgba(255,255,255,0.1)"/>
  <rect x="0" y="540" width="800" height="4" fill="rgba(255,255,255,0.05)"/>

  <!-- Car emoji -->
  <text x="400" y="220" font-family="Arial" font-size="100" text-anchor="middle" filter="url(#shadow_{id})">{emoji}</text>

  <!-- Car name -->
  <text x="400" y="320" font-family="Arial" font-size="42" font-weight="bold" text-anchor="middle" fill="rgba(255,255,255,0.95)" filter="url(#shadow_{id})">{name}</text>

  <!-- Build name / HP -->
  <text x="400" y="380" font-family="Arial" font-size="30" text-anchor="middle" fill="rgba(255,255,255,0.8)">{build}</text>

  <!-- Tag badge -->
  <rect x="340" y="420" width="120" height="36" rx="18" fill="{tag_color}" opacity="0.9"/>
  <text x="400" y="445" font-family="Arial" font-size="18" font-weight="bold" text-anchor="middle" fill="white">{tag}</text>

  <!-- Bottom accent line -->
  <rect x="300" y="500" width="200" height="3" rx="1" fill="{tag_color}" opacity="0.6"/>
</svg>'''

tag_colors = {
    'drift': '#e94560',
    'track': '#4ecdc4',
    'stance': '#f39c12',
    'street': '#3498db',
    'rally': '#2ecc71',
    'touge': '#9b59b6',
}

output_dir = os.path.dirname(__file__)

for preset_id, color1, color2, emoji, name, build, tag in presets:
    tc = tag_colors.get(tag, '#888888')
    svg = svg_template.format(
        id=preset_id,
        color1=color1,
        color2=color2,
        emoji=emoji,
        name=name,
        build=build,
        tag=tag,
        tag_color=tc,
    )

    filename = os.path.join(output_dir, f'{preset_id}.svg')
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(svg)

    print(f'✓ Created {preset_id}.svg')

print('\nAll preset images generated!')
