# Car database with 90s and 00s cars
CARS = [
    {
        "id": "supra",
        "name": "Toyota Supra A80",
        "years": "1993-2002",
        "image": "/static/images/cars/supra.svg",
        "description": "Legendary Japanese sports car with the inline-six 2JZ-GTE"
    },
    {
        "id": "skyline",
        "name": "Nissan Skyline R34 GT-R",
        "years": "1999-2002",
        "image": "/static/images/cars/skyline.svg",
        "description": "Godzilla - legendary all-wheel-drive sports car with RB26DETT"
    },
    {
        "id": "rx7",
        "name": "Mazda RX-7 FD",
        "years": "1992-2002",
        "image": "/static/images/cars/rx7.svg",
        "description": "Sports car with rotary engine 13B-REW"
    },
    {
        "id": "nsx",
        "name": "Honda NSX (NA1/NA2)",
        "years": "1990-2005",
        "image": "/static/images/cars/nsx.svg",
        "description": "Mid-engine supercar with V6 VTEC, developed with input from Ayrton Senna"
    },
    {
        "id": "silvia",
        "name": "Nissan Silvia S15",
        "years": "1999-2002",
        "image": "/static/images/cars/silvia.svg",
        "description": "The perfect drift car with SR20DET engine"
    },
    {
        "id": "chaser",
        "name": "Toyota Chaser JZX100",
        "years": "1996-2001",
        "image": "/static/images/cars/chaser.svg",
        "description": "Sedan with the legendary 1JZ-GTE, a popular tuning platform"
    },
    {
        "id": "civic",
        "name": "Honda Civic Type R (EK9)",
        "years": "1997-2000",
        "image": "/static/images/cars/civic.svg",
        "description": "Legendary hatchback with high-revving B16B VTEC"
    },
    {
        "id": "evo",
        "name": "Mitsubishi Lancer Evolution VI",
        "years": "1999-2001",
        "image": "/static/images/cars/evo.svg",
        "description": "Rally champion with 4G63T and advanced AYC all-wheel-drive"
    },
    {
        "id": "impreza",
        "name": "Subaru Impreza WRX STI (GC8)",
        "years": "1998-2000",
        "image": "/static/images/cars/impreza.svg",
        "description": "Iconic all-wheel-drive sedan with turbocharged flat-four EJ20"
    },
    {
        "id": "ae86",
        "name": "Toyota Sprinter Trueno AE86",
        "years": "1983-1987",
        "image": "/static/images/cars/ae86.svg",
        "description": "Drift legend with 4A-GE engine, star of Initial D"
    }
]

