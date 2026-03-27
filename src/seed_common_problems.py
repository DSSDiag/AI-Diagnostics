"""
Seed data for the common vehicle problems library.

This module provides a curated set of well-documented recurring faults for
popular vehicles in the Australian market. Each entry includes the fault,
common symptoms encountered when searching for the issue, and the typical
repair procedure.
"""

SEED_PROBLEMS = [
    # ── Toyota ──────────────────────────────────────────────────────────────
    {
        "make": "Toyota",
        "model": "Hilux",
        "year_from": 2005,
        "year_to": 2015,
        "fault": "Rear main seal oil leak",
        "symptoms": [
            "Oil pooling under the engine/gearbox area",
            "Burning oil smell after driving",
            "Gradual loss of engine oil between services",
            "Oil staining on the underside of the vehicle near the bellhousing",
        ],
        "repair": (
            "Replace the rear main crankshaft seal. Drop the gearbox/transmission to "
            "access the seal housing. Clean the mating surfaces thoroughly before fitting "
            "the new seal. Use genuine Toyota or high-quality aftermarket seal. Check the "
            "flywheel/flexplate for scoring that could damage the new seal."
        ),
        "obd_codes": "",
        "added_by": "seed",
    },
    {
        "make": "Toyota",
        "model": "LandCruiser 200",
        "year_from": 2007,
        "year_to": 2015,
        "fault": "Injector seal failure / diesel weeping",
        "symptoms": [
            "Diesel smell in the engine bay",
            "Black or brown carbon residue around injectors",
            "Rough idle, especially when cold",
            "Slight smoke at startup",
        ],
        "repair": (
            "Remove the affected injectors and replace the copper sealing washers and "
            "O-ring seals. Use the correct Toyota torque specification when re-fitting. "
            "Inspect injector tips for carbon build-up and clean if required. On high-mileage "
            "engines consider replacing all injector seals preventatively at the same time."
        ),
        "obd_codes": "",
        "added_by": "seed",
    },
    {
        "make": "Toyota",
        "model": "Camry",
        "year_from": 2002,
        "year_to": 2006,
        "fault": "Engine oil sludge build-up (2AZ-FE)",
        "symptoms": [
            "Engine noise after startup until oil circulates",
            "Oil pressure warning light flickering",
            "Premature oil consumption",
            "Visible sludge on oil cap or dipstick",
            "Rough idle or stalling",
        ],
        "repair": (
            "Perform multiple oil flush treatments followed by fresh oil and filter changes. "
            "In severe cases, remove the rocker cover to manually clean sludge deposits. "
            "Check and replace the PCV (positive crankcase ventilation) valve which is a "
            "known contributor to sludge. Switch to a quality 5W-30 fully synthetic oil and "
            "reduce service intervals to 5,000 km. Toyota issued an extended warranty on this "
            "fault — check if applicable."
        ),
        "obd_codes": "",
        "added_by": "seed",
    },
    {
        "make": "Toyota",
        "model": "Corolla",
        "year_from": 2003,
        "year_to": 2008,
        "fault": "Excessive oil consumption / blue smoke (1ZZ-FE)",
        "symptoms": [
            "Blue smoke from exhaust, especially on startup or during deceleration",
            "Needing to top up engine oil between services (more than 0.5 L per 1,000 km)",
            "Spark plugs fouled with oil",
            "Catalyst/DPF damage from oil burning",
        ],
        "repair": (
            "Replace piston rings and valve stem seals. This is a known design deficiency "
            "of the 1ZZ-FE engine. A full engine rebuild or replacement engine is often more "
            "cost effective on high-mileage vehicles. As a short-term measure, use a thicker "
            "viscosity oil (e.g. 10W-40 vs 5W-30) and an oil consumption additive. Check "
            "for Toyota's extended warranty/goodwill policies on this engine."
        ),
        "obd_codes": "P0301, P0302, P0303, P0304",
        "added_by": "seed",
    },
    {
        "make": "Toyota",
        "model": "Prado",
        "year_from": 2003,
        "year_to": 2009,
        "fault": "EGR valve carbon build-up (1KD-FTV)",
        "symptoms": [
            "Loss of power, especially under load",
            "Rough idle or hunting idle",
            "Excessive black smoke from exhaust",
            "Hard starting when warm",
            "Check engine light on",
        ],
        "repair": (
            "Remove and clean or replace the EGR valve and EGR cooler. Clean the intake "
            "manifold of carbon deposits. Many owners fit an EGR blanking plate as a "
            "preventative measure, though this may affect emissions compliance. Ensure the "
            "vehicle is regularly driven at highway speeds to help burn off deposits."
        ),
        "obd_codes": "P0400, P0401, P0402",
        "added_by": "seed",
    },
    # ── Ford ────────────────────────────────────────────────────────────────
    {
        "make": "Ford",
        "model": "Ranger",
        "year_from": 2011,
        "year_to": 2020,
        "fault": "EGR cooler failure (3.2 TDCI)",
        "symptoms": [
            "White/grey steam from exhaust, especially on startup",
            "Coolant loss with no visible external leak",
            "Milky residue on dipstick or oil cap",
            "Overheating or rising coolant temperature",
            "Sweet smell from exhaust",
        ],
        "repair": (
            "Replace the EGR cooler. Flush the cooling system completely after replacement "
            "to remove contaminated coolant. Inspect the oil for coolant contamination — if "
            "present, perform an oil flush and change. In severe cases (head gasket involvement) "
            "a head gasket check/replace is required. Some workshops recommend an upgraded "
            "aftermarket EGR cooler to prevent recurrence."
        ),
        "obd_codes": "P0401, P0402",
        "added_by": "seed",
    },
    {
        "make": "Ford",
        "model": "Focus",
        "year_from": 2012,
        "year_to": 2018,
        "fault": "PowerShift (DCT) transmission shudder",
        "symptoms": [
            "Shuddering or vibration during low-speed acceleration (0–30 km/h)",
            "Jerky or hesitant take-off from standstill",
            "Transmission 'hunting' at low speed in traffic",
            "Worse when engine/transmission is cold",
        ],
        "repair": (
            "Ford issued multiple TSBs and software updates for this fault. Start with a "
            "TCM (transmission control module) software update from a Ford dealer. If shudder "
            "persists, replace the clutch pack assembly. In severe cases the entire PowerShift "
            "unit may need replacement. Ford Australia offered an extended warranty on this issue "
            "— check eligibility. Use only Ford-specified MTF transmission fluid."
        ),
        "obd_codes": "P0726, P0730",
        "added_by": "seed",
    },
    # ── Holden ──────────────────────────────────────────────────────────────
    {
        "make": "Holden",
        "model": "Commodore",
        "year_from": 2006,
        "year_to": 2013,
        "fault": "AFM (Active Fuel Management) lifter failure (VE V8)",
        "symptoms": [
            "Ticking or tapping noise from the engine, especially at idle",
            "Engine running rough / misfire on one or more cylinders",
            "Check engine light on",
            "Oil pressure drops at idle",
            "Noise disappears momentarily after oil change then returns",
        ],
        "repair": (
            "Replace the collapsed/failed AFM lifters. Many workshops recommend replacing "
            "all 16 lifters at the same time rather than just the failed ones. It is common "
            "practice to install a Range Technology AFM disabler or tune out AFM to prevent "
            "recurrence. Replace the push rods if bent. Flush oil system and use a quality "
            "5W-30 or 5W-20 fully synthetic oil."
        ),
        "obd_codes": "P0300, P0301, P0302, P0305, P0306, P0308",
        "added_by": "seed",
    },
    {
        "make": "Holden",
        "model": "Astra",
        "year_from": 2004,
        "year_to": 2009,
        "fault": "Timing chain tensioner failure (Z18XER)",
        "symptoms": [
            "Rattling or chain slapping noise on cold start that may clear when warm",
            "Check engine light on",
            "Rough idle on cold starts",
            "In severe cases — engine misfires or won't start",
        ],
        "repair": (
            "Replace the timing chain tensioner and timing chain. The plastic tensioner "
            "guide is also prone to cracking and should be replaced. At the same time, "
            "replace the timing chain, all guides, and the VVT sprocket. Use only OEM-quality "
            "parts. Change oil promptly at correct intervals (low oil level accelerates wear). "
            "This is a pre-emptive repair that should be done by ~150,000 km."
        ),
        "obd_codes": "P0016, P0017",
        "added_by": "seed",
    },
    # ── Volkswagen ──────────────────────────────────────────────────────────
    {
        "make": "Volkswagen",
        "model": "Golf",
        "year_from": 2010,
        "year_to": 2015,
        "fault": "DSG (DQ200 7-speed) shudder at low speed",
        "symptoms": [
            "Shuddering/vibration during low-speed take-off or parking manoeuvres",
            "Jerky gear changes in stop-start traffic",
            "Transmission warning light",
            "Clunking when engaging Drive or Reverse from standstill",
        ],
        "repair": (
            "Update the mechatronic unit software (DSG adaptation reset). Replace the "
            "DSG mechatronic unit if software update doesn't resolve the issue. Ensure "
            "correct VW-spec DSG fluid (G 052 182) is used and replace the fluid and filter. "
            "VW issued a recall/extended warranty (TSB 09-15-23) — check VIN eligibility. "
            "Mechatronic unit replacement is a specialised job requiring DSG reset procedure."
        ),
        "obd_codes": "P17BF, P189E, P0843",
        "added_by": "seed",
    },
    {
        "make": "Volkswagen",
        "model": "Tiguan",
        "year_from": 2008,
        "year_to": 2016,
        "fault": "Timing chain stretch / failure (TSI engine)",
        "symptoms": [
            "Rattling noise from engine on startup, especially when cold",
            "Check engine light / engine management light on",
            "Rough running or misfires",
            "Engine going into limp mode",
            "Timing code fault stored in ECU",
        ],
        "repair": (
            "Replace the entire timing chain kit including chain, tensioner, guides, and "
            "sprockets. This is a known failure point on the TFSI/TSI family of engines. "
            "Early repair is critical — a snapped chain causes catastrophic engine damage. "
            "Use OEM-quality Iwis or Schaeffler chain kit. Always use correct specification "
            "oil (VW 504/507) and change at 10,000 km intervals maximum."
        ),
        "obd_codes": "P0016, P0017, P0008, P0009",
        "added_by": "seed",
    },
    # ── Mazda ───────────────────────────────────────────────────────────────
    {
        "make": "Mazda",
        "model": "CX-5",
        "year_from": 2012,
        "year_to": 2017,
        "fault": "Timing chain noise / rattle on cold start (SkyActiv-G)",
        "symptoms": [
            "Rattling or ticking from the engine on cold start (first 5–15 seconds)",
            "Noise clears once oil pressure builds",
            "Check engine light in some cases",
        ],
        "repair": (
            "Inspect the timing chain tensioner and chain for wear. Mazda issued a TSB "
            "recommending a revised oil jet to improve lubrication to the chain tensioner. "
            "Replace the chain tensioner with the updated part. Using 0W-20 fully synthetic "
            "oil as specified helps reduce cold-start chain rattle. On high-mileage vehicles "
            "replace the full timing chain kit."
        ),
        "obd_codes": "",
        "added_by": "seed",
    },
    {
        "make": "Mazda",
        "model": "3",
        "year_from": 2004,
        "year_to": 2009,
        "fault": "Rear wheel bearing failure",
        "symptoms": [
            "Humming or growling noise from rear that increases with vehicle speed",
            "Noise changes when turning (becomes louder or quieter)",
            "Vibration felt through seat or floor at highway speeds",
            "Noise doesn't change with engine load or braking",
        ],
        "repair": (
            "Replace the worn rear wheel bearing hub assembly. The Mazda3 BK/BL rear "
            "bearing is integral with the hub and must be replaced as a unit. Check both "
            "sides as both often wear at similar rates. Inspect for play in the bearing "
            "by lifting the vehicle and rocking the wheel at the 12 and 6 o'clock positions."
        ),
        "obd_codes": "",
        "added_by": "seed",
    },
    # ── BMW ─────────────────────────────────────────────────────────────────
    {
        "make": "BMW",
        "model": "3 Series",
        "year_from": 2005,
        "year_to": 2012,
        "fault": "VANOS solenoid failure",
        "symptoms": [
            "Rough idle, especially when cold",
            "Loss of power at low and mid RPM",
            "Increased fuel consumption",
            "Check engine light on",
            "Engine hesitation on acceleration",
        ],
        "repair": (
            "Replace the VANOS solenoids (intake and/or exhaust). The solenoids are "
            "inexpensive and located at the front of the engine. Also inspect and clean "
            "the variable valve timing oil strainers/filters which often clog and mimic "
            "solenoid failure. Use only BMW-specified fully synthetic 5W-30 oil and change "
            "at 10,000 km intervals to reduce VANOS wear."
        ),
        "obd_codes": "P1519, P1522, P0010, P0013",
        "added_by": "seed",
    },
    {
        "make": "BMW",
        "model": "X5",
        "year_from": 2007,
        "year_to": 2013,
        "fault": "Transfer case / ATC failure",
        "symptoms": [
            "4WD/AWD warning light on dashboard",
            "Drivetrain error message on iDrive",
            "Grinding or whining from the transfer case area",
            "Vehicle pulling to one side under acceleration",
            "Unable to engage or disengage 4WD",
        ],
        "repair": (
            "Scan the transfer case module for fault codes. Common failure points are the "
            "ATC 500/700 transfer case motor and the transfer case itself. Rebuild or replace "
            "the transfer case. Check the transfer case fluid level and condition — degraded "
            "fluid accelerates wear. BMW ETK should be consulted for the exact unit fitted. "
            "Reprogramming of the transfer case module is required after replacement."
        ),
        "obd_codes": "4X10, 4X20",
        "added_by": "seed",
    },
    # ── Hyundai ─────────────────────────────────────────────────────────────
    {
        "make": "Hyundai",
        "model": "i30",
        "year_from": 2012,
        "year_to": 2017,
        "fault": "Hydraulic engine mount failure",
        "symptoms": [
            "Excessive engine vibration felt through steering wheel, gear lever, and floor",
            "Clunking or thudding from engine bay at low speeds",
            "Vibration most noticeable at idle in Drive or Reverse",
            "Vibration worse when A/C is on",
        ],
        "repair": (
            "Replace the hydraulic (fluid-filled) engine mount. The front lower engine mount "
            "is the most common failure. Inspect all mounts at the same time as secondary mounts "
            "are often worn simultaneously. Hyundai updated the mount part number — ensure the "
            "revised OEM part is used. The repair is straightforward but requires engine support "
            "while the mount is removed."
        ),
        "obd_codes": "",
        "added_by": "seed",
    },
    # ── Subaru ──────────────────────────────────────────────────────────────
    {
        "make": "Subaru",
        "model": "WRX",
        "year_from": 2001,
        "year_to": 2014,
        "fault": "Head gasket failure (EJ20/EJ25)",
        "symptoms": [
            "Overheating or temperature gauge running higher than normal",
            "Coolant loss with no obvious external leak",
            "White smoke from exhaust",
            "Coolant in oil (milky oil cap/dipstick)",
            "Bubbles in coolant reservoir",
        ],
        "repair": (
            "Replace the head gasket(s). Subaru EJ-series engines are notorious for head "
            "gasket failure, particularly on the exhaust-side gasket. Use Cometic multi-layer "
            "steel (MLS) gaskets with ARP head studs for a long-lasting repair. Machine "
            "the head surface before reassembly. Flush the cooling system thoroughly. "
            "Consider fitting an oil catch can and monitoring coolant level closely post-repair."
        ),
        "obd_codes": "P0217, P0302",
        "added_by": "seed",
    },
    # ── Honda ───────────────────────────────────────────────────────────────
    {
        "make": "Honda",
        "model": "CR-V",
        "year_from": 2002,
        "year_to": 2006,
        "fault": "Timing belt / idler pulley failure (K24A)",
        "symptoms": [
            "Ticking or squealing from the timing cover area",
            "Check engine light on",
            "Engine vibration or rough running",
            "In failure — engine won't start or catastrophic internal damage",
        ],
        "repair": (
            "Replace the timing belt, water pump, idler pulley, tensioner pulley, and "
            "drive belts as a complete kit. This is a scheduled service item (every 160,000 km "
            "or 7 years) but the idler pulley on early K24A engines can fail prematurely. "
            "Never skip or delay this service — if the belt snaps the engine suffers "
            "catastrophic valve damage (interference engine)."
        ),
        "obd_codes": "",
        "added_by": "seed",
    },
    # ── Nissan ──────────────────────────────────────────────────────────────
    {
        "make": "Nissan",
        "model": "Navara",
        "year_from": 2005,
        "year_to": 2015,
        "fault": "Rear leaf spring cracking / chassis lean (D40)",
        "symptoms": [
            "Vehicle sitting noticeably lower on one side (typically driver's side)",
            "Clunking from the rear suspension over bumps",
            "Uneven tyre wear on rear axle",
            "Cracked or broken leaf spring visible on inspection",
        ],
        "repair": (
            "Replace the cracked leaf spring(s). Nissan issued a recall and extended warranty "
            "for this fault in Australia (check your VIN at recalls.infrastructure.gov.au). "
            "Aftermarket leaf spring packs from reputable suppliers (e.g. Dobinson's) are "
            "often a stronger replacement than OEM. Inspect the U-bolts and spring perches "
            "for wear at the same time."
        ),
        "obd_codes": "",
        "added_by": "seed",
    },
    {
        "make": "Nissan",
        "model": "X-Trail",
        "year_from": 2001,
        "year_to": 2007,
        "fault": "CVT transmission failure (T30)",
        "symptoms": [
            "Slipping, jerking, or hesitation during acceleration",
            "Whining or shuddering from the transmission",
            "Vehicle lurching under light throttle",
            "Transmission warning light on dashboard",
            "Loss of drive in forward or reverse",
        ],
        "repair": (
            "Drain and refill CVT fluid with Nissan NS-2 or equivalent CVT-specific fluid "
            "as a first step. If symptoms persist the CVT unit requires removal for inspection "
            "and likely rebuild or replacement. CVT fluid should be changed every 40,000 km "
            "for longevity — neglected fluid is the leading cause of premature failure. "
            "Rebuilt CVT units from reputable specialists are a cost-effective alternative "
            "to new units."
        ),
        "obd_codes": "P0736, P1777, P1778",
        "added_by": "seed",
    },
    # ── Mitsubishi ──────────────────────────────────────────────────────────
    {
        "make": "Mitsubishi",
        "model": "Pajero",
        "year_from": 2000,
        "year_to": 2014,
        "fault": "Rear diff lock actuator failure",
        "symptoms": [
            "4WD / diff lock warning light stays on or flashing",
            "Unable to engage or disengage rear diff lock",
            "Grinding noise when attempting to lock the diff",
            "Dashboard switch illuminated but no engagement",
        ],
        "repair": (
            "Remove the rear differential actuator and inspect the motor and gears for "
            "wear. The actuator motor brushes commonly wear out. Clean and regrease the "
            "actuator or replace the full actuator unit. Check the wiring loom and connector "
            "for corrosion — a common failure point. Verify the diff lock function with a "
            "scan tool before and after repair."
        ),
        "obd_codes": "",
        "added_by": "seed",
    },
    # ── Kia ─────────────────────────────────────────────────────────────────
    {
        "make": "Kia",
        "model": "Sportage",
        "year_from": 2010,
        "year_to": 2016,
        "fault": "Theta II engine failure (2.0/2.4 GDI) — metal debris in oil",
        "symptoms": [
            "Knocking noise from the engine",
            "Oil pressure warning light on",
            "Check engine light on",
            "Engine stalling or loss of power",
            "Metal shavings visible in engine oil",
        ],
        "repair": (
            "This is a known manufacturing defect (insufficient deburring of the crankshaft "
            "oil passage). Kia and Hyundai issued recalls and extended warranties in several "
            "markets. Check your VIN against the Kia recall list. In early cases an oil flush "
            "and replacement may resolve debris contamination. In advanced cases the short "
            "block or complete engine must be replaced. Only use quality 5W-20 or 5W-30 "
            "fully synthetic oil and change every 5,000–7,500 km."
        ),
        "obd_codes": "P0010, P0011, P1326",
        "added_by": "seed",
    },
    # ── Mercedes-Benz ────────────────────────────────────────────────────────
    {
        "make": "Mercedes-Benz",
        "model": "C-Class",
        "year_from": 2007,
        "year_to": 2014,
        "fault": "Balance shaft / oil pump chain failure (M271 engine)",
        "symptoms": [
            "Rattling or chain noise on startup that may or may not clear",
            "Oil pressure warning light",
            "Check engine light with camshaft timing fault codes",
            "Rough idle and poor performance",
            "In severe cases — complete engine seizure",
        ],
        "repair": (
            "Replace the balance shaft module, oil pump chain, and associated guides and "
            "tensioners. This is a well-documented catastrophic failure on M271 engines. "
            "Early intervention is critical — a snapped oil pump chain results in complete "
            "engine destruction. Many specialists recommend pre-emptive replacement around "
            "120,000–150,000 km. Use only OEM or OEM-equivalent parts from suppliers such as "
            "INA/Schaeffler."
        ),
        "obd_codes": "P0016, P0017, P0011",
        "added_by": "seed",
    },
    # ── Subaru (additional) ──────────────────────────────────────────────────
    {
        "make": "Subaru",
        "model": "Forester",
        "year_from": 2008,
        "year_to": 2012,
        "fault": "PCV (positive crankcase ventilation) system failure causing oil consumption",
        "symptoms": [
            "Blue smoke from exhaust at startup or under deceleration",
            "Excessive oil consumption (needing top-up between services)",
            "Oil in the air intake / intercooler pipes",
            "Rough idle due to unmetered air entering intake",
        ],
        "repair": (
            "Replace the PCV valve and inspect the associated hoses for cracks and blockages. "
            "The PCV valve on EJ engines is inexpensive and often overlooked. Install an "
            "aftermarket oil catch can in the breather circuit to prevent recurrence. Also "
            "inspect valve stem seals and piston rings if consumption continues after PCV repair."
        ),
        "obd_codes": "",
        "added_by": "seed",
    },
    # ── Mitsubishi (additional) ──────────────────────────────────────────────
    {
        "make": "Mitsubishi",
        "model": "Triton",
        "year_from": 2006,
        "year_to": 2015,
        "fault": "Transfer case vacuum actuator failure",
        "symptoms": [
            "4WD does not engage despite switch activation",
            "4WD light flashing continuously",
            "Unable to switch between 2H, 4H, and 4L",
            "Grinding when attempting 4WD engagement",
        ],
        "repair": (
            "Inspect the vacuum actuator on the front differential for cracks or failures "
            "in the diaphragm. Check all vacuum hoses for splits or disconnections. Replace "
            "the vacuum actuator if the diaphragm has failed. The vacuum pump or solenoids "
            "controlling the system should also be tested. Some workshops convert to a manual "
            "cable engagement as a more reliable long-term solution."
        ),
        "obd_codes": "",
        "added_by": "seed",
    },
]
