from paraview.simple import *
from paraview import coprocessing


#--------------------------------------------------------------
# Code generated from cpstate.py to create the CoProcessor.
# paraview version 5.5.1

#--------------------------------------------------------------
# Global screenshot output options
imageFileNamePadding=0
rescale_lookuptable=False


# ----------------------- CoProcessor definition -----------------------

def CreateCoProcessor():
  def _CreatePipeline(coprocessor, datadescription):
    class Pipeline:
      # state file generated using paraview version 5.5.1

      # ----------------------------------------------------------------
      # setup the data processing pipelines
      # ----------------------------------------------------------------

      # trace generated using paraview version 5.5.1

      #### disable automatic camera reset on 'Show'
      # paraview.simple._DisableFirstRenderCameraReset()

      # create a new 'XML MultiBlock Data Reader'
      # create a producer from a simulation input
      region = coprocessor.CreateProducer(datadescription, 'region')

      # create a new 'Slice'
      slice1 = Slice(Input=region)
      slice1.SliceType = 'Plane'
      slice1.SliceOffsetValues = [0.0]

      # init the 'Plane' selected for 'SliceType'
      slice1.SliceType.Origin = [-0.5999999046325684, -0.40000000363215804, 0.0]
      slice1.SliceType.Normal = [0.0, 1.0, 0.0]

      # create a new 'Glyph'
      glyph1 = Glyph(Input=slice1, GlyphType='Arrow')
      glyph1.Scalars = ['POINTS', 'p']
      glyph1.Vectors = ['POINTS', 'U']
      glyph1.ScaleFactor = 0.5
      glyph1.MaximumNumberOfSamplePoints = 4000
      glyph1.GlyphTransform = 'Transform2'

      # init the 'Arrow' selected for 'GlyphType'
      glyph1.GlyphType.TipRadius = 0.05
      glyph1.GlyphType.TipLength = 0.1
      glyph1.GlyphType.ShaftRadius = 0.008

      glyphWriter1 = servermanager.writers.XMLMultiBlockDataWriter(Input=glyph1)
      coprocessor.RegisterWriter(glyphWriter1, filename='glyph_front_%t.vtm', freq=2)

      # ----------------------------------------------------------------
      # finally, restore active source
      # SetActiveSource(glyph1)
      # SetActiveSource(slice2)
      # ----------------------------------------------------------------
    return Pipeline()

  class CoProcessor(coprocessing.CoProcessor):
    def CreatePipeline(self, datadescription):
      self.Pipeline = _CreatePipeline(self, datadescription)

  coprocessor = CoProcessor()
  # these are the frequencies at which the coprocessor updates.
  freqs = {'region': []}
  coprocessor.SetUpdateFrequencies(freqs)
  return coprocessor


#--------------------------------------------------------------
# Global variable that will hold the pipeline for each timestep
# Creating the CoProcessor object, doesn't actually create the ParaView pipeline.
# It will be automatically setup when coprocessor.UpdateProducers() is called the
# first time.
coprocessor = CreateCoProcessor()

#--------------------------------------------------------------
# Enable Live-Visualizaton with ParaView and the update frequency
coprocessor.EnableLiveVisualization(True)

# ---------------------- Data Selection method ----------------------

def RequestDataDescription(datadescription):
    "Callback to populate the request for current timestep"
    global coprocessor
    if datadescription.GetForceOutput() == True:
        # We are just going to request all fields and meshes from the simulation
        # code/adaptor.
        for i in range(datadescription.GetNumberOfInputDescriptions()):
            datadescription.GetInputDescription(i).AllFieldsOn()
            datadescription.GetInputDescription(i).GenerateMeshOn()
        return

    # setup requests for all inputs based on the requirements of the
    # pipeline.
    coprocessor.LoadRequestedData(datadescription)

# ------------------------ Processing method ------------------------

def DoCoProcessing(datadescription):
    "Callback to do co-processing for current timestep"
    global coprocessor

    # Update the coprocessor by providing it the newly generated simulation data.
    # If the pipeline hasn't been setup yet, this will setup the pipeline.
    coprocessor.UpdateProducers(datadescription)

    # Write output data, if appropriate.
    coprocessor.WriteData(datadescription);

    # Write image capture (Last arg: rescale lookup table), if appropriate.
    coprocessor.WriteImages(datadescription, rescale_lookuptable=rescale_lookuptable, image_quality=0, padding_amount=imageFileNamePadding)

    # Live Visualization, if enabled.
    coprocessor.DoLiveVisualization(datadescription, "localhost", 22222)
