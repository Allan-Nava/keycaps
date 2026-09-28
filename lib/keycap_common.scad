// ============================================================================
//  keycap_common.scad  -  shared geometry for 3D-printed replacement keycaps
//
//  Include this FIRST, then override any parameter below, then call
//  render_keycap().  OpenSCAD resolves each name to its LAST assignment in the
//  file scope, so an override placed after the include also reaches the
//  derived values computed here.
//
//      include <../lib/keycap_common.scad>
//      units = 2.25;  h_center = 10.65;  ...
//      render_keycap();
//
//  Conventions
//    millimetres; origin at the key centre; z = 0 at the bottom rim of the
//    skirt; +Y towards the back of the keyboard; +X to the right.
//
//  Every dimension in a keycap file carries a provenance tag:
//    [SRC] from an online source   [DER] derived from a [SRC] value
//    [EST] estimate / closest standard value, NOT verified for that board
//    [FIT] fit-critical AND unverifiable online - measure the original cap
// ============================================================================

$fn = 96;

// ---------------------------------------------------------------- switches --
print_orientation = false;   // true = flipped + levelled, ready for the slicer
stab_style        = "none";  // "none" | "costar"   (see NOTE at the bottom)

// ------------------------------------------------------- outside of the cap --
U            = 19.05;   // [SRC] 1u pitch, ANSI standard
units        = 1.00;    // key width in units
key_gap      = 0.96;    // gap between adjacent caps, along X
key_gap_y    = 0.95;    // gap between adjacent caps, along Y
body_x       = units*U - key_gap;
body_y       = U       - key_gap_y;

h_center     = 10.65;   // top plate height at the key centre
row_tilt     = 6;       // deg, back edge higher
taper        = 2.10;    // per-side inset of the top plate
r_bot        = 1.20;    // plan corner radius at the skirt
r_top        = 2.60;    // plan corner radius at the top plate
bevel        = 0.60;    // chamfer where the top plate meets the walls
dish_r       = 28.0;    // cylindrical dish radius, axis along X
dish_depth   = 1.05;    // sag at the centre

// ------------------------------------------------------------ wall / shell --
wall         = 1.55;    // side wall, horizontal measure
wall_skirt   = 1.15;    // thinner near the rim, so the interior is never
                        // tighter than a stock OEM cap around the switch
skirt_z      = 4.20;    // the thin skirt ends here ...
skirt_blend  = 0.80;    // ... and blends back to `wall` over this height
roof         = 1.70;    // roof thickness under the dish

// ------------------------------------------- MX-compatible cross stem -------
stem_od      = 5.60;    // stem boss OD; stock is ~5.5
stem_z0      = 0.50;    // bottom face of the stem boss above the rim
cross_w      = 4.10;    // [SRC] Cherry MX stem cross: 4.1 mm across
cross_t      = 1.17;    // [SRC] Cherry MX stem cross: 1.17 mm thick
cross_clr_w  = 0.12;    // FDM tolerance added on the 4.1 mm direction
cross_clr_t  = 0.22;    // FDM tolerance added on the 1.17 mm direction
cross_depth  = 4.30;    // socket depth (an MX stem is ~3.7 mm tall)
cross_lead   = 0.45;    // chamfered lead-in at the socket mouth

// ------------------------------------------------ Costar wire stabiliser ----
stab_units   = 1.25;    // [SRC] 2u stabiliser mounts sit 1.25u apart
stab_x       = stab_units*U/2;
stab_wire_d  = 1.30;    // wire diameter assumed
wire_z       = 4.20;    // [FIT] height of the wire stub above the keycap rim
bore_clr     = 0.35;    // clearance around the wire inside the hook
throat_w     = stab_wire_d - 0.10;   // snap-in throat: 0.1 mm of interference
throat_grip  = 0.60;    // straight (gripping) length below the bore
hook_len     = 6.00;    // hook block length along X
hook_w       = 5.50;    // hook block width along Y
hook_z0      = 2.60;    // bottom face of the hook block above the rim

// ------------------------------------------------------------ stiffeners ----
rib_t        = 1.20;    // diagonal rib thickness
rib_len      = 10.0;    // rib length from the key centre outwards
rib_z0       = 5.00;    // ribs start this high, so the switch top housing and
                        // any in-switch LED stay clear

// ============================================================================
//  helpers
// ============================================================================

module prof(w, d, rr) {
    rr2 = min(rr, min(w, d)/2 - 0.01);
    offset(r = rr2) square([w - 2*rr2, d - 2*rr2], center = true);
}

