"""
A Reference is a composition arc that enables users to aggregate layers or assets onto a Stage. A Reference targets a prim from a layer and loads it and all of its descendants into a new namespace within the referencing layer.
This snippet shows how to create and add a Reference to a prim.
A single prim can have multiple References.
"""

import omni.kit.commands
import omni.usd
from pxr import Usd, Sdf

def create_reference(usd_context: omni.usd.UsdContext, path_to: Sdf.Path, asset_path: str, prim_path: Sdf.Path) -> Usd.Prim:
    omni.kit.commands.execute("CreateReference",
        usd_context=usd_context,
        path_to=path_to, # Prim path for where to create the prim with the reference
        asset_path=asset_path, # The file path to reference. Relative paths are accepted too.
        prim_path=prim_path # OPTIONAL: Prim path to a prim in the referenced USD, if not provided the default prim is used
    )
    return usd_context.get_stage().GetPrimAtPath(path_to)


#############
# Full Usage
#############

# Get the USD context from kit
context: omni.usd.UsdContext = omni.usd.get_context()

# Create and add external reference to specific prim
ref_prim: Usd.Prim = create_reference(context, Sdf.Path("/World/ref_prim"), "C:/path/to/file.usd", Sdf.Path("/World/some/target"))

# Get the existing USD stage from kit
stage: Usd.Stage = context.get_stage()
usda = stage.GetRootLayer().ExportToString()
print(usda)

# Check that the reference prims were created
assert ref_prim.IsValid()

assert ref_prim.GetPrimStack()[0].referenceList.prependedItems[0] == Sdf.Reference(assetPath="file:/C:/path/to/file.usd", primPath=Sdf.Path("/World/some/target"))