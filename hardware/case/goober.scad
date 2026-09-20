// Goober Rev A — millimetres. Engineering prototype; print fit coupon first.
// Parts: "base", "lid", "knob", "coupon", "assembly", "exploded".
part = "assembly";
$fn = 64;
pcb_w=80; pcb_h=96; pcb_t=1.6;
pcb_top=13; pcb_bottom=pcb_top-pcb_t;
plate_t=1.5; plate_top=18; plate_bottom=plate_top-plate_t;
hood_top=24; hood_front=32;
wall=2.5; floor_t=2.4; gap=.5;
switch_cut=14.10;
insert_hole=3.4; // Nominal for M2.5 insert, OD 3.8, length 4.0; test coupon.
holes=[[4,4],[76,4],[4,92],[76,92]];
keys=[for(r=[0:2],c=[0:2]) [40+(c-1)*19.05,44+r*19.05]];
oled=[27,18]; encoder=[62,20];

module rounded(w,h,r,z) {
    linear_extrude(z) hull() for(x=[r,w-r],y=[r,h-r]) translate([x,y]) circle(r=r);
}
module outside(h) {translate([-3,-3,0]) rounded(86,102,6,h);}
module inside(h) {translate([-.5,-.5,0]) rounded(81,97,3.5,h);}
module usb_cut() {
    // Large enough for plug overmould to reach the recessed module connector.
    translate([28,-1.75,5.8]) rotate([90,0,0])
        linear_extrude(8,center=true) hull()
            for(x=[-5.8,5.8],y=[-2.8,2.8]) translate([x,y]) circle(r=1.2);
}
module base() {
    difference() {
        union() {
            difference() {
                outside(plate_bottom);
                translate([0,0,floor_t]) inside(30);
            }
            for(p=holes) translate([p[0],p[1],floor_t]) cylinder(d=7,h=pcb_bottom-floor_t);
        }
        usb_cut();
        for(p=holes) {
            translate([p[0],p[1],floor_t+.5]) cylinder(d=2.8,h=20);
            translate([p[0],p[1],pcb_bottom-4.1]) cylinder(d=insert_hole,h=4.3);
        }
        // Feet recesses: adhesive 8-mm rubber feet, 0.6 mm deep.
        for(p=[[8,8],[72,8],[8,88],[72,88]]) translate([p[0],p[1],-.1]) cylinder(d=8.3,h=.7);
    }
}
module hood_outer() {translate([-3,-3,plate_top-.01]) rounded(86,hood_front+3,6,hood_top-plate_top+.01);}
module lid() {
    difference() {
        union() {
            difference() {
                union() {
                    translate([0,0,plate_bottom]) outside(plate_t);
                    hood_outer();
                }
                // Hollow control area, leaving a 1.5-mm roof and 2.5-mm walls.
                translate([-.5,-.5,plate_bottom-.1]) rounded(81,hood_front-2,3.5,hood_top-plate_t-plate_bottom+.1);
                for(p=keys) translate([p[0]-switch_cut/2,p[1]-switch_cut/2,plate_bottom-.1]) cube([switch_cut,switch_cut,2]);
                translate([oled[0]-14,oled[1]-4.5,hood_top-2]) cube([28,9,3]);
                translate([encoder[0],encoder[1],hood_top-2]) cylinder(d=8,h=3);
            }
            // Spacers set the MX plate top exactly 5 mm above PCB top.
            for(p=holes) translate([p[0],p[1],pcb_top]) cylinder(d=6.4,h=(p[1]<10?hood_top:plate_top)-pcb_top);
            // OLED pocket suspended below roof; open end for the PH connector.
            difference() {
                translate([oled[0]-20,oled[1]-8.6,18.3]) cube([40,17.2,4.2]);
                translate([oled[0]-18.3,oled[1]-6.55,19.1]) cube([36.6,13.1,5]);
                translate([oled[0]-17.3,oled[1]-5.55,18.2]) cube([34.6,11.1,1]);
                translate([oled[0]-20.1,oled[1]-4.5,18.2]) cube([4,9,3.1]);
                translate([oled[0]-14,oled[1]-4.5,18]) cube([28,9,8]);
            }
        }
        for(p=holes) translate([p[0],p[1],12]) cylinder(d=2.9,h=15);
        // Thin front identification engraving.
        translate([40,93.5,17.6]) linear_extrude(.5) mirror([0,1,0])
            text("goober",size=2.8,halign="center",valign="center",font="Helvetica:style=Bold");
    }
}
module knob() {
    difference() {
        union() {
            cylinder(d=20,h=14);
            for(a=[0:12:348]) rotate([0,0,a]) translate([9.7,0,1]) cylinder(d=.7,h=12);
        }
        // D shaft: 6.2-mm bore, flat 1.65 mm from centre; blind 12-mm depth.
        intersection() {
            translate([0,0,-.1]) cylinder(d=6.2,h=12.1);
            translate([-4,-4,-.1]) cube([5.65,8,12.1]);
        }
        translate([-.5,5.5,13.6]) cube([1,3,.6]);
    }
}
module coupon() {
    difference() {
        rounded(64,27,2,1.5);
        for(i=[0:2]) translate([3+i*19,3,-.1]) cube([13.9+i*.1,13.9+i*.1,2]);
    }
    for(i=[0:2]) translate([10+i*19,22,1.5]) linear_extrude(.35) text(str(13.9+i*.1),size=2.5,halign="center");
    translate([68,0,0]) difference() {
        rounded(14,27,2,6);
        for(i=[0:2]) translate([7,5+i*8,1]) cylinder(d=3.3+i*.1,h=6);
    }
}
module preview_components(explode=0, key_raise=0, control_raise=0) {
    color([.08,.3,.18]) translate([0,0,pcb_bottom+explode]) rounded(pcb_w,pcb_h,3,pcb_t);
    color([.13,.15,.18]) translate([19,0,7.4+explode]) cube([18,23.5,1]);
    color("silver") translate([23.6,-1.2,4.2+explode]) cube([8.8,7.5,3.2]);
    color([.1,.1,.13]) translate([9,11.75,19.1+control_raise]) cube([36,12.5,1.2]);
    color([.03,.06,.08]) translate([13,13.5,22.6+control_raise]) cube([28,9,.5]);
    color("white") translate([27,18,23.2+control_raise]) linear_extrude(.05) mirror([0,1,0]) text("GOOBER",size=2.8,halign="center",valign="center");
    for(i=[0:8]) {
        p=keys[i];
        color([.15,.15,.17]) translate([p[0]-7,p[1]-7,pcb_top+key_raise]) cube([14,14,5]);
        color([.3+.07*(i%3),.3+.06*i,.9-.08*i]) translate([p[0]-8.7,p[1]-8.7,plate_top+.5+key_raise]) rounded(17.4,17.4,1,1.5);
        color([.86,.85,.8]) translate([p[0],p[1],plate_top+2+key_raise]) hull() {
            translate([-8.5,-8.5,0]) rounded(17,17,1,.3);
            translate([-7.3,-7.3,7]) rounded(14.6,14.6,1,.3);
        }
    }
    color("silver") translate([encoder[0],encoder[1],26+control_raise]) knob();
}
module layout() {
if(part=="base") base();
else if(part=="lid") translate([0,0,-pcb_top]) lid();
else if(part=="knob") knob();
else if(part=="coupon") coupon();
else if(part=="exploded") {
    color([.15,.16,.18])base();
    color([.22,.23,.25])translate([0,0,35])lid();
    preview_components(15,50,35);
} else {
    color([.15,.16,.18])base();
    color([.22,.23,.25])lid();
    preview_components();
}

}
// KiCad plan coordinates: +Y runs down the page. Convert to CAD world.
if(part=="coupon" || part=="knob") layout();
else mirror([0,1,0]) layout();
