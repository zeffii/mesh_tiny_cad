Blender CAD utils
=================

A tiny subset of unmissable CAD functions for Blender 3d.

### OK, what's this all about?

I'll try to keep this short as I'd rather be coding. There is certain functionality found in most dedicated CAD software that I can't live without, namely:  

  - Extend
  - Trim
  - Intersect / weld

For edges these functions exist as Python scripts, and i've bundled them here in the hope they might be useful to you or they might make you angry and you code nicer versions which I will then use instead :)

### Why on github?

The issue tracker, use it. Let me know if these things are broken in new releases. Why? I don't update Blender as often as some so am oblivious to the slow evolution. Secondly; the issue tracker. use it. If you can make a valid argument for extra functionality and it seems like something I might use or be able to implement for fun, it's going to happen. Thirdly, the issue tracker; use it. I'm always open to pull requests (just don't expect instant approval of something massive, we can talk..you can use your gift of persuasion and sharp objectivism)

### VTX

All the functions have low error margins, `1.5E-6` normally. These functions are not easy to describe hence pictures below:

  - V : extending two edges towards their _calculated_ intersection point.  
   ![V](http://i.imgur.com/83HcD51.png)

  - T : extending the path of one edge towards another edge.  
   ![T](http://i.imgur.com/h7oOwIr.png)  

  - X : two edges intersect, their intersection gets a weld vertex. You now have 4 edgse and 5 vertices.  
   ![X](http://i.imgur.com/kqtX9OE.png)



### X ALL

Intersect all, it programatically goes through all selected edges and slices them all using any found intersections, then welds them.

  - XALL is fast!  
  ![XALL](http://i.imgur.com/9po2kIV.gif)

### V2X (Vertex to Intersection)

This might be a niche accessory, but sometimes all you want is a vertex positioned on the intersection of two edges. Nothing fancy.

### Trim Multiples

Explained in the issue tracker with moving GIF: [issue3](https://github.com/zeffii/Blender_CAD_utils/issues/3)

### Extend Multiples

Explained in the issue tracker with moving GIF: [issue2](https://github.com/zeffii/Blender_CAD_utils/issues/2)