# Engine options database
ENGINES = {
    "supra": [
        {"id": "stock", "name": "Stock Engine", "power": "280 hp", "description": "Original stock engine, no modifications"},
        {"id": "2jz-stock", "name": "2JZ-GTE Stock", "power": "280 hp", "description": "Stock turbo engine"},
        {"id": "2jz-single", "name": "2JZ-GTE Single Turbo", "power": "500-700 hp", "description": "Single large turbo conversion"},
        {"id": "2jz-stroker", "name": "2JZ-GTE Stroker 3.4L", "power": "800-1000 hp", "description": "Increased displacement with forged internals"},
        {"id": "2jz-vvti", "name": "2JZ-GTE VVT-i Build", "power": "1000+ hp", "description": "Maximum build with VVT-i head"},
        {"id": "custom", "name": "Other option (specify)", "power": "—", "description": "Write your desired engine/configuration"},
    ],
    "skyline": [
        {"id": "stock", "name": "Stock Engine", "power": "280 hp", "description": "Original stock engine, no modifications"},
        {"id": "rb26-stock", "name": "RB26DETT Stock", "power": "280 hp", "description": "Stock Godzilla engine"},
        {"id": "rb26-stroker", "name": "RB26DETT Stroker 2.8L", "power": "600-800 hp", "description": "Increased displacement for higher boost"},
        {"id": "rb30", "name": "RB30DE + RB26 Head", "power": "700-900 hp", "description": "RB30 block with RB26 head hybrid"},
        {"id": "vr38-swap", "name": "VR38DETT Swap", "power": "600-1000+ hp", "description": "Engine swap from GT-R R35"},
        {"id": "custom", "name": "Other option (specify)", "power": "—", "description": "Write your desired engine/configuration"},
    ],
    "rx7": [
        {"id": "stock", "name": "Stock Engine", "power": "280 hp", "description": "Original stock engine, no modifications"},
        {"id": "13b-stock", "name": "13B-REW Stock", "power": "280 hp", "description": "Stock rotary with twin-turbo"},
        {"id": "13b-single", "name": "13B-REW Single Turbo", "power": "400-600 hp", "description": "Single turbo conversion Precision/Garrett"},
        {"id": "13b-bridge", "name": "13B Bridge Port", "power": "500-700 hp", "description": "Bridge ported for high RPM"},
        {"id": "20b-swap", "name": "20B-REW Swap", "power": "300-600 hp", "description": "3-rotor engine swap"},
        {"id": "custom", "name": "Other option (specify)", "power": "—", "description": "Write your desired engine/configuration"},
    ],
    "nsx": [
        {"id": "stock", "name": "Stock Engine", "power": "274 hp", "description": "Original stock engine, no modifications"},
        {"id": "c30a-stock", "name": "C30A Stock", "power": "274 hp", "description": "Stock V6 VTEC"},
        {"id": "c30a-sc", "name": "C30A Supercharged", "power": "350-400 hp", "description": "Comptech/CTS supercharger"},
        {"id": "c32b", "name": "C32B Swap", "power": "290 hp", "description": "Engine from NSX-R"},
        {"id": "k-swap", "name": "K-Series Swap", "power": "400-600 hp", "description": "K20/K24 swap with turbo"},
        {"id": "custom", "name": "Other option (specify)", "power": "—", "description": "Write your desired engine/configuration"},
    ],
    "silvia": [
        {"id": "stock", "name": "Stock Engine", "power": "250 hp", "description": "Original stock engine, no modifications"},
        {"id": "sr20-stock", "name": "SR20DET Stock", "power": "250 hp", "description": "Stock turbo engine"},
        {"id": "sr20-vvt", "name": "SR20DET VVT Swap", "power": "400-600 hp", "description": "SR20VE head with turbo"},
        {"id": "sr20-stroker", "name": "SR20DET Stroker 2.2L", "power": "500-700 hp", "description": "Increased displacement with forged internals"},
        {"id": "rb-swap", "name": "RB25/RB26 Swap", "power": "400-800 hp", "description": "RB inline-six engine swap"},
        {"id": "custom", "name": "Other option (specify)", "power": "—", "description": "Write your desired engine/configuration"},
    ],
    "chaser": [
        {"id": "stock", "name": "Stock Engine", "power": "280 hp", "description": "Original stock engine, no modifications"},
        {"id": "1jz-stock", "name": "1JZ-GTE Stock", "power": "280 hp", "description": "Stock turbo engine"},
        {"id": "1jz-vvti", "name": "1JZ-GTE VVT-i", "power": "320 hp", "description": "VVT-i version (Version 2)"},
        {"id": "1jz-single", "name": "1JZ-GTE Single Turbo", "power": "500-800 hp", "description": "Single large turbo conversion"},
        {"id": "2jz-swap", "name": "2JZ-GTE Swap", "power": "600-1000+ hp", "description": "Big brother 2JZ engine swap"},
        {"id": "custom", "name": "Other option (specify)", "power": "—", "description": "Write your desired engine/configuration"},
    ],
    "civic": [
        {"id": "stock", "name": "Stock Engine", "power": "185 hp", "description": "Original stock engine, no modifications"},
        {"id": "b16b-stock", "name": "B16B Stock", "power": "185 hp", "description": "Stock high-revving VTEC"},
        {"id": "b16b-built", "name": "B16B Built", "power": "250-300 hp", "description": "Forged pistons, camshafts"},
        {"id": "b18c", "name": "B18C Swap", "power": "200 hp", "description": "Engine from Integra Type R"},
        {"id": "k-swap", "name": "K20A Swap", "power": "300-500 hp", "description": "K-Series swap with turbo"},
        {"id": "custom", "name": "Other option (specify)", "power": "—", "description": "Write your desired engine/configuration"},
    ],
    "evo": [
        {"id": "stock", "name": "Stock Engine", "power": "280 hp", "description": "Original stock engine, no modifications"},
        {"id": "4g63-stock", "name": "4G63T Stock", "power": "280 hp", "description": "Stock turbo engine"},
        {"id": "4g63-built", "name": "4G63T Built", "power": "400-600 hp", "description": "Forged pistons, FP turbo"},
        {"id": "4g63-stroker", "name": "4G63T Stroker 2.2L", "power": "500-700 hp", "description": "Increased displacement with big turbo"},
        {"id": "4b11-swap", "name": "4B11 Swap (Evo X)", "power": "400-600 hp", "description": "Engine from Evo X"},
        {"id": "custom", "name": "Other option (specify)", "power": "—", "description": "Write your desired engine/configuration"},
    ],
    "impreza": [
        {"id": "stock", "name": "Stock Engine", "power": "280 hp", "description": "Original stock engine, no modifications"},
        {"id": "ej20-stock", "name": "EJ20 Stock", "power": "280 hp", "description": "Stock flat-four with turbo"},
        {"id": "ej20-built", "name": "EJ20 Built", "power": "400-500 hp", "description": "Forged pistons, VF/Garrett turbo"},
        {"id": "ej22", "name": "EJ22 Stroker", "power": "500-600 hp", "description": "Increased displacement 2.2L"},
        {"id": "ej25", "name": "EJ25 Swap", "power": "400-600 hp", "description": "2.5L block with EJ20 head"},
        {"id": "custom", "name": "Other option (specify)", "power": "—", "description": "Write your desired engine/configuration"},
    ],
    "ae86": [
        {"id": "stock", "name": "Stock Engine", "power": "130 hp", "description": "Original stock engine, no modifications"},
        {"id": "4age-stock", "name": "4A-GE Stock", "power": "130 hp", "description": "Stock high-revving engine"},
        {"id": "4age-built", "name": "4A-GE Built", "power": "200-250 hp", "description": "Individual throttle bodies, camshafts, ported"},
        {"id": "20v-blacktop", "name": "4A-GE 20V Black Top", "power": "165 hp", "description": "20-valve version from AE111"},
        {"id": "3sgte-swap", "name": "3S-GTE Swap", "power": "300-500 hp", "description": "Turbo engine swap from Celica MR2"},
        {"id": "custom", "name": "Other option (specify)", "power": "—", "description": "Write your desired engine/configuration"},
    ],
}

