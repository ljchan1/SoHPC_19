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

      # create a new 'Stream Tracer'
      streamTracer1 = StreamTracer(Input=region, SeedType='High Resolution Line Source')
      streamTracer1.Vectors = ['POINTS', 'U']
      streamTracer1.MaximumStreamlineLength = 9.199999809265137

      # init the 'High Resolution Line Source' selected for 'SeedType'
      streamTracer1.SeedType.Point1 = [-5.2, -0.8, 1.032]
      streamTracer1.SeedType.Point2 = [-5.2, 0.0, 1.032]
      streamTracer1.SeedType.Resolution = 60

      # create a new 'Tube'
      tube1 = Tube(Input=streamTracer1)
      tube1.Scalars = ['POINTS', 'p']
      tube1.Vectors = ['POINTS', 'U']
      tube1.Radius = 0.01


      tubeWriter1 = servermanager.writers.XMLPPolyDataWriter(Input=tube1)
      coprocessor.RegisterWriter(tubeWriter1, filename='streamline_top1_%t.vtm', freq=2)

      # create a new 'Stream Tracer'
      streamTracer2 = StreamTracer(Input=region, SeedType='High Resolution Line Source')
      streamTracer2.Vectors = ['POINTS', 'U']
      streamTracer2.MaximumStreamlineLength = 9.199999809265137

      # init the 'High Resolution Line Source' selected for 'SeedType'
      streamTracer2.SeedType.Point1 = [-5.2, -0.8, -1.032]
      streamTracer2.SeedType.Point2 = [-5.2, 0.0, -1.032]
      streamTracer2.SeedType.Resolution = 60

      # create a new 'Tube'
      tube2 = Tube(Input=streamTracer2)
      tube2.Scalars = ['POINTS', 'p']
      tube2.Vectors = ['POINTS', 'U']
      tube2.Radius = 0.01


      tubeWriter2 = servermanager.writers.XMLPPolyDataWriter(Input=tube2)
      coprocessor.RegisterWriter(tubeWriter2, filename='streamline_top2_%t.vtm', freq=2)

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
