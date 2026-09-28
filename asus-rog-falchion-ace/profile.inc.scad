// ============================================================================
//  ASUS ROG Falchion Ace - shared profile for every key on this board.
//  Include AFTER ../lib/keycap_common.scad, then set the per-key values.
//
//  Provenance tags: [SRC] sourced · [DER] derived · [EST] estimate ·
//                   [FIT] fit-critical and unverifiable, measure it.
//  Full reasoning in ./README.md.
// ============================================================================

// -------------------------------------------------------------- the board --
// 65 %, 68 keys, ISO. ROG NX switches: "standard cross-shaped stem design
// ensures compatibility with most keycaps" [SRC, ASUS], so MX cross geometry
// applies. Per-key RGB comes from "centrally placed RGB LEDs" on the PCB
// shining through the hollow stem and the transparent upper housing [SRC,
// ASUS] - nothing protrudes into the keycap.
led_clear_h  = 0;       // [SRC] no in-switch LED to clear

// ------------------------------------------------------------ the profile --
// ASUS ships Cherry profile PBT doubleshot caps [SRC, reviews]. Cherry is
// cylindrical and "1-2 mm lower than OEM across all rows" - the one claim the
// sources agree on. Absolute per-row heights are NOT consistently documented
// (two guides disagree by 1.5 mm and even on which row is lowest), so:
//   * the ABSOLUTE height is anchored on 1.5 mm below this repo's own
//     validated OEM cap (ozone-strike-battle/left-shift, 11.39 mm overall);
//   * the row-to-row DELTA and the tilts come from the one internally
//     coherent source (home row lowest, tilt growing away from it).
// Everything here is therefore [EST]. It is cosmetic, not fit-critical.
//  Exposed as FUNCTIONS, not variables, on purpose: OpenSCAD will not resolve
//  an included file's VARIABLE inside an assignment in the including file
//  (it reports "Ignoring unknown variable" and yields undef), but it does
//  resolve an included FUNCTION. So a key file writes  h_center = fa_h(4);
//    row 3 = home row (ASDF)  -> ~8.50 mm overall
//    row 4 = ZXCV row         -> ~9.90 mm overall
function fa_h(row)    = row == 3 ?  7.99 : 8.52;   // [EST] top plate at centre
function fa_tilt(row) = row == 3 ?  5    : 12;     // [EST] deg, back edge up
function fa_font()    = "Helvetica:style=Bold";    // present on macOS

key_gap      = 0.95;    // [EST] no measured cap for this board; 18.10 mm for
key_gap_y    = 0.95;    // [EST] 1u is the common value for Cherry-profile sets
taper        = 2.10;    // [EST] per-side inset of the top plate
r_bot        = 1.20;    // [EST]
r_top        = 2.60;    // [EST]
bevel        = 0.60;    // [EST]

dish_axis    = "y";     // [EST] concave left-right, as on 1u / small-modifier
                        //       caps (a 2u+ key would use "x")
dish_r       = 25.0;    // [EST] chosen so the dish runs off the top plate edge
dish_depth   = 0.90;    // [EST] sag at the centre

// ------------------------------------------------------------ wall / shell --
wall         = 1.55;    // [EST]
wall_skirt   = 1.15;    // [EST] keeps the interior as roomy as a stock cap of
skirt_z      = 4.20;    // [EST] the same sculpt, right around the switch
skirt_blend  = 0.80;    // [EST]
roof         = 1.70;    // [EST]

// ------------------------------------------------------- MX / ROG NX stem --
stem_od      = 5.60;    // [EST] stock is ~5.5
stem_z0      = 0.50;    // [EST]
cross_w      = 4.10;    // [SRC] Cherry MX stem cross: 4.1 mm across
cross_t      = 1.17;    // [SRC] Cherry MX stem cross: 1.17 mm thick
cross_clr_w  = 0.12;    // [EST] FDM tolerance
cross_clr_t  = 0.22;    // [EST] FDM tolerance
cross_depth  = 4.30;    // [EST] ASUS advertises a "shorter stem" on ROG NX; a
                        //       deeper socket is harmless, a shallow one is not
cross_lead   = 0.45;    // [EST]

// ----------------------------------------------------------------- the rest --
stab_style   = "none";  // none of the three keys modelled here is stabilised
ribs_on      = false;   // a 1u / 1.25u roof is carried by four close walls
