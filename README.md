# Meridian W104

Meridian W104 is my custom full size **104-key wireless mechanical keyboard**, built around a **Seeed XIAO nRF52840 non-Plus**.

so basically i wanted a full size board with a proper number pad that could run over bluetooth, but still use usb-c when needed. the project brings together the key matrix, diodes, serial scan logic, battery connection and a slim rounded case. the hardware is in KiCad and the case source is in Fusion 360, with the files needed to make a first prototype included here.

![Meridian W104 full 3D assembly](Images/Fusion%20Assembly.png)

## why i made this

i wanted to understand how a complete keyboard fits together, from what happens when a switch closes to how that key reaches the computer. keeping the numpad and navigation block was important, and i wanted the enclosure to feel like one finished design instead of a box around a PCB.

main goals for this project :

- make a full size ANSI board with 104 keys, navigation keys and numpad
- use **Bluetooth LE** with a protected single-cell battery, plus usb-c
- scan the large matrix using one 74HC595 and three 74HC165 registers
- keep the schematic on one sheet and the board routing orderly
- build a slim rounded case with a bronze seam accent and concealed screws
- learn the complete sequence: schematic → PCB layout → CAD → fabrication → firmware bring-up

the tricky parts were making the matrix and firmware agree, keeping the radio antenna clear, and checking that the screws and battery actually fit the case. those checks matter just as much as the overall appearance.

## project status

this is the final digital **V1 first-prototype fabrication package**. the latest review on 9 October 2026 passed the configured KiCad electrical and board checks with zero errors and zero unconnected items. firmware simulation covers all 104 populated keys. the five printable meshes are closed, and the retained full STEP check covers 219 valid solids. physical soldering, typing, BLE range, charging and print-fit testing are the next stage.

whats included :

- editable KiCad project, one-page schematic, PCB, local libraries and 104 linked switch models
- editable Fusion archive and complete assembly `.step`
- five printable `.stl` parts, with printing and assembly instructions
- Gerber/drill ZIP, assembly BOM, placement files and release checks
- CircuitPython USB/BLE firmware and a matrix diagnostic
- schematic/PCB PDFs, project images, cart evidence

current hardware summary :

| | |
|---|---|
| Layout | full size ANSI, 104 keys including nav block and numpad |
| Controller | Seeed XIAO nRF52840, original non-Plus |
| Connectivity | Bluetooth LE and usb-c; rear mode button switches transport |
| Matrix | 6 rows × 22 columns, 104 populated positions |
| Scan logic | 1× 74HC595 row register, 3× 74HC165 column registers, 3.3V |
| Diodes | 104× 1N4148W, one per switch |
| Battery | protected 3.7V 500mAh 502248P, with a separate PH2.0 pigtail |
| Indicators | Caps Lock, Num Lock and Scroll Lock; Num LED blinks while waiting for BLE |
| Stabilizers | Durock V2 PCB screw-in set: seven 2U plus one 6.25U |
| Switches | soldered MX-compatible PCB pattern; listed Haku pack selection |
| Keycaps | ANSI MX set with 6.25U spacebar; white Cherry-profile selection |
| Case | rounded printed bottom, frame, plate, bronze accent and mode-button cap |
| PCB | four copper layers, 1.6mm FR4; nominal 458.15 × 164mm |

the Meridian look comes from the rounded frame, recessed rear controls and thin accent seam. the white keycaps keep the full size layout easy to read. these are design renders; a finished physical keyboard has not been photographed yet.

## images

### full 3d model

![Complete keyboard assembly](Images/Fusion%20Assembly.png)

### indicator leds (caps / num / scroll)

the three lock indicators sit in the rear strip. the PCB view also shows the switches and controller placement.

![PCB 3D view and indicator strip](Images/KiCad%20PCB%203D.png)

### pcb

![Meridian W104 PCB routing](Images/KiCad%20PCB%20Editor.png)

### schematic / wiring

the complete matrix, XIAO, four scan registers, battery wiring, switches and lock indicators are on one A2 sheet. the [PDF](PDFs/Meridian%20W104.pdf) can be zoomed to read individual values and pins.

![Complete one-page schematic](Images/Schematic%20Full.png)

### other screenshots

some more views of the case and plate from Fusion :

![Bottom case and battery area](Images/Fusion%20Bottom.png)
![Switch plate](Images/Fusion%20Plate.png)
![Rounded top frame](Images/Fusion%20Top%20Frame.png)
![Bronze seam accent](Images/Fusion%20Bronze%20Seam%20Accent.png)
![Rear mode-button cap](Images/Fusion%20Mode%20Button.png)

## repo file checklist

important files in this repo :

