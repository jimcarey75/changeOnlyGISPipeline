# Publishes a service
# Catalog window of ArcMap before running this script
import arcpy, os, sys, logging

log_file = "C:/scripts/logs/Publish_logfile.txt"
logging.basicConfig(filename=log_file, level=logging.INFO)

# Define local variables
wrkspc = 'C:/scripts/MXDs'
extension = ".mxd"

# Get all mxds in workspace     
for f in os.listdir(wrkspc):
    if f.endswith(extension):
        logging.info(f.rstrip('\n'))
        MXD = 'C:/scripts/MXDs/' + f.rstrip('\n')
        mapDoc = arcpy.mapping.MapDocument(MXD)

# Provide path to connection file
con = wrkspc + '/MSPXAGSDEV.ags'

# Provide other service details
service = mapDoc.filePath.lstrip('C:/scripts/MXDs/')
servicename = service.rstrip('.mxd')
servicename = service[:-4]
folder = 'JC_MAPS' 
sddraft = wrkspc + '/' + servicename + '.sddraft'
sd = wrkspc + '/' + servicename + '.sd'
summary = 'Jim Test'
tags = 'UK'
outputFile = wrkspc + '/' + servicename + '_log.txt'

# Create service definition draft
arcpy.mapping.CreateMapSDDraft(mapDoc, sddraft, servicename, 'ARCGIS_SERVER', con, True, folder, summary, tags)

# Analyze the service definition draft
analysis = arcpy.mapping.AnalyzeForSD(sddraft)

# Stage and upload the service if the sddraft analysis did not contain errors
if analysis['errors'] == {}:
# Execute StageService. This creates the service definition.
    arcpy.StageService_server(sddraft, sd)
# Execute UploadServiceDefinition. This uploads the service definition and publishes the service.
    arcpy.UploadServiceDefinition_server(sd, con)
    logging.info ("Service successfully published")
else: 
    logging.info ("Service could not be published because errors were found during analysis.")
logging.info( arcpy.GetMessages())
    
# Logging.info( errors, warnings, and messages returned from the analysis
def logFile():
    logging.info( "The following information was returned during analysis of the MXD:")
    for key in ('messages', 'warnings', 'errors'):
      logging.info( '----' + key.upper() + '---')
      vars = analysis[key]
      for ((message, code), layerlist) in vars.iteritems():
        logging.info( '    ', message, ' (CODE %i)' % code)
        logging.info( '       applies to:',)
        for layer in layerlist:
            logging.info( layer.name,)
        


