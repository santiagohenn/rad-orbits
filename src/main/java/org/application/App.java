package org.application;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import constellation.tools.ConstellationCoverageComputer;
import constellation.tools.RegionAccessComputer;
import constellation.tools.geometry.GeographicTools;
import constellation.tools.utilities.FileUtils;
import satellite.tools.assets.entities.Satellite;
import satellite.tools.utils.Log;

import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class App {

    public static void main(String[] args) {

        String configurationsPath = "./inputs/config.rad.orbits.properties";
        String outputPath = "./outputs/analysis/";

//        GeographicTools geographicTools = new GeographicTools();

//        List<Satellite> satelliteList = new ArrayList<>();

//        ConstellationCoverageComputer constellationCoverageComputer = new ConstellationCoverageComputer(configurationsPath);


//        List<double[]> SAA = fileUtils.file2DoubleList("");
        List<double[]> SAA;
        try {
            SAA = App.extractCoordinates("./outputs/polygons_tpo_750.json", 100);
        } catch (IOException e) {
            Log.error("Error trying to load polygon: " + e.getMessage());
            throw new RuntimeException(e);
        }

//        double roiSurface = geographicTools.computeNonEuclideanSurface(SAA);

        Log.info("Running constellation coverage over SAA ... ");
        RegionAccessComputer regionAccessComputer = new RegionAccessComputer(configurationsPath);
        regionAccessComputer.setOutputPath(outputPath);
//        regionAccessComputer.setSatelliteList(satelliteList);
        regionAccessComputer.setROI(SAA);
        regionAccessComputer.computeROIAccess();
        Log.info("... done!");

    }

    public static ArrayList<double[]> extractCoordinates(String filePath, double requiredLevel) throws IOException {

        // Initialize the list to store coordinates
        ArrayList<double[]> coordinatesList = new ArrayList<>();

        // Parse the JSON file
        try (FileReader reader = new FileReader(filePath)) {
            JsonArray root = JsonParser.parseReader(reader).getAsJsonArray();

            // Iterate over the JSON array
            for (JsonElement element : root) {
                JsonObject polygonObject = element.getAsJsonObject();

                // Check if the "level" matches the required value
                if (polygonObject.has("level") && polygonObject.get("level").getAsDouble() == requiredLevel) {
                    // Navigate to the "geometry" -> "coordinates" array
                    JsonObject geometry = polygonObject.getAsJsonObject("geometry");
                    JsonArray coordinates = geometry.getAsJsonArray("coordinates");

                    // Extract the outer ring (first array in the coordinates)
                    if (!coordinates.isEmpty()) {
                        JsonArray outerRing = coordinates.get(0).getAsJsonArray();

                        // Iterate through the coordinate pairs in the outer ring
                        for (JsonElement coordinatePair : outerRing) {
                            JsonArray pair = coordinatePair.getAsJsonArray();
                            double longitude = pair.get(0).getAsDouble();
                            double latitude = pair.get(1).getAsDouble();
                            coordinatesList.add(new double[]{longitude, latitude});
                        }
                    }
                }
            }
        }

        return coordinatesList;
    }


}
