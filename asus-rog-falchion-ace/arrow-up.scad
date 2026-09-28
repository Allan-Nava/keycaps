// ============================================================================
//  ASUS ROG Falchion Ace - UP ARROW, 1u
//  ZXCV row: on a 65 % the up arrow sits to the right of the right Shift, in
//  the same row as Z X C V - confirmed on the product photo.
// ============================================================================

include <../lib/keycap_common.scad>
include <./profile.inc.scad>

units        = 1.00;
h_center     = fa_h(4);      // [EST] ZXCV row, same sculpt as the left Shift
row_tilt     = fa_tilt(4);   // [EST]
legend_mode  = "emboss";    // raised: doubles as a tactile marker for the arrows

render_keycap()
    emboss_2d(cx = 0, cy = 0, h = 0.40)
        arrow_up_2d(w = 5.2, h = 6.0, shaft = 2.3);
