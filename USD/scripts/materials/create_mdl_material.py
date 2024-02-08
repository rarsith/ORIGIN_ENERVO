from pxr import Sdf, UsdShade, Usd


stage: Usd.Stage = Usd.Stage.CreateInMemory()
root_layer: Sdf.Layer = stage.GetRootLayer()

mtl_path = Sdf.Path("/World/Looks/OmniPBR")
mtl = UsdShade.Material.Define(stage, mtl_path)
shader = UsdShade.Shader.Define(stage, mtl_path.AppendPath("Shader"))
shader.CreateImplementationSourceAttr(UsdShade.Tokens.sourceAsset)
# MDL shaders should use "mdl" sourceType
shader.SetSourceAsset("OmniPBR.mdl", "mdl")
shader.SetSourceAssetSubIdentifier("OmniPBR", "mdl")
# MDL materials should use "mdl" renderContext
mtl.CreateSurfaceOutput("mdl").ConnectToSource(shader.ConnectableAPI(), "out")
mtl.CreateDisplacementOutput("mdl").ConnectToSource(shader.ConnectableAPI(), "out")
mtl.CreateVolumeOutput("mdl").ConnectToSource(shader.ConnectableAPI(), "out")

