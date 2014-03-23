Blender CAD utils
=================

A tiny subset of unmissable CAD functions for Blender 3d.

### OK, what's this all about?

I'll try to keep this short as I'd rather be coding. There is certain functionality found in most dedicated CAD software that speed up drafting, namely: `Extend`, `Trim` and `Intersect / weld`. For edges these functions exist as Python scripts, and are bundled here in the hope that they might be as useful to you as they are to me.
  
The VTX script has lived in contrib distributions of Blender since 2010, with relatively minor changes. The feedback from BlenderArtists has been [overwhelmingly positive](http://blenderartists.org/forum/showthread.php?204836-CAD-Addon-Edge-Tools-(blender-2-6x)). I'm not going to claim it's bug free, but finding them has proven difficult.  
  
Todo:  

  - Trim multiple
  
Other features like `Fillet / Chamfer` and `Offset` are also catered for as scripts. [link here](http://blenderartists.org/forum/showthread.php?179375)
  
### Why on github?

The issue tracker, use it.  

-  Let me know if these things are broken in new releases. Why? I don't update Blender as often as some so am oblivious to the slow evolution. 
-  If you can make a valid argument for extra functionality and it seems like something I might use or be able to implement for fun, it's going to happen.
-  I'm always open to pull requests (just don't expect instant approval of something massive, we can talk..you can use your gift of persuasion and sharp objectivism)

### VTX

All the functions have low error margins (`1.5E-6` = tolerance) and are happy to operate on geometry that isn't flat on X,Y or Z. Expect full freedom of orientation, but stuff must really intersect within this tolerance. These functions are not easy to describe hence pictures below:

  - V : extending two edges towards their _calculated_ intersection point.  
   ![V](http://i.imgur.com/zBSciFf.png)

  - T : extending the path of one edge towards another edge.  
   ![T](http://i.imgur.com/CDH5oHm.png)

  - X : two edges intersect, their intersection gets a weld vertex. You now have 4 edges and 5 vertices.  
   ![X](http://i.imgur.com/kqtX9OE.png)

A note about usage: Once the operation completes, all geometry that was previously selected will now be separated from any surrounding geometry that it was attached to. This has pros and cons, but is ultimately due to weak initial algorithm design. I've started an [issue about this](https://github.com/zeffii/Blender_CAD_utils/issues/4).


### X ALL

Intersect all, it programatically goes through all selected edges and slices them all using any found intersections, then welds them.

  - XALL is fast!  
  ![XALL](http://i.imgur.com/9po2kIV.gif)

### V2X (Vertex to Intersection)

This might be a niche accessory, but sometimes all you want is a vertex positioned on the intersection of two edges. Nothing fancy.

### Trim Multiples

Explained in the issue tracker with moving GIF: [issue3](https://github.com/zeffii/Blender_CAD_utils/issues/3)

### Extend Multiples

This has now progressed to an addon called [EXM](https://github.com/zeffii/Blender_CAD_utils/tree/master/EXM)  
It has two modes.  
  -  Pick an edge (we'll call this Edge Prime)
  -  make sure only one edge is selected
  -  Run `extend edge` from spacebar menu
  -  Your picked edge has turned light blue
  -  Pick edges to extend towards that edge
  -  If edges are picked that don't intersect in 3d space (within tolerance) then those edges are not added
  -  Edges that do intersect will be shown in a different colour with the extended part in yet another colour
  -  You can unpick edges by clicking on them
  -  To finalize the operation:  
    - Press `Comma` to extend the edges using the vertex closest to the intersection point
    - Press `Period` to create a new edge attached to the original geometry.
  -  This addon does not weld the extended edges onto Edge Prime.


![Imgur](http://i.imgur.com/PYggEIq.gif)  

