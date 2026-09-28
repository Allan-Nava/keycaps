// ============================================================================
//  Ozone Strike Battle - LEFT SHIFT, ANSI 2.25u (stabilised, Costar)
//  Cherry MX cross stem, Costar (Filco-style) wire stabiliser interface,
//  OEM-like sculpted profile, designed for FDM printing in PLA / PETG.
//
//  Provenance for every number is in ./README.md. Tags:
//    [SRC] from an online source   [DER] derived from a [SRC] value
//    [EST] estimate / closest standard value, NOT verified for this board
//    [FIT] fit-critical AND unverifiable online - measure the original cap
//
//  Render:  openscad -o out.stl -D 'print_orientation=true' left-shift.scad
// ============================================================================

include <../lib/keycap_common.scad>

legend_arrow = true;    // embossed up-arrow (Shift) on the top surface

// ------------------------------------------------------- outside of the cap --
units        = 2.25;    // [SRC] left Shift = 2.25u (Omnitype keycap size table)
key_gap      = 0.96;    // [DER] gap between adjacent caps; fits the review's
                        //       measured 51 mm right Shift (2.75u) and
                        //       118 mm spacebar (6.25u) on this keyboard
key_gap_y    = 0.95;    // [DER] same reasoning on the 1u axis

h_center     = 10.65;   // [EST] top plate height at the key centre; the review
                        //       measures this keyboard's caps at 9-11 mm
row_tilt     = 6;       // [EST] deg, back edge higher (OEM ZXCV row sculpt)
taper        = 2.10;    // [EST] per-side inset of the top plate (OEM-like draft)
r_bot        = 1.20;    // [EST] plan corner radius at the skirt
r_top        = 2.60;    // [EST] plan corner radius at the top plate
bevel        = 0.60;    // [EST] chamfer where the top plate meets the walls
dish_r       = 28.0;    // [EST] cylindrical dish radius, axis along X
dish_depth   = 1.05;    // [EST] sag at the centre; the dish runs off the edge

// ------------------------------------------------------------ wall / shell --
wall         = 1.55;    // [EST] side wall, horizontal measure (~1.51 normal)
wall_skirt   = 1.15;    // [EST] thinner near the rim, so the interior is never
                        //       tighter than a stock OEM cap around the switch
skirt_z      = 4.20;    // [EST]
skirt_blend  = 0.80;    // [EST]
roof         = 1.70;    // [EST] roof thickness under the dish

// ------------------------------------------------------------- Cherry MX ----
stem_od      = 5.60;    // [EST] stem boss OD; stock is ~5.5, kept small so the
                        //       in-switch LED at the north face stays clear
stem_z0      = 0.50;    // [EST] bottom face of the stem boss above the rim
cross_w      = 4.10;    // [SRC] Cherry MX stem cross: 4.1 mm across
cross_t      = 1.17;    // [SRC] Cherry MX stem cross: 1.17 mm thick
cross_clr_w  = 0.12;    // [EST] FDM tolerance added on the 4.1 mm direction
cross_clr_t  = 0.22;    // [EST] FDM tolerance added on the 1.17 mm direction
cross_depth  = 4.30;    // [EST] socket depth (MX stem is ~3.7 mm tall)
cross_lead   = 0.45;    // [EST] chamfered lead-in at the socket mouth

// ------------------------------------------------ Costar wire stabiliser ----
stab_style   = "costar";// [SRC] the Test-Gear review names Costar stabilisers
stab_units   = 1.25;    // [SRC] 2u stabiliser mounts are 1.25u apart
stab_wire_d  = 1.30;    // [SRC/EST] Costar 2u wire quoted at 1.2 mm; +0.1 margin
wire_z       = 4.20;    // [FIT] height of the wire stub above the keycap rim
                        //       *** MEASURE THIS ON THE ORIGINAL CAP ***
bore_clr     = 0.35;    // [EST] clearance around the wire inside the hook
throat_grip  = 0.60;    // [EST] straight (gripping) length below the bore
hook_len     = 6.00;    // [EST] hook block length along X
hook_w       = 5.50;    // [EST] hook block width along Y
hook_z0      = 2.60;    // [EST] bottom face of the hook block above the rim

// ------------------------------------------------------------ stiffeners ----
rib_t        = 1.20;    // [EST]
rib_len      = 10.0;    // [EST]
rib_z0       = 5.00;    // [EST] ribs start high enough to clear the MX top
                        //       housing and the in-switch LED

// ============================================================================
render_keycap() {
    if (legend_arrow)
        emboss_2d(cx = -13.5, cy = 0, h = 0.45)
            arrow_up_2d(w = 5.2, h = 6.0, shaft = 2.4);
}
