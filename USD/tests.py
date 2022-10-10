from pxr import Usd

path_usd = r'C:\Users\arsithra\PycharmProjects\ORIGIN_ENERVO\USD\a_new_stage.usda'

stage = Usd.Stage.CreateNew(r'C:\Users\arsithra\PycharmProjects\ORIGIN_ENERVO\USD\a_new_stage02.usda')



stage = Usd.Stage.Open(path_usd)
# do something to the stage
# stage.Save()