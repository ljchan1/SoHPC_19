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
      slice1.Crinkleslice = 0
      slice1.Triangulatetheslice = 1
      slice1.SliceOffsetValues = [0.0]

      # init the 'Plane' selected for 'SliceType'
      slice1.SliceType.Origin = [-0.6, -0.4, -0.19684969115002143]
      slice1.SliceType.Normal = [0.0, 0.0, 1.0]
      slice1.SliceType.Offset = 0.0

      sliceWriter1 = servermanager.writers.XMLMultiBlockDataWriter(Input=slice1)
      coprocessor.RegisterWriter(sliceWriter1, filename='threeslices1_%t.vtm', freq=2)

      #second slices
      slice2 = Slice(Input=region)
      slice2.SliceType = 'Plane'
      slice2.Crinkleslice = 0
      slice2.Triangulatetheslice = 1
      slice2.SliceOffsetValues = [0.0]

      # init the 'Plane' selected for 'SliceType'
      slice2.SliceType.Origin = [-0.6, -0.4, 0.0]
      slice2.SliceType.Normal = [0.0, 1.0, 0.0]
      slice2.SliceType.Offset = 0.0

      sliceWriter2 = servermanager.writers.XMLMultiBlockDataWriter(Input=slice2)
      coprocessor.RegisterWriter(sliceWriter2, filename='threeslices2_%t.vtm', freq=2)

      #third slices
      slice3 = Slice(Input=region)
      slice3.SliceType = 'Plane'
      slice3.Crinkleslice = 0
      slice3.Triangulatetheslice = 1
      slice3.SliceOffsetValues = [0.0]

      # init the 'Plane' selected for 'SliceType'
      slice3.SliceType.Origin = [-0.6, -0.4, 0.19754985715402515]
      slice3.SliceType.Normal = [0.0, 0.0, 1.0]
      slice3.SliceType.Offset = 0.0

      sliceWriter3 = servermanager.writers.XMLMultiBlockDataWriter(Input=slice3)
      coprocessor.RegisterWriter(sliceWriter3, filename='threeslices3_%t.vtm', freq=2)


      # ----------------------------------------------------------------
      # finally, restore active source
      # SetActiveSource(slice1)
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
