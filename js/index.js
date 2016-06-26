var svg_vtx = d3.select('svg#vtx');
var svg_v2x = d3.select('svg#v2x');
var svg_xall = d3.select('svg#xall');
var svg_e2f = d3.select('svg#e2f');
var svg_bix = d3.select('svg#bix');
var svg_ccen = d3.select('svg#ccen');

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

function draw_dots(destination, locations, translate, style){
    counter = locations.length;
    for (var i=0; i<counter; i+=1){
        var loc = locations[i];
        var geom = destination.append('circle');
        geom.attr({'r': 4, 'cx': loc[0], 'cy': loc[1]})
        geom.attr({transform: "translate(" + translate  + ")"})
        geom.style(style)
    }
}

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