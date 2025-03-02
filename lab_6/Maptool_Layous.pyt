import arcpy

class Toolbox:
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the .pyt file)."""
        self.label = "Toolbox"
        self.alias = "t"
        # List of tool classes associated with this toolbox
        self.tools = [GraduatedColorsRenderer]

class GraduatedColorsRenderer:
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "graduatedcolor"
        self.description = "create a graduated colored map based on a specific attribute of a layer"
        self.canRunInBackground = False
        self.category = "MapTools"

    def getParameterInfo(self):
        """Define the tool parameters."""
        #original project name
        param0 = arcpy.Parameter(
            displayName = "Input ArcGIS Pro Project Name",
            name = "aprxInputName",
            datatype = "DEFile",
            parameterType = "Required",
            direction = "Input"
        )
        #which layer you want to classify to create a color map
        param1 = arcpy.Parameter(
            displayName = "Layer to Classify",
            name = "LayertoClassify",
            datatype = "GPLayer",
            parameterType = "Required",
            direction = "Input"
        )
        #output folder location
        param2 = arcpy.Parameter(
            displayName = "Output Location",
            name = "OutputLocation",
            datatype = "DEFolder",
            parameterType = "Required",  #added parameter type
            direction = "Input"
        )
        #output project name
        param3 = arcpy.Parameter(
            displayName = "Output Project Name",
            name = "OutputProjectName",
            datatype = "GPString",
            parameterType = "Required",
            direction = "Input"
        )
        params = [param0, param1, param2, param3]
        return params

    def isLicensed(self):
        """Set whether the tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter. This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        # Define Progressor Variables
        readTime = 3 #the time for users to read the progress
        start = 0   #beginning position of the progressor
        max = 100   #end position
        step = 25   #the progress interval to move the progressor along

        #Setup Progressor
        import time #added
        arcpy.SetProgressor("step", "Validating Profile File...", start, max, step)
        time.sleep(readTime) #pause the execution for 3 seconds
        #Add message to the results name
        arcpy.AddMessage("Validating Project File...")
        #Project File
        project = arcpy.mp.ArcGISProject(parameters[0].valueAsText)

        #grabs the first instance of a map from the .aprx
        campus = project.listMaps('Map')[0] #access to the first map

        #Increment Progressor
        arcpy.SetProgressorPosition(start + step) #now is at 25%
        arcpy.SetProgressorLabel("Finding your map layer...")
        time.sleep(readTime)
        arcpy.AddMessage("Finding your map layer...")



        #Loop through the layers of the map
        for layer in campus.listLayers():
            #Check if the layer is a feature layer
            if layer.isFeatureLayer:
                #Copy the layer's symbology
                symbology = layer.symbology
                #Make sure the symbology has rederer attribute
                if hasattr(symbology, 'renderer'):
                    arcpy.AddMessage(f"Layer {layer.name} has a renderer: {type(symbology.renderer)}")

                    #Check layer name
                    if layer.name == parameters[1].valueAsText: #check if the layer name matches the input layer
                        arcpy.AddMessage(f"Found target layer: {layer.name}")
                        #Increment progressor
                        arcpy.SetProgressorPosition(start + step*2) #now is 50% completed
                        arcpy.SetProgressorLabel("Calculating and classifying...")
                        time.sleep(readTime)
                        arcpy.AddMessage("Calculating and classifying...")

                        #Update the copy's renderer to "graduated colors renderer"
                        symbology.updateRenderer('GraduatedColorsRenderer')

                        #Tell arcpy which field we want to base our chloropleth off of
                        symbology.renderer.classificationField = "Shape_Area"

                        #Increment progressor
                        arcpy.SetProgressorPosition(start + step*3) #now is 75% completed
                        arcpy.SetProgressorLabel("Cleaning Up...")
                        time.sleep(readTime)
                        arcpy.AddMessage("Cleaning Up...")

                        #Set how many classes we will have for the map
                        symbology.renderer.breakCount = 5

                        #Set color ramp
                        symbology.renderer.colorRamp = project.listColorRamps('Oranges (5 Classes)')[0]

                        #Set the layer's actual symbology equal to the copy's
                        layer.symbology = symbology

                        arcpy.AddMessage("Finish Generating Layer...")
                else:
                    print("No feature layers found")

        #Increment Progressor
        arcpy.SetProgressorPosition(start + step*4-1) #now is 99% completed
        arcpy.SetProgressorLabel("Saving...")
        time.sleep(readTime)
        arcpy.AddMessage("Saving...")

        project.saveACopy(parameters[2].valueAsText + "\\" + parameters[3].valueAsText + ".aprx")
        #Param2 is the folder location and Param3 is the name of the new project

        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
