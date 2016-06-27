var svg_vtx = d3.select('svg#vtx');
var svg_v2x = d3.select('svg#v2x');
var svg_xall = d3.select('svg#xall');
var svg_e2f = d3.select('svg#e2f');
var svg_bix = d3.select('svg#bix');
var svg_ccen = d3.select('svg#ccen');
var svg_logo = d3.select('svg#logo');

var regular_line = {"stroke-width": "2px", stroke: "#eee", fill: "#22aaee"};
var dashed_line = {"stroke-dasharray": "5 5", "stroke-width": "2px", stroke: "#eee"};
var new_vertex = {'stroke-width': '1px', 'stroke': '#222', fill: "#aaeeaa"};
var existing_vertex = {'stroke-width': '1px', 'stroke': '#eee', fill: "#ee8844"};
var nofill_regular = {"stroke-width": "2px", stroke: "#eee", fill: "none"}
var nofill_new = {"stroke-width": "2px", stroke: "#000eaa", fill: "none"}
var nofill_dashed = {"stroke-width": "2px", "stroke-dasharray": "5 5", stroke: "#eee", fill: "none"}

function draw_lines(destination, path, translate, style){
    var geom = destination.append('path');
    geom.attr("d", path)
    geom.attr({transform: "translate(" + translate  + ")"})
    geom.style(style)
}

function draw_dots(destination, locations, translate, style, rad){
    counter = locations.length;
    rad = rad || 4;
    for (var i=0; i<counter; i+=1){
        var loc = locations[i];
        var geom = destination.append('circle');
        geom.attr({'r': rad, 'cx': loc[0], 'cy': loc[1]})
        geom.attr({transform: "translate(" + translate  + ")"})
        geom.style(style)
    }
}

// LOGO
var dots = [[24.319, 28.056], [40.355, 28.056], [40.355, 12.02], [24.319, 12.02], [4.319, 28.056], [20.355, 28.056], [20.355, 12.02], [4.319, 12.02], [64.319, 28.056], [80.355, 28.056], [80.355, 12.02], [64.319, 12.02], [44.319, 28.056], [60.355, 28.056], [60.355, 12.02], [44.319, 12.02], [132.337, 28.056], [132.337, 12.02], [120.354, 12.02], [104.319, 12.02], [84.319, 28.056], [100.355, 28.056], [112.337, 12.02], [112.337, 28.056], [144.319, 28.056], [160.354, 28.056], [160.354, 12.02], [144.319, 12.02], [172.337, 28.056], [180.354, 12.02], [164.319, 12.02], [12.337, 28.056], [24.319, 20.038], [44.319, 20.038], [32.337, 20.038], [60.355, 20.038], [64.319, 20.038], [80.355, 20.038], [172.337, 20.038], [207.597, 27.259], [207.597, 4.777], [241.194, 27.259], [241.194, 4.777], [213.155, 27.259], [235.637, 27.259], [224.396, 4.777], [185.115, 18.646], [193.729, 27.259], [185.771, 21.942], [187.638, 24.736], [190.433, 26.604], [193.729, 4.777], [185.115, 13.391], [190.433, 5.433], [187.638, 7.3], [185.771, 10.095], [263.676, 18.646], [255.062, 27.259], [263.02, 21.942], [261.153, 24.736], [258.359, 26.604], [263.676, 13.391], [255.062, 4.777], [263.02, 10.095], [261.153, 7.3], [258.359, 5.433]];