# Suspension setups
SUSPENSIONS = {
    "stock": {
        "name": "Stock Suspension",
        "description": "Original stock suspension, no modifications",
        "ride_height": "Stock height",
        "dampening": "Factory setting",
        "spring_rate": "Factory springs",
        "camber": "Factory angle",
        "use_case": "Original condition, daily driving"
    },
    "street": {
        "name": "Street Comfort",
        "description": "Comfortable setup for daily driving",
        "ride_height": "-30 mm",
        "dampening": "Soft",
        "spring_rate": "6-8 kg/mm",
        "camber": "-1.0 deg",
        "use_case": "Daily driving, cruises"
    },
    "sport": {
        "name": "Sport Setup",
        "description": "Sport setup for active driving",
        "ride_height": "-50 mm",
        "dampening": "Medium",
        "spring_rate": "8-10 kg/mm",
        "camber": "-1.5 deg",
        "use_case": "Sport driving, mountain roads"
    },
    "drift": {
        "name": "Drift Spec",
        "description": "Drift setup with increased steering angle",
        "ride_height": "-60 mm",
        "dampening": "Stiff front / medium rear",
        "spring_rate": "10-12 kg/mm",
        "camber": "-2.0 deg front / -1.0 deg rear",
        "use_case": "Drift, competitions"
    },
    "track": {
        "name": "Track Attack",
        "description": "Track setup for maximum performance",
        "ride_height": "-70 mm",
        "dampening": "Stiff",
        "spring_rate": "12-14 kg/mm",
        "camber": "-2.5 deg",
        "use_case": "Track days, time attack"
    },
    "stance": {
        "name": "Stance Show",
        "description": "Extremely lowered for shows",
        "ride_height": "-100 mm",
        "dampening": "Air suspension / Coilovers",
        "spring_rate": "8-10 kg/mm",
        "camber": "-3.0 deg and more",
        "use_case": "Shows, exhibitions"
    },
    "custom": {
        "name": "Other option (specify)",
        "description": "Write your desired suspension configuration",
        "ride_height": "—",
        "dampening": "—",
        "spring_rate": "—",
        "camber": "—",
        "use_case": "Custom setup"
    },
}

