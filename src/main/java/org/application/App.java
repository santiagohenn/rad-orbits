package org.application;

import constellation.tools.ConstellationCoverageComputer;
import constellation.tools.geometry.GeographicTools;
import constellation.tools.utilities.FileUtils;
import satellite.tools.assets.entities.Satellite;
import satellite.tools.utils.Log;

import java.util.ArrayList;
import java.util.List;

public class App {
    public static void main(String[] args) {

        String configurationsPath = "";
        String outputPath = "";

        FileUtils fileUtils = new FileUtils(outputPath);
        GeographicTools geographicTools = new GeographicTools();

        List<Satellite> satelliteList = new ArrayList<>();

        Log.info("Running constellation coverage over SAA ... ");
        ConstellationCoverageComputer constellationCoverageComputer = new ConstellationCoverageComputer(configurationsPath);

        List<double[]> SAA = fileUtils.file2DoubleList("");
        double roiSurface = geographicTools.computeNonEuclideanSurface(SAA);

        constellationCoverageComputer.setOutputPath(outputPath);
        constellationCoverageComputer.setSatelliteList(satelliteList);
        constellationCoverageComputer.setROI(SAA);
        constellationCoverageComputer.run();
        Log.info("... done!");

    }

}
