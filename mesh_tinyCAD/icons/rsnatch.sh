convert RENDERED_icons.png local01.miff
convert local01.miff -crop 32x32+0+0 VTX.png
convert local01.miff -crop 32x32+32+0 V2X.png
convert local01.miff -crop 32x32+64+0 XALL.png
convert local01.miff -crop 32x32+96+0 BIX.png
convert local01.miff -crop 32x32+128+0 PERP.png
convert local01.miff -crop 32x32+160+0 CCEN.png
convert local01.miff -crop 32x32+192+0 EXM.png
rm local01.miff