- `PCB/Meridian W104.kicad_pro`
- `PCB/Meridian W104.kicad_sch`
- `PCB/Meridian W104.kicad_pcb`
- `PCB/3D Models/` — portable switch models and attribution
- `CAD/Full Meridian W104/Meridian W104.step`
- `CAD/Printing Files/` — `Bottom.stl`, `Plate.stl`, `Top Frame.stl`, `Bronze Seam Accent.stl`, `Mode Button.stl`
- `Firmware/boot.py`, `code.py`, `scanner.py`, `keymap.py`, `matrix_diagnostic.py`
- `Fabrication/Assembly BOM.csv`
- `Fabrication/Component Positions.csv` and `SMD Positions.csv`
- `Fabrication/netlist.ipc` — IPC-D-356 bare-board test netlist
- `Fabrication/Meridian-W104-PCB-Fabrication.zip`
- `Fabrication/Gerbers/` — individual plots, job and drill files
- `bom.csv`
- `PDFs/Meridian W104.pdf` — chematic page
- `PDFs/PCB Editor.pdf` — PCB layer pages
- `JOURNAL.md`

## cad

the case source is in **Fusion 360**, with a full `.step` export in `CAD/Full Meridian W104/`. only the five parts that need printing are in `CAD/Printing Files/`. all dimensions are millimetres; the largest part spans **466.15mm**, so the printer needs enough real usable bed area, including space for a brim.

## firmware note

the firmware is **CircuitPython** with a custom serial-matrix scanner. the normal files are `boot.py`, `code.py`, `scanner.py` and `keymap.py`; `matrix_diagnostic.py` is the separate bring-up tool.

