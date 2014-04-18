Blender CAD utils
=================

A tiny subset of unmissable CAD functions for Blender 3d.
Addon [page on blender.org/wiki](http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Modeling/mesh_tinyCAD) (Wich has most of the same info)

### OK, what's this all about?

Dedicated CAD software speeds up drafting significantly with functions like: `Extend`, `Trim`,  `Intersect`, `Fillet /w radius` and `Offset /w distance`. At the moment of this writing many of these functions aren't included by default in regular distributions on Blender.org, so i've coded scripts to perform a few of the main features that I missed most. 
  
My scripts have shortnames: `VTX, EXM, V2X, XALL, BIX` and are described separately in sections below. `Fillet` and `Offset` are written by zmj100 and can be found [here](http://blenderartists.org/forum/showthread.php?179375).
  

### VTX

The VTX script has lived in contrib distributions of Blender since 2010, with relatively minor changes. The feedback from BlenderArtists has been [overwhelmingly positive](http://blenderartists.org/forum/showthread.php?204836-CAD-Addon-Edge-Tools-(blender-2-6x)). I'm not going to claim it's bug free, but finding any showstopping issues has proven difficult. It now performs V, T or X selection automatically.   
  
Expect full freedom of orientation, but stuff must really intersect within error margins (`1.5E-6` = tolerance). These kinds of functions are handy for drawing construction lines and fixing up geometry. 

  - V : extending two edges towards their _calculated_ intersection point.  
   ![V](http://i.imgur.com/zBSciFf.png)

  - T : extending the path of one edge towards another edge.  
   ![T](http://i.imgur.com/CDH5oHm.png)

  - X : two edges intersect, their intersection gets a weld vertex. You now have 4 edges and 5 vertices.  
   ![X](http://i.imgur.com/kqtX9OE.png)


- Select two edges  
- hit `Spacebar` and type `vtx` ..select `autoVTX`  
- Bam. the rest is taken care of.


### X ALL

Intersect all, it programatically goes through all selected edges and slices them all using any found intersections, then welds them.

  - XALL is fast!  
  ![Imgur](http://i.imgur.com/1I7totI.gif)
  - Select as many edges as you want to intersect.
  - hit `spacebar` and type `xa`  ..select `XALL intersect all edges`

### V2X (Vertex to Intersection)

This might be a niche accessory, but sometimes all you want is a vertex positioned on the intersection of two edges. Nothing fancy.

### EXM (Extend Multiples)

It has two modes.  
  -  Pick an edge (we'll call this Edge Prime)
  -  make sure only one edge is selected
  -  Run `EXM extend multiple edges` from spacebar menu
  -  Your picked edge has turned light blue
  -  Pick edges to extend towards that edge
  -  If edges are picked that don't intersect in 3d space (within tolerance) then those edges are not added
  -  Edges that do intersect will be shown in a different colour with the extended part in yet another colour
  -  You can unpick edges by clicking on them
  -  To finalize the operation:  
    - Press `Comma` to extend the edges using the vertex closest to the intersection point by moving the vertex closest to the edge being extended towards.
    - Press `Period` to create a new edge attached to the original geometry.
  -  This addon does not weld the extended edges onto Edge Prime.


![Imgur](http://i.imgur.com/WRD0prj.gif)  

### BIX (generate Bisector)

Creates a single edge which is the bisect of two edges.  
![Imgur](http://i.imgur.com/uzyv1Mv.gif)  
  
### Trim Multiples

Explained in the issue tracker with moving GIF: [issue3](https://github.com/zeffii/Blender_CAD_utils/issues/3)


### Why on github?

The issue tracker, use it.  

-  Let me know if these things are broken in new releases. Why? I don't update Blender as often as some so am oblivious to the slow evolution. 
-  If you can make a valid argument for extra functionality and it seems like something I might use or be able to implement for fun, it's going to happen.
-  I'm always open to pull requests (just don't expect instant approval of something massive, we can talk..you can use your gift of persuasion and sharp objectivism)