var lines = [[[112.337, 28.056], [112.337, 12.02]], [[32.337, 20.038], [24.319, 20.038]], [[4.319, 12.02], [4.319, 28.056]], [[60.355, 28.056], [44.319, 28.056]], [[40.355, 12.02], [24.319, 12.02]], [[60.355, 20.038], [44.319, 20.038]], [[40.355, 28.056], [24.319, 28.056]], [[60.355, 12.02], [44.319, 12.02]], [[164.319, 12.02], [172.337, 20.038]], [[180.354, 12.02], [172.337, 20.038]], [[172.337, 28.056], [172.337, 20.038]], [[213.155, 27.259], [224.396, 4.777]], [[112.337, 12.02], [104.319, 12.02]], [[100.355, 28.056], [84.319, 28.056]], [[241.194, 27.259], [241.194, 4.777]], [[24.319, 20.038], [24.319, 12.02]], [[60.355, 28.056], [60.355, 20.038]], [[20.355, 28.056], [20.355, 12.02]], [[64.319, 20.038], [64.319, 12.02]], [[80.355, 20.038], [80.355, 12.02]], [[44.319, 20.038], [44.319, 12.02]], [[80.355, 28.056], [80.355, 20.038]], [[132.337, 28.056], [132.337, 12.02]], [[235.637, 27.259], [213.155, 27.259]], [[160.354, 28.056], [144.319, 12.02]], [[120.354, 12.02], [112.337, 12.02]], [[144.319, 28.056], [144.319, 12.02]], [[160.354, 12.02], [160.354, 28.056]], [[235.637, 27.259], [224.396, 4.777]], [[80.355, 20.038], [64.319, 20.038]], [[64.319, 28.056], [64.319, 20.038]], [[20.355, 12.02], [12.337, 28.056]], [[4.319, 12.02], [12.337, 28.056]], [[24.319, 28.056], [24.319, 20.038]], [[185.115, 18.646], [185.771, 21.942]], [[185.771, 21.942], [187.638, 24.736]], [[187.638, 24.736], [190.433, 26.604]], [[190.433, 26.604], [193.729, 27.259]], [[193.729, 4.777], [190.433, 5.433]], [[190.433, 5.433], [187.638, 7.3]], [[187.638, 7.3], [185.771, 10.095]], [[185.771, 10.095], [185.115, 13.391]], [[263.676, 18.646], [263.02, 21.942]], [[263.02, 21.942], [261.153, 24.736]], [[261.153, 24.736], [258.359, 26.604]], [[258.359, 26.604], [255.062, 27.259]], [[263.676, 13.391], [263.02, 10.095]], [[263.02, 10.095], [261.153, 7.3]], [[261.153, 7.3], [258.359, 5.433]], [[258.359, 5.433], [255.062, 4.777]], [[185.115, 18.646], [185.115, 13.391]], [[193.729, 27.259], [207.597, 27.259]], [[193.729, 4.777], [207.597, 4.777]], [[263.676, 18.646], [263.676, 13.391]], [[255.062, 27.259], [241.194, 27.259]], [[255.062, 4.777], [241.194, 4.777]]];

function smooth(coords, amp){
    var frump = [];
    for (var i=0; i<coords.length; i+=1){
        var c = coords[i]
        frump.push([c[0]*amp, c[1]*amp])
    }
    return frump
}

function uppercut(lines, amp){
    var fk = ""
    for (var i=0; i<lines.length; i+=1){
      var seg = lines[i];
      var modified = smooth(seg, amp);
      fk += ('M' + modified[0] + ' ' + modified[1])
    }
    return fk
}

var dots_modded = smooth(dots, 2.6);
var edges = uppercut(lines, 2.6);
console.log(edges)
draw_lines(svg_logo, edges, [25, 5], nofill_regular)
draw_dots(svg_logo, dots_modded, [25, 5], new_vertex, 1)
// V T X 

// T
var path = "M 50 50 50 100 M 0 0 100 0";
draw_lines(svg_vtx, path, [205, 5], regular_line)
var path2 = "M 50 50 50 0";
draw_lines(svg_vtx, path2, [205, 5], dashed_line)
draw_dots(svg_vtx, [[0, 0],[100,0],[50,50],[50,100]], [205, 5], existing_vertex)
draw_dots(svg_vtx, [[50, 0]], [205, 5], new_vertex)

// X
var path3 = "M 0 0 100 100 M 100 0 0 100";
draw_lines(svg_vtx, path3, [345, 5], regular_line)
draw_dots(svg_vtx, [[0, 100],[0,0],[100,0],[100,100]], [345, 5], existing_vertex)
draw_dots(svg_vtx, [[50, 50]], [345, 5], new_vertex)

// V
var path4 = "M 0 0 25 50 M 75 50 100 0";
draw_lines(svg_vtx, path4, [65, 5], regular_line)
var path5 = "M 25 50 50 100 M 50 100 75 50";
draw_lines(svg_vtx, path5, [65, 5], dashed_line)
draw_dots(svg_vtx, [[25, 50],[0,0],[75,50],[100,0]], [65, 5], existing_vertex)
draw_dots(svg_vtx, [[50, 100]], [65, 5], new_vertex)