install the official [XIAO nRF52840 CircuitPython build](https://circuitpython.org/board/Seeed_XIAO_nRF52840_Sense/) after checking that page's bootloader prerequisite, then copy the four normal files and `adafruit_ble`, `adafruit_hid` plus their dependencies from the matching [library bundle](https://circuitpython.org/libraries) to `CIRCUITPY`. the family download also covers the original non-Sense module used here.

usb insertion/removal selects the available transport. a short press and release of the rear mode button toggles USB/BLE; holding it for five seconds clears BLE bonding. the advertised name is **Meridian W104**. reports support six ordinary keys plus modifiers. test the diagnostic with all 104 real switches before closing the case; simulation is already passing, but soldered hardware still needs bring-up.

## bom (summary)

full BOM is in `bom.csv`. these are recorded carts, supplier listings and a PCB quote, **not a record of paid orders**. prices below are totals for each row, including the stated retailer packs; the CSV notes explain fitted quantities and spares.

| # | Name | Purpose | Qty | Cost (INR) | Cost ($) | Distributor | Link |
|---|---|---|---:|---:|---:|---|---|
| 1 | XIAO nRF52840 non-Plus | BLE / USB controller and module charger | 1 | 1,451.00 | 15.06 | LionCircuits | [View](https://www.lioncircuits.com/parts/102010448) |
| 2 | SN74HC595D SOIC-16 | 6 row sink outputs | 1 | 32.20 | 0.33 | KTRON | [View](https://www.ktron.in/product/74hc595d-8-bit-shift-register-ic-smd/) |
| 3 | SN74HC165D SOIC-16 | 22 column samples | 3 | 59.40 | 0.62 | KTRON | [View](https://www.ktron.in/product/74hc165d-ic-8-bit-shift-register-soic-16-nxp/) |
| 4 | Cherry MX PCB-pattern switch, 5-pin | Soldered keys | 104 | 3,850.00 | 39.96 | StacksKB | [View](https://stackskb.com/store/menel-eight-nine-haku-linear-switch-pack-of-10/) |
| 5 | 1N4148W SOD-123 | Per-key isolation | 104 | 108.16 | 1.12 | Robu | [View](https://robu.in/product/1n4148w-slkor-75v-1v-4ns-150ma-sod-123-switching-diodes-rohs/) |
| 6 | 22k 0805 1% resistor | Column bias | 22 | 10.08 | 0.10 | Robu | [View](https://robu.in/product/ac0805fr-0722kl-yageo-res-thick-film-0805-22k-ohm-1-0-125w1-8w-%c2%b1100ppm-c-pad-smd-t-r-automotive-aec-q200/) |
| 7 | 1k 0805 resistor | Lock indicator current limit | 3 | 13.80 | 0.14 | Robu | [View](https://robu.in/product/rc0805jr-071kl-yageo-res-thick-film-0805-1k-ohm-5-0-125w1-8w-%c2%b1100ppm-c-pad-smd-t-r/) |
| 8 | 100k 0805 resistor | Row output enable default OFF | 1 | 13.50 | 0.14 | Robu | [View](https://robu.in/product/0805w8f1003t5e-uniohm-royal-ohm-125mw-thick-film-resistors-150v-%c2%b1100ppm-%e2%84%83%c2%b11-100k%cf%89-0805-chip-resistor-surface-mount-rohs/) |
| 9 | 100n 0805 X7R, 10V or above | Logic decoupling | 4 | 30.00 | 0.31 | Flyrobo | [View](https://www.flyrobo.in/0805-100nf-50v-chip-capacitors) |
| 10 | 10u 0805 X5R, 10V or above | Rail bulk capacitor | 1 | 10.60 | 0.11 | Robu | [View](https://robu.in/product/08053d106kat2a-kyocera-avx-smd-multilayer-ceramic-capacitor-10-%c2%b5f-25-v-0805-2012-metric-%c2%b1-10-x5r/) |
| 11 | 3mm LED, diffused, Vf compatible with 3.3V | Caps / Num / Scroll indicators | 3 | 18.80 | 0.20 | KTRON | [View](https://www.ktron.in/product/red-led-red-diffusion-3mm-th/) |
| 12 | JST PH S2B-PH-K horizontal 2-pin | Battery connector | 1 | 16.00 | 0.17 | Robu | [View](https://robu.in/product/s2b-ph-klfsn-jst-1x2p-2p-ph-tin-2-25%e2%84%8385%e2%84%83-2a-1-2mm-brass-bend-insert-push-pullp2mm-wire-to-board-connector-rohs/) |
| 13 | PCM12-pattern SMD SPDT slide switch | Battery disconnect | 1 | 66.00 | 0.68 | Robu | [View](https://robu.in/product/pcm12smtr-ck-standing-paste-single-pole-double-throw-spdt-6v-smd-slide-switches-rohs/) |
| 14 | 6mm THT tactile pushbutton | Transport toggle / bond reset | 1 | 3.00 | 0.03 | Tomson | [View](https://www.tomsonelectronics.com/products/tactile-push-button-micro-switch-6x6x4-3mm) |
| 15 | Protected 3.7V 500mAh LiPo 502248P (bare leads) | Wireless power; maximum assembled envelope 60x28x6mm | 1 | 299.00 | 3.10 | Probots | [View](https://probots.co.in/3-7v-500mah-lipo-battery-502248-open-ended.html) |
| 16 | JST-PH2.0 2-pin female pigtail to bare wire | Adapt protected bare-lead battery to J1 | 1 | 4.13 | 0.04 | Hubtronics | [View](https://hubtronics.in/connectors/relimate_connectors/board_to_wire_relimate/1508) |
| 17 | 7-pin 2.54mm headers | Module mounting; two rows | 2 | 40.00 | 0.42 | Flyrobo | [View](https://www.flyrobo.in/40-pin-male-header-connector-strip-breakable-5pcs) |
| 18 | Flexible insulated wire | Module underside BAT+ / BAT- leads | 2 | 24.00 | 0.25 | Robu | [View](https://robu.in/product/high-quality-ultra-flexible-28awg-silicone-wire-1000m-red/) |
| 19 | ANSI 104-key MX keycap set | User keycaps; 6.25u spacebar | 1 | 1,000.00 | 10.38 | StacksKB | [View](https://stackskb.com/store/stackspbt-blank-white-cherry-profile-keycaps-113-key/) |
| 20 | Durock V2 PCB screw-in stabilizer kit (7x2U + 1x6.25U) | Seven wide keys and 6.25U spacebar | 1 | 2,365.00 | 24.54 | StacksKB | [View](https://stackskb.com/store/durock-clear-screw-in-stabilizers-v2/?attribute_combination=7%2B1+Set&attribute_spacebar-size=6.25U) |
| 21 | M3x30mm DIN912 socket-head SS304 screws (10pc pack) | 3 concealed rear mounts | 1 | 116.00 | 1.20 | RPI Shop | [View](https://rpishop.in/products/ss-allen-cap-m3?variant=45146051510424) |
| 22 | M3x15mm DIN912 socket-head SS304 screws (10pc pack) | 3 concealed front mounts | 1 | 88.00 | 0.91 | RPI Shop | [View](https://rpishop.in/products/ss-allen-cap-m3?variant=45146051412120) |
| 23 | M3x20mm DIN912 socket-head SS304 screws (10pc pack) | 1 concealed centre mounts | 1 | 92.00 | 0.95 | RPI Shop | [View](https://rpishop.in/products/ss-allen-cap-m3?variant=45146051444888) |
| 24 | M3 insert assortment; select 5mm long x4.2mm OD | Seven top-frame bosses, 3.9mm pilot holes | 1 | 1,519.00 | 15.76 | Robu | [View](https://robu.in/product/brass-heat-set-insert-nut-hot-melt-knurled-threaded-m3-400pcs-kit/) |
| 25 | Meridian W104 four-layer PCB, 1.6mm | Final checked four-layer Gerber and drill package | 5 | 8,647.58 | 89.25 | JLCPCB | [View](https://cart.jlcpcb.com/shopcart/cart/) |
| 26 | Printed case set | Bottom, plate, top frame, seam accent, mode button | 1 | 0.00 | 0.00 | Printing Legion | [View](https://printlegion.hackclub.com/) |

**listed BOM total : ₹19,877.25 / $205.77**

---

