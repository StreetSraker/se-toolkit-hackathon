"""Generate SVG car placeholders with gradients"""

import os

cars = [
    ('supra', '#ff6b35', '#ffcc00', '🏎️'),
    ('skyline', '#1e3c72', '#4a90d9', '🚗'),
    ('rx7', '#c41e3a', '#ff6b6b', '🏎️'),
    ('nsx', '#e0e0e0', '#bdbdbd', '🏎️'),
    ('silvia', '#f5f5f5', '#cccccc', '🚗'),
    ('chaser', '#4a4a4a', '#8a8a8a', '🚗'),
    ('civic', '#ffffff', '#e0e0e0', '🏎️'),
    ('evo', '#1e3a8a', '#3b82f6', '🚗'),
    ('impreza', '#0033a0', '#0099ff', '🚗'),
    ('ae86', '#f5f5f5', '#d0d0d0', '🚗'),
]

svg_template = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" width="800" height="600">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{color1}"/>
      <stop offset="100%" style="stop-color:{color2}"/>
    </linearGradient>
  </defs>
  
  <rect width="800" height="600" fill="url(#bg)"/>
  
  <text x="400" y="280" font-family="Arial" font-size="120" text-anchor="middle" fill="rgba(255,255,255,0.9)">{emoji}</text>
  
  <text x="400" y="380" font-family="Arial" font-size="48" font-weight="bold" text-anchor="middle" fill="rgba(255,255,255,0.95)">{name}</text>
  
  <text x="400" y="440" font-family="Arial" font-size="32" text-anchor="middle" fill="rgba(255,255,255,0.8)">{years}</text>
</svg>'''

output_dir = os.path.dirname(__file__)

car_info = {
    'supra': ('Toyota Supra', '1993-2002'),
    'skyline': ('Nissan Skyline R34', '1999-2002'),
    'rx7': ('Mazda RX-7 FD', '1992-2002'),
    'nsx': ('Honda NSX', '1990-2005'),
    'silvia': ('Nissan Silvia S15', '1999-2002'),
    'chaser': ('Toyota Chaser', '1996-2001'),
    'civic': ('Honda Civic Type R', '1997-2000'),
    'evo': ('Mitsubishi Evo VI', '1999-2001'),
    'impreza': ('Subaru Impreza STI', '1998-2000'),
    'ae86': ('Toyota AE86', '1983-1987'),
}

for car_id, color1, color2, emoji in cars:
    name, years = car_info[car_id]
    # Determine text color based on background brightness
    light_cars = ['nsx', 'silvia', 'civic', 'ae86', 'chaser']
    text_color = 'rgba(0,0,0,0.8)' if car_id in light_cars else 'rgba(255,255,255,0.95)'
    
    svg = svg_template.format(
        color1=color1,
        color2=color2,
        emoji=emoji,
        name=name,
        years=years
    )
    
    # Replace text colors for light cars
    if car_id in light_cars:
        svg = svg.replace('rgba(255,255,255,0.9)', 'rgba(0,0,0,0.6)')
        svg = svg.replace('rgba(255,255,255,0.95)', 'rgba(0,0,0,0.8)')
        svg = svg.replace('rgba(255,255,255,0.8)', 'rgba(0,0,0,0.6)')
    
    filename = os.path.join(output_dir, f'{car_id}.svg')
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(svg)
    
    print(f'✓ Created {car_id}.svg')

print('\nAll car images generated!')