# Bodykit options (4 options as requested)
BODYKITS = [
    {
        "id": "stock",
        "name": "Stock Body",
        "description": "Original body, no modifications",
        "components": [],
        "style": "Original factory look",
        "price_range": "$0 (no changes)",
        "image": "/static/images/bodykits/Stock.png"
    },
    {
        "id": "rocket_bunny",
        "name": "Rocket Bunny / Pandem",
        "description": "Wide fiberglass fenders, aggressive look",
        "components": ["Wide front fenders", "Wide rear fenders", "Front bumper", "Rear bumper", "Side skirts", "Splitter", "GT wing"],
        "style": "Aggressive widebody",
        "price_range": "$2500-4000",
        "image": "/static/images/bodykits/Rocket Bunny.png"
    },
    {
        "id": "varis",
        "name": "VARIS",
        "description": "Japanese premium bodykit, track-developed",
        "components": ["Carbon hood", "Front bumper with canards", "Rear diffuser", "GT Wing", "Side skirts"],
        "style": "Aerodynamic track",
        "price_range": "$3000-5000",
        "image": "/static/images/bodykits/Varis.jpg"
    },
    {
        "id": "n1",
        "name": "N1 / Origin Labo",
        "description": "90s style with wide Super Silhouette fenders",
        "components": ["N1 wide fenders", "Front bumper", "Rear bumper", "Side skirts", "GT wing"],
        "style": "Retro 90s Super Silhouette",
        "price_range": "$2000-3500",
        "image": "/static/images/bodykits/Origin Labo.png"
    },
    {
        "id": "pandem_wide",
        "name": "Pandem Wide Arch",
        "description": "Extremely wide fenders for maximum effect",
        "components": ["Extra-wide front fenders", "Extra-wide rear fenders", "Aggressive front splitter", "Rear diffuser", "Side skirts", "Large GT wing"],
        "style": "Extreme widebody",
        "price_range": "$2500-4500",
        "image": "/static/images/bodykits/Pandem.jpg"
    },
    {
        "id": "custom",
        "name": "Other option (specify)",
        "description": "Write your desired bodykit or brand (VARIS, Rocket Bunny, Voltex, etc.)",
        "components": [],
        "style": "Custom",
        "price_range": "Negotiable",
        "image": ""
    },
]