h_shoulder = h_center - bevel;                       // top bevel starts here
inset      = function (z) taper * z / h_shoulder;    // linear draft

module slab(w, d, rr, z, tilt = 0) {
    translate([0, 0, z]) rotate([tilt, 0, 0])
        linear_extrude(0.01) prof(w, d, rr);
}

// ---- solid outside shape (dish already cut) --------------------------------
module outer_solid() {
    difference() {
        hull() {
            slab(body_x, body_y, r_bot, 0);
            slab(body_x - 2*taper - 2*bevel, body_y - 2*taper - 2*bevel,
                 r_top, h_shoulder, row_tilt);
            slab(body_x - 2*taper, body_y - 2*taper, r_top, h_center, row_tilt);
        }
        rotate([row_tilt, 0, 0])
            translate([0, 0, h_center + dish_r - dish_depth])
                rotate([0, 90, 0])
                    cylinder(h = 4*body_x + 40, r = dish_r, center = true);
    }
}

// ---- interior cavity -------------------------------------------------------
module inner_prism(w, zlo, zhi) {
    hull() {
        slab(body_x - 2*inset(zlo) - 2*w, body_y - 2*inset(zlo) - 2*w,
             max(r_bot - w, 0.3), zlo);
        slab(body_x - 2*inset(zhi) - 2*w, body_y - 2*inset(zhi) - 2*w,
             max(r_top - w, 0.3), zhi);
    }
}

module cavity() {
    zlo = -3;
    zhi = h_center + 9;
    union() {
        intersection() {
            inner_prism(wall, zlo, zhi);
            translate([0, 0, -roof]) outer_solid();
        }
        // thin skirt near the rim, blending back to the full wall
        hull() {
            slab(body_x - 2*inset(zlo) - 2*wall_skirt,
                 body_y - 2*inset(zlo) - 2*wall_skirt,
                 max(r_bot - wall_skirt, 0.3), zlo);
            slab(body_x - 2*inset(skirt_z) - 2*wall_skirt,
                 body_y - 2*inset(skirt_z) - 2*wall_skirt,
                 max(r_bot - wall_skirt, 0.3), skirt_z);
            // ends strictly inside the main cavity, so the two surfaces cross
            // transversally instead of touching tangentially
            slab(body_x - 2*inset(skirt_z + skirt_blend) - 2*(wall + 0.25),
                 body_y - 2*inset(skirt_z + skirt_blend) - 2*(wall + 0.25),
                 max(r_bot - wall - 0.25, 0.3), skirt_z + skirt_blend);
        }
    }
}

// ---- MX cross socket -------------------------------------------------------
module cross_prism(extra, zlo, h) {
    translate([0, 0, zlo]) linear_extrude(h) union() {
        square([cross_w + cross_clr_w + extra, cross_t + cross_clr_t + extra],
               center = true);
        square([cross_t + cross_clr_t + extra, cross_w + cross_clr_w + extra],
               center = true);
    }
}

module cross_cut() {
    hull() {   // chamfered mouth
        cross_prism(2*cross_lead, stem_z0 - 0.6, 0.01);
        cross_prism(0,            stem_z0 + cross_lead, 0.01);
    }
    cross_prism(0, stem_z0 - 0.61, cross_depth + 0.61);
}

module stem_boss() {
    intersection() {
        translate([0, 0, stem_z0]) cylinder(h = 30, d = stem_od);
        outer_solid();
    }
}

// ---- Costar hook -----------------------------------------------------------
module hook_solid(sx) {
    intersection() {
        translate([sx - hook_len/2, -hook_w/2, hook_z0])
            cube([hook_len, hook_w, 30]);
        outer_solid();
    }
}

module hook_cut(sx) {
    bore = stab_wire_d + bore_clr;
    // through-bore along X: the wire stub may point inwards or outwards
    translate([sx, 0, wire_z]) rotate([0, 90, 0])
        cylinder(h = hook_len + 8, d = bore, center = true);
    // snap-in throat: straight where it grips, flared below as a lead-in
    translate([sx - (hook_len + 8)/2, -throat_w/2, wire_z - throat_grip])
        cube([hook_len + 8, throat_w, throat_grip + 0.01]);
    hull() {
        translate([sx - (hook_len + 8)/2, -throat_w/2, wire_z - throat_grip])
            cube([hook_len + 8, throat_w, 0.01]);
        translate([sx - (hook_len + 8)/2, -(throat_w + 1.6)/2, hook_z0 - 1.2])
            cube([hook_len + 8, throat_w + 1.6, 0.01]);
    }
}

