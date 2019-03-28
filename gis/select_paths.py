import arcpy
import arcpy.management as mgmt
import arcpy.analysis as anlys
import re

from trs_path import expand_paths, abbrev_paths


#
# SelectPaths - Create a new selection from a list of TRS path specs
#

def selected_paths(paths, secs_lyr, subsecs_lyr, clear_selection):

    if clear_selection:
        mgmt.SelectLayerByAttribute(secs_lyr, 'CLEAR_SELECTION')
        mgmt.SelectLayerByAttribute(subsecs_lyr, 'CLEAR_SELECTION')

    # Get selected sections
    sec_paths = []
    if arcpy.Describe(secs_lyr).FIDSet:
        with arcpy.da.SearchCursor(secs_lyr, ['TRS_PATH']) as cur:
            sec_paths += [row[0] for row in cur]

    # Get selected subsections
    subsec_paths = []
    if arcpy.Describe(subsecs_lyr).FIDSet:
        with arcpy.da.SearchCursor(subsecs_lyr, ['TRS_PATH']) as cur:
            subsec_paths += [row[0] for row in cur]

    # Add in any TRS path specs from input parameter
    if paths:
        try:
            for path in expand_paths(re.split(';?\s+', paths.upper())):
                if path[-1].isdigit():
                    sec_paths.append(path)
                else:
                    subsec_paths.append(path)
        except ValueError as err:
            arcpy.AddError(err)
            return None

        if sec_paths:
            sql = '"TRS_PATH" IN (\'%s\')' % '\',\''.join(sec_paths)
            mgmt.SelectLayerByAttribute(secs_lyr, 'ADD_TO_SELECTION', where_clause=sql)

            # Expand full section paths into subsections
            expanded_sec_paths = expand_paths(sec + '.A-P' for sec in sec_paths)
            sql = '"TRS_PATH" IN (\'%s\')' % '\',\''.join(expanded_sec_paths)
            mgmt.SelectLayerByAttribute(subsecs_lyr, 'ADD_TO_SELECTION', where_clause=sql)

        if subsec_paths:
            sql = '"TRS_PATH" IN (\'%s\')' % '\',\''.join(subsec_paths)
            mgmt.SelectLayerByAttribute(subsecs_lyr, 'ADD_TO_SELECTION', where_clause=sql)

    # Add full section path for *.A-P and remove redundant full section paths
    subsec_paths = abbrev_paths(subsec_paths)
    for i in range(len(subsec_paths) - 1, -1, -1):
        sec = '.'.join(subsec_paths[i].split('.')[0:3])
        if subsec_paths[i].endswith('A-P'):
            # Convert to a full section path
            subsec_paths.pop(i)
            if sec not in sec_paths:
                sec_paths.append(sec)
        elif sec in sec_paths:
            # Remove redundant full section path
            sec_paths.remove(sec)
    subsec_paths = expand_paths(subsec_paths)

    paths = '; '.join(abbrev_paths(sec_paths + subsec_paths))

    return paths


class SelectedPaths(object):
    def __init__(self):
        self.label = "TRS Path Specs"
        self.description = "Create a TRS path spec from selected sections/subsections."
        self.category = None
        self.canRunInBackground = False

    def getParameterInfo(self):
        params = []

        # Input TRS path specs
        param = arcpy.Parameter(
            displayName='TRS Path Specs (optional)',
            name='paths',
            datatype='GPString',
            parameterType='Optional',
            direction='Input'
        )
        params.append(param)

        # Input sections feature layer
        param = arcpy.Parameter(
            displayName='Sections Layer',
            name='secs_fl',
            datatype='GPFeatureLayer',
            parameterType='Required',
            direction='Input',
            multiValue=False
        )
        param.value = 'BLM Sections'
        params.append(param)

        # Input subsections feature layer
        param = arcpy.Parameter(
            displayName='Subsections Layer',
            name='subsecs_fl',
            datatype='GPFeatureLayer',
            parameterType='Required',
            direction='Input',
            multiValue=False
        )
        param.value = 'BLM SubSections'
        params.append(param)

        # Input clear selection
        param = arcpy.Parameter(
            displayName='Clear Selection',
            name='clear_selection',
            datatype='GPBoolean',
            parameterType='Required',
            direction='Input',
            multiValue=False
        )
        param.value = False
        params.append(param)

        # Output TRS path spec
        param = arcpy.Parameter(
            displayName='Selected Paths',
            name='output_paths',
            datatype='GPString',
            parameterType='Derived',
            direction='Output'
        )
        params.append(param)

        return params

    def execute(self, params, messages):
        paths = params[0].valueAsText
        secs_lyr = params[1].valueAsText
        subsecs_lyr = params[2].valueAsText
        clear_selection = params[3].value

        paths = selected_paths(paths, secs_lyr, subsecs_lyr, clear_selection)

        arcpy.SetParameterAsText(4, paths)


if __name__ == '__main__':

    paths = arcpy.GetParameterAsText(0)
    secs_lyr = arcpy.GetParameterAsText(1)
    subsecs_lyr = arcpy.GetParameterAsText(3)
    clear_selection = arcpy.GetParameter(2)

    result = selected_paths(paths, secs_lyr, subsecs_lyr, clear_selection)