# Wheel options (~10 options as requested)
WHEELS = [
    {
        "id": "stock",
        "name": "Stock Wheels",
        "description": "Original factory wheels",
        "sizes": "Factory size",
        "weight": "Factory weight",
        "style": "Original design",
        "price_range": "$0 (no changes)",
        "image": "/static/images/wheels/Stock.png"
    },
    {
        "id": "rays_volk",
        "name": "Rays Volk Racing TE37",
        "description": "Legendary forged wheels, JDM icon",
        "sizes": "17x9 / 18x9.5 / 18x10.5",
        "weight": "7.2 kg (17\")",
        "style": "6-spoke",
        "price_range": "$1200-1800/set",
        "image": "/static/images/wheels/Rays Volk Racing TE37.png"
    },
    {
        "id": "work_emotion",
        "name": "Work Emotion CR Kai",
        "description": "Classic JDM wheels with deep dish",
        "sizes": "17x8.5 / 18x9 / 18x9.5",
        "weight": "8.1 kg (17\")",
        "style": "10-spoke mesh",
        "price_range": "$900-1300/set",
        "image": "/static/images/wheels/Work Emotion CR Kai.png"
    },
    {
        "id": "ssr_profix",
        "name": "SSR Professor SP1",
        "description": "Premium classic-style wheels",
        "sizes": "18x8.5 / 18x9.5 / 19x10",
        "weight": "9.0 kg (18\")",
        "style": "3-piece mesh",
        "price_range": "$1500-2200/set",
        "image": "/static/images/wheels/SSR Professor SP1.png"
    },
    {
        "id": "advan_racing",
        "name": "Advan Racing GT",
        "description": "Lightweight track wheels from Yokohama",
        "sizes": "17x9 / 18x9.5 / 18x10",
        "weight": "6.9 kg (17\")",
        "style": "5 Y-spoke",
        "price_range": "$1000-1500/set",
        "image": "/static/images/wheels/ADVAN Racing GT.png"
    },
    {
        "id": "weds_sport",
        "name": "WedsSport TC-105X",
        "description": "Lightest Japanese track wheels",
        "sizes": "17x8.5 / 17x9 / 18x9.5",
        "weight": "6.5 kg (17\")",
        "style": "10 thin spokes",
        "price_range": "$900-1400/set",
        "image": "/static/images/wheels/WedsSport TC-105X.png"
    },
    {
        "id": "enkei_rpf1",
        "name": "Enkei RPF1",
        "description": "Versatile lightweight wheels, time attack choice",
        "sizes": "15x7 / 16x8 / 17x9 / 18x10",
        "weight": "6.4 kg (17\")",
        "style": "6 twin-spoke",
        "price_range": "$800-1200/set",
        "image": "/static/images/wheels/Enkei RPF1.png"
    },
    {
        "id": "bbs_rs",
        "name": "BBS RS-GT",
        "description": "German classic with gold spokes",
        "sizes": "17x8.5 / 18x9 / 18x9.5",
        "weight": "7.8 kg (17\")",
        "style": "Mesh gold spokes",
        "price_range": "$1800-2500/set",
        "image": "/static/images/wheels/BBS RS-GT.png"
    },
    {
        "id": "oz_ultra",
        "name": "OZ Ultraleggera",
        "description": "Italian lightweight wheels",
        "sizes": "17x7.5 / 18x8 / 18x9",
        "weight": "6.8 kg (17\")",
        "style": "5 Y-spoke",
        "price_range": "$1000-1500/set",
        "image": "/static/images/wheels/OZ Superleggera.png"
    },
    {
        "id": "work_cr_kai",
        "name": "Work CR Kai 3-Piece",
        "description": "Classic 3-piece wheels in 90s style",
        "sizes": "17x9 / 18x9.5 / 18x10.5",
        "weight": "8.5 kg (17\")",
        "style": "Step-lip mesh",
        "price_range": "$1500-2000/set",
        "image": "/static/images/wheels/WORK CR Kai 3-Piece.png"
    },
    {
        "id": "rays_volk_g25",
        "name": "Rays Volk Racing G25",
        "description": "Modern classic from Rays, 5-spoke",
        "sizes": "18x9 / 18x9.5 / 18x10.5",
        "weight": "7.5 kg (18\")",
        "style": "5-spoke",
        "price_range": "$1300-1800/set",
        "image": "/static/images/wheels/RAYS Volk Racing G25.png"
    },
    {
        "id": " Volk_racing_ce28n",
        "name": "Rays Volk Racing CE28N",
        "description": "6-spoke, forged, perfect for stance",
        "sizes": "17x8.5 / 18x9 / 18x9.5",
        "weight": "7.0 kg (17\")",
        "style": "6-spoke",
        "price_range": "$1400-2000/set",
        "image": "/static/images/wheels/RAYS Volk Racing CE28N.png"
    },
    {
        "id": "custom",
        "name": "Other option (specify)",
        "description": "Write your desired wheels (brand, model, size)",
        "sizes": "—",
        "weight": "—",
        "style": "Custom",
        "price_range": "Negotiable",
        "image": ""
    },
]