// V 2 X

var path6 = "M 0 0 25 50 M 75 50 100 0";
draw_lines(svg_v2x, path6, [65, 5], regular_line)
// draw_lines(svg_v2x, path5, [65, 5], dashed_line)
draw_dots(svg_v2x, [[25, 50],[0,0],[75,50],[100,0]], [65, 5], existing_vertex)
draw_dots(svg_v2x, [[50, 100]], [65, 5], new_vertex)

// XALL

var path7 = "M 0 0 100 100 M 50 0 150 100 M 100 0 200 100 M 150 0 250 100 M 0 100 250 0";
draw_lines(svg_xall, path7, [65, 5], regular_line)
draw_dots(svg_xall, [
  [0,0],[50,0],[100,0],[150,0],
  [0,100],[100,100],[150,100],
  [200,100],[250,100],[250,0]], [65, 5], existing_vertex)
draw_dots(svg_xall, [[72,71],[108,57],[143,43],[180,28]], [65, 5], new_vertex)

// E2F

var path8 = "M 0 0 50 25";
draw_lines(svg_e2f, path8, [65, 5], regular_line)
var path9 = "M 100 0 200 0 150 100 50 100 z"
draw_lines(svg_e2f, path9, [65, 5], regular_line)
var path10 = "M 50 25 100 50";
draw_lines(svg_e2f, path10, [65, 5], dashed_line)
draw_dots(svg_e2f, [
  [0, 0],[100,0],[200,0],[150,100],[50,100],[50,25]], [65, 5], existing_vertex)
draw_dots(svg_e2f, [[100, 50]], [65, 5], new_vertex)

// BIX

var path11 = "M 0 0 50 25 M 0 100 50 75";
draw_lines(svg_bix, path11, [65, 5], regular_line)
draw_lines(svg_bix, "M 0 50 150 50", [65, 5], dashed_line)
draw_dots(svg_bix, [[0,0], [0,100], [50,25], [50,75]], [65, 5], existing_vertex)
draw_dots(svg_bix, [[0,50], [150,50], [100,50]], [65, 5], new_vertex)

var path11 = "M 0 0 100 50 M 100 50 0 100";
draw_lines(svg_bix, path11, [325, 5], regular_line)
draw_lines(svg_bix, "M 0 50 150 50", [325, 5], dashed_line)
draw_dots(svg_bix, [[0,0], [0,100], [100,50]], [325, 5], existing_vertex)
draw_dots(svg_bix, [[0,50], [150,50]], [325, 5], new_vertex)

// CCEN

function make_circle(destination, r, translate, style){
    var ccen = destination.append('ellipse');
    ccen.attr({transform: "translate(" + translate + ")"})
    ccen.attr({rx: r, ry: r})
    ccen.style(style)
}

function make_points(r, num){
    var points = [];
    var theta = Math.PI / num * 2;
    for (var i=0; i<num; i+=1){
        points.push([Math.sin(theta * i) * r, Math.cos(theta * i) * r])
    }
    return points
}

function make_selection(source, indices){
  var take = [];
  var drop = [];
  for (var i=0; i<source.length; i+=1){
      if (indices.indexOf(i) >=0){
          take.push(source[i]);
      } else {
          drop.push(source[i]);
      }
  }
  return [take, drop]
}

var y_offset = 105
var y_jump = 180
function get_row(num){ return y_offset + (num * y_jump)}

make_circle(svg_ccen, 50,  [get_row(0), 55], nofill_regular)
make_circle(svg_ccen, 50,  [get_row(1), 55], nofill_dashed)
make_circle(svg_ccen, 50,  [get_row(2), 55], nofill_new)

var points = make_points(50, 22);
var degen = make_selection(points, [3, 6, 15]);
var degenerate = degen[0];
var invert_degenerate = degen[1];

draw_dots(svg_ccen, points, [get_row(0), 55], existing_vertex)

draw_dots(svg_ccen, degenerate, [get_row(1), 55], existing_vertex)

draw_dots(svg_ccen, degenerate, [get_row(2), 55], existing_vertex)
draw_dots(svg_ccen, invert_degenerate, [get_row(2), 55], new_vertex)