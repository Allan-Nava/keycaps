// ============================================================================
//  ASUS ROG Falchion Ace - G, 1u
//  Home row (ASDF). Legend engraved rather than raised: it is a key you type
//  on constantly, and a raised glyph is felt under the fingertip.
// ============================================================================

include <../lib/keycap_common.scad>
include <./profile.inc.scad>

units        = 1.00;
h_center     = fa_h(3);      // [EST] home row - the lowest row of the sculpt
row_tilt     = fa_tilt(3);   // [EST]
legend_mode  = "deboss";    // engraved 0.40 mm

render_keycap()
    engrave_2d(cx = 0, cy = 0, d = 0.40)
        text("G", size = 6.2, font = fa_font(),
             halign = "center", valign = "center");