# Pre-tuned car builds (ready-to-order configurations)
PRESET_BUILDS = [
    {
        "id": "drift_supra",
        "name": "Toyota Supra — Drift King",
        "car_id": "supra",
        "image": "/static/images/cars/preset_drift_supra.svg",
        "tag": "Drift",
        "tag_color": "#e94560",
        "hp": "700 hp",
        "description": "Supra A80 with single large turbo, coilovers, and widebody kit — ready to drift and burn tires.",
        "engine": {"id": "2jz-single", "name": "2JZ-GTE Single Turbo", "power": "500-700 hp", "description": "Single large turbo conversion Garrett/Precision"},
        "suspension": {"id": "drift", "name": "Drift Spec", "description": "Drift setup with increased steering angle", "ride_height": "-60 mm", "dampening": "Stiff front / medium rear", "spring_rate": "10-12 kg/mm", "camber": "-2.0 deg front / -1.0 deg rear", "use_case": "Drift, competitions"},
        "bodykit": {"id": "rocket_bunny", "name": "Rocket Bunny / Pandem", "description": "Wide fiberglass fenders, aggressive look", "components": ["Wide front fenders", "Wide rear fenders", "Front bumper", "Rear bumper", "Side skirts", "Splitter", "GT wing"], "style": "Aggressive widebody", "price_range": "$2500-4000"},
        "wheels": {"id": "rays_volk", "name": "Rays Volk Racing TE37", "description": "Legendary forged wheels, JDM icon", "sizes": "17x9 / 18x9.5 / 18x10.5", "weight": "7.2 kg (17\")", "style": "6-spoke", "price_range": "$1200-1800/set"},
        "price_estimate": "$15,000-20,000"
    },
    {
        "id": "track_skyline",
        "name": "Nissan Skyline R34 — Track Weapon",
        "car_id": "skyline",
        "image": "/static/images/cars/preset_track_skyline.svg",
        "tag": "Track",
        "tag_color": "#4ecdc4",
        "hp": "800 hp",
        "description": "Godzilla for time attack: 2.8L stroker, track suspension, VARIS aero.",
        "engine": {"id": "rb26-stroker", "name": "RB26DETT Stroker 2.8L", "power": "600-800 hp", "description": "Increased displacement for higher boost"},
        "suspension": {"id": "track", "name": "Track Attack", "description": "Track setup for maximum performance", "ride_height": "-70 mm", "dampening": "Stiff", "spring_rate": "12-14 kg/mm", "camber": "-2.5 deg", "use_case": "Track days, time attack"},
        "bodykit": {"id": "varis", "name": "VARIS", "description": "Japanese premium bodykit, track-developed", "components": ["Carbon hood", "Front bumper with canards", "Rear diffuser", "GT Wing", "Side skirts"], "style": "Aerodynamic track", "price_range": "$3000-5000"},
        "wheels": {"id": "advan_racing", "name": "Advan Racing GT", "description": "Lightweight track wheels from Yokohama", "sizes": "17x9 / 18x9.5 / 18x10", "weight": "6.9 kg (17\")", "style": "5 Y-spoke", "price_range": "$1000-1500/set"},
        "price_estimate": "$18,000-25,000"
    },
    {
        "id": "stance_rx7",
        "name": "Mazda RX-7 FD — Stance Build",
        "car_id": "rx7",
        "image": "/static/images/cars/preset_stance_rx7.jpg",
        "tag": "Stance",
        "tag_color": "#f39c12",
        "hp": "400 hp",
        "description": "RX-7 FD with single turbo, air suspension, and extreme widebody — for shows and photos.",
        "engine": {"id": "13b-single", "name": "13B-REW Single Turbo", "power": "400-600 hp", "description": "Single turbo conversion Precision/Garrett"},
        "suspension": {"id": "stance", "name": "Stance Show", "description": "Extremely lowered for shows", "ride_height": "-100 mm", "dampening": "Air suspension / Coilovers", "spring_rate": "8-10 kg/mm", "camber": "-3.0 deg and more", "use_case": "Shows, exhibitions"},
        "bodykit": {"id": "pandem_wide", "name": "Pandem Wide Arch", "description": "Extremely wide fenders for maximum effect", "components": ["Extra-wide front fenders", "Extra-wide rear fenders", "Aggressive front splitter", "Rear diffuser", "Side skirts", "Large GT wing"], "style": "Extreme widebody", "price_range": "$2500-4500"},
        "wheels": {"id": "work_cr_kai", "name": "Work CR Kai 3-Piece", "description": "Classic 3-piece wheels in 90s style", "sizes": "17x9 / 18x9.5 / 18x10.5", "weight": "8.5 kg (17\")", "style": "Step-lip mesh", "price_range": "$1500-2000/set"},
        "price_estimate": "$14,000-19,000"
    },
    {
        "id": "street_nsx",
        "name": "Honda NSX — Street Elegance",
        "car_id": "nsx",
        "image": "/static/images/cars/preset_street_nsx.svg",
        "tag": "Street",
        "tag_color": "#3498db",
        "hp": "380 hp",
        "description": "NSX with supercharger, comfortable suspension, and stock body — the perfect grand tourer.",
        "engine": {"id": "c30a-sc", "name": "C30A Supercharged", "power": "350-400 hp", "description": "Comptech/CTS supercharger"},
        "suspension": {"id": "street", "name": "Street Comfort", "description": "Comfortable setup for daily driving", "ride_height": "-30 mm", "dampening": "Soft", "spring_rate": "6-8 kg/mm", "camber": "-1.0 deg", "use_case": "Daily driving, cruises"},
        "bodykit": {"id": "stock", "name": "Stock Body", "description": "Original body, no modifications", "components": [], "style": "Original factory look", "price_range": "$0 (no changes)"},
        "wheels": {"id": "bbs_rs", "name": "BBS RS-GT", "description": "German classic with gold spokes", "sizes": "17x8.5 / 18x9 / 18x9.5", "weight": "7.8 kg (17\")", "style": "Mesh gold spokes", "price_range": "$1800-2500/set"},
        "price_estimate": "$20,000-28,000"
    },
    {
        "id": "drift_silvia",
        "name": "Nissan Silvia S15 — Drift Missile",
        "car_id": "silvia",
        "image": "/static/images/cars/preset_drift_silvia.svg",
        "tag": "Drift",
        "tag_color": "#e94560",
        "hp": "600 hp",
        "description": "Silvia S15 with VVT swap, drift suspension, and wide bodykit — ready for sideways action.",
        "engine": {"id": "sr20-vvt", "name": "SR20DET VVT Swap", "power": "400-600 hp", "description": "SR20VE head with turbo"},
        "suspension": {"id": "drift", "name": "Drift Spec", "description": "Drift setup with increased steering angle", "ride_height": "-60 mm", "dampening": "Stiff front / medium rear", "spring_rate": "10-12 kg/mm", "camber": "-2.0 deg front / -1.0 deg rear", "use_case": "Drift, competitions"},
        "bodykit": {"id": "rocket_bunny", "name": "Rocket Bunny / Pandem", "description": "Wide fiberglass fenders, aggressive look", "components": ["Wide front fenders", "Wide rear fenders", "Front bumper", "Rear bumper", "Side skirts", "Splitter", "GT wing"], "style": "Aggressive widebody", "price_range": "$2500-4000"},
        "wheels": {"id": "enkei_rpf1", "name": "Enkei RPF1", "description": "Versatile lightweight wheels, time attack choice", "sizes": "15x7 / 16x8 / 17x9 / 18x10", "weight": "6.4 kg (17\")", "style": "6 twin-spoke", "price_range": "$800-1200/set"},
        "price_estimate": "$10,000-15,000"
    },
    {
        "id": "street_chaser",
        "name": "Toyota Chaser JZX100 — Street Sleeper",
        "car_id": "chaser",
        "image": "/static/images/cars/preset_street_chaser.svg",
        "tag": "Street",
        "tag_color": "#3498db",
        "hp": "500 hp",
        "description": "Sleeper sedan: 1JZ with big turbo, sport suspension, stock body — nobody expects it.",
        "engine": {"id": "1jz-single", "name": "1JZ-GTE Single Turbo", "power": "500-800 hp", "description": "Single large turbo conversion"},
        "suspension": {"id": "sport", "name": "Sport Setup", "description": "Sport setup for active driving", "ride_height": "-50 mm", "dampening": "Medium", "spring_rate": "8-10 kg/mm", "camber": "-1.5 deg", "use_case": "Sport driving, mountain roads"},
        "bodykit": {"id": "stock", "name": "Stock Body", "description": "Original body, no modifications", "components": [], "style": "Original factory look", "price_range": "$0 (no changes)"},
        "wheels": {"id": "rays_volk_g25", "name": "Rays Volk Racing G25", "description": "Modern classic from Rays, 5-spoke", "sizes": "18x9 / 18x9.5 / 18x10.5", "weight": "7.5 kg (18\")", "style": "5-spoke", "price_range": "$1300-1800/set"},
        "price_estimate": "$12,000-17,000"
    },
    {
        "id": "track_civic",
        "name": "Honda Civic EK9 — Time Attack",
        "car_id": "civic",
        "image": "/static/images/cars/preset_track_civic.svg",
        "tag": "Track",
        "tag_color": "#4ecdc4",
        "hp": "400 hp",
        "description": "EK9 Type R with K20 swap and turbo, track suspension, minimal bodykit for downforce.",
        "engine": {"id": "k-swap", "name": "K20A Swap", "power": "300-500 hp", "description": "K-Series swap with turbo"},
        "suspension": {"id": "track", "name": "Track Attack", "description": "Track setup for maximum performance", "ride_height": "-70 mm", "dampening": "Stiff", "spring_rate": "12-14 kg/mm", "camber": "-2.5 deg", "use_case": "Track days, time attack"},
        "bodykit": {"id": "n1", "name": "N1 / Origin Labo", "description": "90s style with wide Super Silhouette fenders", "components": ["N1 wide fenders", "Front bumper", "Rear bumper", "Side skirts", "GT wing"], "style": "Retro 90s Super Silhouette", "price_range": "$2000-3500"},
        "wheels": {"id": "weds_sport", "name": "WedsSport TC-105X", "description": "Lightest Japanese track wheels", "sizes": "17x8.5 / 17x9 / 18x9.5", "weight": "6.5 kg (17\")", "style": "10 thin spokes", "price_range": "$900-1400/set"},
        "price_estimate": "$12,000-16,000"
    },
    {
        "id": "rally_evo",
        "name": "Mitsubishi Evo VI — Rally Spec",
        "car_id": "evo",
        "image": "/static/images/cars/preset_rally_evo.svg",
        "tag": "Rally",
        "tag_color": "#2ecc71",
        "hp": "550 hp",
        "description": "Evo VI in rally spec: built 4G63, sport suspension, stock body.",
        "engine": {"id": "4g63-built", "name": "4G63T Built", "power": "400-600 hp", "description": "Forged pistons, FP turbo"},
        "suspension": {"id": "sport", "name": "Sport Setup", "description": "Sport setup for active driving", "ride_height": "-50 mm", "dampening": "Medium", "spring_rate": "8-10 kg/mm", "camber": "-1.5 deg", "use_case": "Sport driving, mountain roads"},
        "bodykit": {"id": "stock", "name": "Stock Body", "description": "Original body, no modifications", "components": [], "style": "Original factory look", "price_range": "$0 (no changes)"},
        "wheels": {"id": "rays_volk", "name": "Rays Volk Racing TE37", "description": "Legendary forged wheels, JDM icon", "sizes": "17x9 / 18x9.5 / 18x10.5", "weight": "7.2 kg (17\")", "style": "6-spoke", "price_range": "$1200-1800/set"},
        "price_estimate": "$14,000-19,000"
    },
    {
        "id": "rally_impreza",
        "name": "Subaru Impreza GC8 — Gravel Rally",
        "car_id": "impreza",
        "image": "/static/images/cars/preset_rally_impreza.svg",
        "tag": "Rally",
        "tag_color": "#2ecc71",
        "hp": "450 hp",
        "description": "Impreza GC8 in rally style: built EJ20, sport suspension, N1 bodykit.",
        "engine": {"id": "ej20-built", "name": "EJ20 Built", "power": "400-500 hp", "description": "Forged pistons, VF/Garrett turbo"},
        "suspension": {"id": "sport", "name": "Sport Setup", "description": "Sport setup for active driving", "ride_height": "-50 mm", "dampening": "Medium", "spring_rate": "8-10 kg/mm", "camber": "-1.5 deg", "use_case": "Sport driving, mountain roads"},
        "bodykit": {"id": "n1", "name": "N1 / Origin Labo", "description": "90s style with wide Super Silhouette fenders", "components": ["N1 wide fenders", "Front bumper", "Rear bumper", "Side skirts", "GT wing"], "style": "Retro 90s Super Silhouette", "price_range": "$2000-3500"},
        "wheels": {"id": "enkei_rpf1", "name": "Enkei RPF1", "description": "Versatile lightweight wheels, time attack choice", "sizes": "15x7 / 16x8 / 17x9 / 18x10", "weight": "6.4 kg (17\")", "style": "6 twin-spoke", "price_range": "$800-1200/set"},
        "price_estimate": "$12,000-17,000"
    },
    {
        "id": "touge_ae86",
        "name": "Toyota AE86 — Touge Legend",
        "car_id": "ae86",
        "image": "/static/images/cars/preset_touge_ae86.jpg",
        "tag": "Touge",
        "tag_color": "#9b59b6",
        "hp": "220 hp",
        "description": "Initial D style: built 4A-GE with individual throttle bodies, lightweight suspension, stock Hachi-Roku body.",
        "engine": {"id": "4age-built", "name": "4A-GE Built", "power": "200-250 hp", "description": "Individual throttle bodies, camshafts, ported"},
        "suspension": {"id": "street", "name": "Street Comfort", "description": "Comfortable setup for daily driving", "ride_height": "-30 mm", "dampening": "Soft", "spring_rate": "6-8 kg/mm", "camber": "-1.0 deg", "use_case": "Daily driving, cruises"},
        "bodykit": {"id": "stock", "name": "Stock Body", "description": "Original body, no modifications", "components": [], "style": "Original factory look", "price_range": "$0 (no changes)"},
        "wheels": {"id": "rays_volk", "name": "Rays Volk Racing TE37", "description": "Legendary forged wheels, JDM icon", "sizes": "17x9 / 18x9.5 / 18x10.5", "weight": "7.2 kg (17\")", "style": "6-spoke", "price_range": "$1200-1800/set"},
        "price_estimate": "$10,000-14,000"
    },
]
