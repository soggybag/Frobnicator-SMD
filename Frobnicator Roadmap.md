# Frobnicator SMD — notes, opinions and plan

Discussion 2026-09-29. Source: `~/Documents/eagle/projects/Frobnicator/Frobnicator.sch` (John Hollis design, user's Eagle build; boards ordered 2022–2023).

## How the original works (from the Eagle netlist)

- **VB = two LEDs in series** (D2 + D3) fed by R14 10k → about 3.6–3.8 V, not 4.5 V.
- **LFO (TL072):**
  - IC1A is a Schmitt trigger: − at VB, + gets R10 100k from its own output and R11 47k from the triangle. The triangle swings about ±0.47 × the square.
  - RATE (A100k, R9 4k7 to VB) divides the square → R12 220k → IC1B integrator.
  - **C6 2n2 is always there; C7 100n is added in parallel by the TREM switch.**
  - Estimated range: **LFO ≈ 1–24 Hz** (102n), **audio ≈ 50 Hz–1.1 kHz** (2n2). The ratio is 46×.
- **Control:** the triangle → DEPTH B10k (other end at VB) → R13 10k → **C5 100n to GND** → **LED D4** → D1 → 3080 Iabc (pin 5). The LED flashes at the LFO rate.
  - C5 with R13 is a **~160 Hz low-pass on the control current**. It rounds the modulation, and at audio rate it's what limits depth and brightness.
  - There's **no edge-softening cap on the Schmitt** in this circuit. The "softening" cap in the designer's notes is most likely C5, since that's where the square's edges get smoothed before the VCA (my reading, not confirmed).
- **VCA:** IN → C4 47n → R2 330k / R3 10k to VB (34× attenuation, so the 3080 sees a few mV) → 3080 + input.
  - TRIM (100k across the supply) → R6 10M nudges the + input to **null control bleed-through**.
  - − input: R5 10k to VB, R4 470k from the output. The output drives Q1 2N5089 as an emitter follower (R7 22k) → C3 1µ → OUT (R8 100k).
- **Power:** 1N5817 in series; power LED D6 (RLED 1k) on the footswitch LED pads.

## Replacing the 3080 — options

| Option | Pros | Cons | JLC |
|---|---|---|---|
| **LM13700 (½)** | The standard 3080 replacement: same OTA core. Its built-in Darlington buffer replaces Q1, and its **linearising diodes allow ~10× more input** (less noise, less distortion). The second half is free for something else. | Datasheet single-supply minimum is ~9.5 V; it works at 9 V in practice (Penfold) but it's out of spec, so bench-check. | C174050 (TI LM13700MX), extended; already used on Penfold |
| NJM13700 / AS13700 | Same as above, other makers | Availability varies | Check |
| AS3080 (Alfa reissue) | A true 3080 drop-in | Hobby-distributor part, probably not at JLC; 8-pin DIP | Unlikely |
| Discrete OTA (matched pairs + mirrors) | No special chip; the Trem's LM3086-style VCA is basically this | More parts, needs matching and a trim | Basic/cheap parts |
| SSM2164/V2164, THAT2180 | High-quality VCAs | Different (log) control, pricier, overkill | Extended/expensive |

**Opinion: use the LM13700.** It's the "modern 3080", keeps the Frobnicator's character, removes Q1 and the fussy 330k/10k attenuator balance, and is already a known part in our Penfold build. Use one half as the VCA with linearising diodes, and its buffer as the output.

**Using the second half:**
- Leave it unused (simplest), or
- a **second VCA fed the inverted LFO**, blended, for a harmonic-trem or panning flavour, or
- a voltage-controlled filter on the wet signal. That's feature creep; keep it for a v2.

## Is it worth its own project?

**Yes, as a small, simple pedal.** It sits next to the Trem SMD rather than replacing it:

- **Frobnicator SMD:** RATE, DEPTH, RANGE (LFO/AUDIO) toggle, and a rate LED. TL072 + LM13700, about 30 SMD parts, compact (1590B, same drilling family as the other pedals). A quick build with a distinct OTA sound and a proper audio-rate "pseudo ring mod".
- **Trem SMD v2:** keeps SHAPE and SQ/TRI, and gets the same RANGE idea (see `Trem SMD/Trem Roadmap.md`). The Frobnicator's 46× ratio confirms the Trem plan (470n → ~10n is 47×).

## Updates I'd make for the SMD version

1. **LM13700** in place of the 3080; linearising diodes; its buffer in place of Q1; input attenuation recalculated (about 10× more signal into the OTA).
2. **VB:** a 100k/100k divider + 10–22µ (4.5 V, centred swing), instead of the two-LED reference. The asymmetric 3.8 V reference skews the square and the triangle.
3. **C5 control smoothing:** switch it with RANGE (e.g. 100n in LFO, ~2n2 in AUDIO), or make it smaller overall. Otherwise the audio range gets dull and shallow above ~160 Hz.
4. **RANGE switch:** SPST adding C7 100n across C6 2n2, as the original. Use a DPDT if C5 switches too (or a CD4053 if more parts need switching).
5. **Bleed-through null:** keep a trimmer (on the LM13700's input offset), and note it on the silkscreen. It matters most in AUDIO mode.
6. **Rate LED:** keep it as a panel LED (THT, hand-soldered). Drive it from the control current, or from a separate op-amp/transistor so it doesn't sit in the VCA's control path.
7. Standard house style: SS14 in series, LED after the diode, 0805 parts, ribbon header centred on the footswitch, name + version on the front silkscreen.

## Road map

1. **Transcribe** the Eagle original into KiCad (faithful, netlist-checked), as with the Harmonic Energizer.
2. **Frobnicator SMD schematic:** the LM13700 changes above, reviewed together.
3. **Bench/breadboard check:** LM13700 at 9 V (headroom, noise), audio-range brightness with C5 switched, bleed-through null.
4. **PCB + JLC** (1590B).

## To-do

- [ ] Transcribe the Eagle Frobnicator (sch + brd) and net-check.
- [ ] Confirm what the original designer's "softening" note refers to (likely C5).
- [ ] Decide on a use for the second LM13700 half (none / inverted-LFO VCA / filter).
- [ ] Confirm LM13700 behaviour at 9 V after the SS14 (~8.7 V); consider a charge pump if headroom is poor.
- [ ] Choose C5 switching (DPDT vs fixed smaller value).
- [ ] Enclosure/drilling: 1590B, 2 knobs + toggle + rate LED.

## Decisions (2026-09-29)

- **OTA:** 3080 in a **DIP-8 socket** (the user has 3080s), plus an **LM13700 SOIC-16 footprint wired in parallel as a plain OTA** (no linearising diodes, buffers unused). Fit one. The LM13700 is left off the JLC BOM until the 3080s run out. Q1 stays as the output follower.
- **Bias:** replace the two-LED VB with a **TL431 shunt reference (CJ431, C3113, JLC basic) at ~4.5 V**. The LED pair's Vf varies with batch, current and light, and a 3.6 V VB lets the triangle dip below the TL072's specified input range, a likely cause of the intermittent LFO failures.

## Future ideas (user notes 2026-09-29)

- **What to do with the extra OTA when we move to a full LM13700 version.** Candidates:
  - A second VCA fed the inverted LFO and blended, for a harmonic-trem or panning flavour.
  - Stereo/ping-pong outputs.
  - A voltage-controlled low-pass on the wet signal, swept by the LFO.
  - A dual-OTA true ring modulator in AUDIO mode (the carrier suppressed rather than pseudo-ring).
  - Also use the linearising diodes (more input, less noise) and the built-in buffers (replace Q1).
- **Envelope-controlled rate** (like the Ugly Face envelope → frequency): an envelope follower on the input adds to the RATE control, so playing harder speeds the tremolo up (or slows it), with attack/release like the LDR feel. Could share an envelope-follower design with Ugly Face 4. Options: add the envelope voltage into the RATE divider, or modulate the integrator current with a transistor. Needs a SENS/amount control and possibly a direction switch.

## Open questions

- 2 knobs (RATE, DEPTH), or add SHAPE/waveform from the Trem?
- Rate LED: keep the flashing LED in the control path (original charm), or buffer it?

## Overlap with Trem v2 (2026-10-02)

- The Trem SMD's discrete VCA tested well. A Trem v2 with a RANGE (audio-rate) switch and a rate LED would cover the Frobnicator's features, plus SHAPE and SQ/TRI. This SMD version may be moot.
- Keep this on hold. Revisit if an A/B against the built original shows the 3080/LM13700 OTA character is worth its own pedal. See `Trem SMD/Trem Roadmap.md` and `Trem SMD/docs/VCA Building Block.md`.
