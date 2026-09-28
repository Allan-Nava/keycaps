// ============================================================================
//  Ozone Strike Battle - LEFT SHIFT, ISO 1.25u  (ITA / UK / DE)
//
//  This is the variant that fits an ISO board: 1.25u, with the extra <>| key
//  next to it, and therefore NOT stabilised. The 2.25u ANSI left Shift and its
//  Costar wire interface live in left-shift-ansi.scad - the two are not
//  interchangeable.
//
//  Confirmed from the user's own keyboard: a <> key sits next to the left
//  Shift, and the Enter is the tall ISO L.
//
//  Everything except the width and the stabiliser is shared with the ANSI cap,
//  so the provenance of each dimension is the same - see ./README.md.
//    [SRC] sourced · [DER] derived · [EST] estimate · [FIT] measure it
//
//  Render:  openscad -o out.stl -D 'print_orientation=true' left-shift-iso.scad
// ============================================================================

include <../lib/keycap_common.scad>

// ------------------------------------------------------- outside of the cap --
units        = 1.25;    // [SRC] ISO left Shift is 1.25u
key_gap      = 0.96;    // [DER] same reconciliation as the ANSI cap: fits the
key_gap_y    = 0.95;    //       review's measured 51 mm right Shift / 118 mm space

h_center     = 10.65;   // [EST] ZXCV row, same sculpt as the ANSI left Shift
row_tilt     = 6;       // [EST] deg, back edge higher
taper        = 2.10;    // [EST]
r_bot        = 1.20;    // [EST]
r_top        = 2.60;    // [EST]
bevel        = 0.60;    // [EST]

dish_axis    = "y";     // [EST] concave left-right: at 1.25u this cap follows
                        //       the alphas, not the 2u+ rule the ANSI cap uses
dish_r       = 25.0;    // [EST] chosen so the dish runs off the top plate edge
dish_depth   = 1.05;    // [EST]

// ------------------------------------------------------------ wall / shell --
wall         = 1.55;    // [EST]
wall_skirt   = 1.15;    // [EST]
skirt_z      = 4.20;    // [EST]
skirt_blend  = 0.80;    // [EST]
roof         = 1.70;    // [EST]

// ------------------------------------------------------------- Cherry MX ----
stem_od      = 5.60;    // [EST] kept small so the in-switch LED stays clear
stem_z0      = 0.50;    // [EST]
cross_w      = 4.10;    // [SRC] Cherry MX stem cross: 4.1 mm across
cross_t      = 1.17;    // [SRC] Cherry MX stem cross: 1.17 mm thick
cross_clr_w  = 0.12;    // [EST] FDM tolerance
cross_clr_t  = 0.22;    // [EST] FDM tolerance
cross_depth  = 4.30;    // [EST]
cross_lead   = 0.45;    // [EST]

// ----------------------------------------------------------------- the rest --
stab_style   = "none";  // [SRC] a 1.25u key is never stabilised
ribs_on      = false;   // a 1.25u roof is carried by four close walls
led_clear_h  = 7.00;    // [SRC] this board IS backlit through the switch, so
                        //       the north LED column must stay clear
legend_mode  = "emboss";

render_keycap()
    emboss_2d(cx = 0, cy = 0, h = 0.45)
        arrow_up_2d(w = 5.4, h = 6.2, shaft = 2.4);
