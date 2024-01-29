'''
Creates an asset file that consists of a top level layer and sublayers for
shading and geometry.
'''

from __future__ import print_function

import os
from pxr import Kind, Sdf, Usd, UsdGeom


def _CreateAsset(assetName, assetDir, assetKind, addShadingVariantLayer):
    assetFilePath = os.path.join(assetDir, '%s.usda' % assetName)

    print("Creating asset at %s" % assetFilePath)
    # Make the layer ascii - good for readability, plus the file is small
    rootLayer = Sdf.Layer.CreateNew(assetFilePath, args = {'format':'usda'})
    assetStage = Usd.Stage.Open(rootLayer)

    # Define a prim for the asset and make it the default for the stage.
    assetPrim = UsdGeom.Xform.Define(assetStage, '/%s' % assetName).GetPrim()
    assetStage.SetDefaultPrim(assetPrim)
    # Lets viewing applications know how to orient a free camera properly
    UsdGeom.SetStageUpAxis(assetStage, UsdGeom.Tokens.y)

    # Usually we will "loft up" the kind authored into the exported geometry
    # layer rather than re-stamping here; we'll leave that for a later
    # tutorial, and just be explicit here.
    model = Usd.ModelAPI(assetPrim)
    if assetKind:
        model.SetKind(assetKind)
    
    model.SetAssetName(assetName)
    model.SetAssetIdentifier('%s/%s.usda' % (assetName, assetName))
    
    refs = []
    if addShadingVariantLayer:
        # if we're going to add it, then shading is stronger than geom and needs
        # to be added first
        refs.append('./%s.shadingVariants.usda' % assetName)

    refs.append('./%s.maya.usda' % assetName)

    _CreateAndReferenceLayers(assetPrim, assetDir, refs)

    assetStage.GetRootLayer().Save()

def _CreateAndReferenceLayers(assetPrim, assetDir, refs):
    from pxr import Usd
    for refLayerPath in refs:
        referencedStage = Usd.Stage.CreateNew(os.path.join(assetDir, refLayerPath))
        referencedAssetPrim = referencedStage.DefinePrim(assetPrim.GetPath())
        referencedStage.SetDefaultPrim(referencedAssetPrim)
        referencedStage.GetRootLayer().Save()

        assetPrim.GetReferences().AddReference(refLayerPath)

    # If you want to print things out, you can do:
    #print(rootLayer.ExportToString())

if __name__ == '__main__':
    asset_name = "test_asset"
    asset_dir = "D:\\__SANDBOX\\USD"
    asset_kind = Kind.Tokens.component
    asset_shading_variant = True
    
    _CreateAsset(asset_name, asset_dir, asset_kind, asset_shading_variant)
    
    # main()