// ---- diagonal stiffening ribs ---------------------------------------------
module ribs() {
    for (a = [45, 135, 225, 315])
        intersection() {
            rotate([0, 0, a])
                translate([0, -rib_t/2, rib_z0]) cube([rib_len, rib_t, 30]);
            outer_solid();
        }
}

// ---- relief legend ---------------------------------------------------------
//  Takes a 2-D child and lays it on the top surface as raised relief, rooted
//  0.30 mm into the roof so it fuses instead of floating.
module emboss_2d(cx = 0, cy = 0, h = 0.45, grow = 0.25) {
    intersection() {
        translate([cx, cy, 0]) linear_extrude(40) offset(r = grow) children();
        difference() {
            translate([0, 0,  h   ]) outer_solid();
            translate([0, 0, -0.30]) outer_solid();
        }
    }
}

module arrow_up_2d(w = 5.2, h = 6.0, shaft = 2.4) {
    polygon([[0, h/2], [-w/2, h/2 - w/2], [-shaft/2, h/2 - w/2],
             [-shaft/2, -h/2], [shaft/2, -h/2], [shaft/2, h/2 - w/2],
             [w/2, h/2 - w/2]]);
}

// ============================================================================
//  the keycap
// ============================================================================
module keycap() {
    difference() {
        union() {
            difference() { outer_solid(); cavity(); }
            stem_boss();
            ribs();
            if (stab_style == "costar") { hook_solid(stab_x); hook_solid(-stab_x); }
            children();                       // legends and any extra relief
        }
        cross_cut();
        if (stab_style == "costar") { hook_cut(stab_x); hook_cut(-stab_x); }
    }
}

module render_keycap() {
    if (print_orientation)
        // top plate down on the bed, levelled: no supports needed anywhere
        rotate([180 - row_tilt, 0, 0]) keycap() children();
    else
        keycap() children();
}

// Machine-readable parameter dump, consumed by tools/scadparams.py so the
// Python tooling never has to mirror these numbers by hand.
echo("##PARAM", "U", U);                     echo("##PARAM", "units", units);
echo("##PARAM", "body_x", body_x);           echo("##PARAM", "body_y", body_y);
echo("##PARAM", "h_center", h_center);       echo("##PARAM", "row_tilt", row_tilt);
echo("##PARAM", "taper", taper);             echo("##PARAM", "bevel", bevel);
echo("##PARAM", "r_bot", r_bot);             echo("##PARAM", "r_top", r_top);
echo("##PARAM", "dish_r", dish_r);           echo("##PARAM", "dish_depth", dish_depth);
echo("##PARAM", "wall", wall);               echo("##PARAM", "wall_skirt", wall_skirt);
echo("##PARAM", "skirt_z", skirt_z);         echo("##PARAM", "roof", roof);
echo("##PARAM", "stem_od", stem_od);         echo("##PARAM", "stem_z0", stem_z0);
echo("##PARAM", "cross_w", cross_w);         echo("##PARAM", "cross_t", cross_t);
echo("##PARAM", "cross_clr_w", cross_clr_w); echo("##PARAM", "cross_clr_t", cross_clr_t);
echo("##PARAM", "cross_depth", cross_depth); echo("##PARAM", "stab_style", stab_style);
echo("##PARAM", "stab_x", stab_x);           echo("##PARAM", "stab_wire_d", stab_wire_d);
echo("##PARAM", "wire_z", wire_z);           echo("##PARAM", "bore_clr", bore_clr);
echo("##PARAM", "throat_w", throat_w);       echo("##PARAM", "hook_len", hook_len);
echo("##PARAM", "hook_w", hook_w);           echo("##PARAM", "hook_z0", hook_z0);
echo("##PARAM", "rib_t", rib_t);             echo("##PARAM", "rib_z0", rib_z0);

// NOTE on stabiliser styles
//   "costar"  - wire stabiliser, integrated hooks (Ozone Strike Battle, Filco,
//               most older TKLs). Implemented above.
//   "cherry"  - clip-in plastic stabiliser stems (most modern boards, and very
//               likely the ASUS ROG Falchion Ace). NOT implemented: the housing
//               and stem dimensions have to be measured or sourced first.
//               Do not fake it - a wrong stabiliser stem binds the key.
