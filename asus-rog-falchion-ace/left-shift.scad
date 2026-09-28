// ============================================================================
//  ASUS ROG Falchion Ace - LEFT SHIFT, ISO/ITA 1.25u
//  ZXCV row. NOT stabilised (unlike the ANSI 2.25u left Shift): on ISO the
//  1.25u Shift sits next to the extra <>| key, confirmed on the product photo.
// ============================================================================

include <../lib/keycap_common.scad>
include <./profile.inc.scad>

units        = 1.25;        // [SRC] ISO left Shift is 1.25u
h_center     = fa_h(4);      // [EST] ZXCV row
row_tilt     = fa_tilt(4);   // [EST]
legend_mode  = "emboss";    // raised: a tactile marker on a modifier

render_keycap()
    emboss_2d(cx = 0, cy = 0, h = 0.40)
        arrow_up_2d(w = 5.4, h = 6.2, shaft = 2.4);
