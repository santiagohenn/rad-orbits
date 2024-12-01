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

import java.io.*;
import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

public class App {

    public static void main(String[] args) {



    }

    public void ssrgt() {

        String configurationsPath = "./inputs/config.rad.orbits.properties";
        String outputPath = "./outputs/analysis/";

        List<double[]> SAA;
        try {
            SAA = App.extractCoordinates("./outputs/polygons_tpo_750.json", 100);
        } catch (IOException e) {
            Log.error("Error trying to load polygon: " + e.getMessage());
            throw new RuntimeException(e);
        }

        List<Satellite> allSsRgt = satellitesFromFile("./inputs/ssrgt_1030.csv");
        RegionAccessComputer regionAccessComputer = new RegionAccessComputer(configurationsPath);

        LinkedList<Satellite> currentSsRgt = new LinkedList<>();

        for (Satellite sat : allSsRgt) {
            currentSsRgt.clear();
            currentSsRgt.add(sat);
            regionAccessComputer.setSatelliteList(currentSsRgt);
            regionAccessComputer.setROI(SAA);
            regionAccessComputer.computeROIAccess();
        }



        for (int inc = 45; inc < 100; inc++) {
            Log.info("Running constellation coverage over SAA ... inc: " + inc + " degrees");
            regionAccessComputer.setOutputPath(outputPath);
            regionAccessComputer.getSatelliteList().get(0).getElements().setInclination(inc);
//        regionAccessComputer.setSatelliteList(satelliteList);
            regionAccessComputer.setROI(SAA);
            regionAccessComputer.computeROIAccess();
            Log.info("... done!");
        }

    }

    public void sweepInc() {

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
        RegionAccessComputer regionAccessComputer = new RegionAccessComputer(configurationsPath);
        for (int inc = 45; inc < 100; inc++) {
            Log.info("Running constellation coverage over SAA ... inc: " + inc + " degrees");
            regionAccessComputer.setOutputPath(outputPath);
            regionAccessComputer.getSatelliteList().get(0).getElements().setInclination(inc);
//        regionAccessComputer.setSatelliteList(satelliteList);
            regionAccessComputer.setROI(SAA);
            regionAccessComputer.computeROIAccess();
            Log.info("... done!");
        }

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

    public static List<Satellite> satellitesFromFile(String fileName) {
        List<Satellite> satelliteList = new ArrayList();
        File file = new File(fileName);

        try (
                FileReader fr = new FileReader(file);
                BufferedReader br = new BufferedReader(fr);
        ) {
            int id = 0;

            String line;
            while((line = br.readLine()) != null) {
                if (!line.startsWith("//") && line.length() > 0) {
                    String[] data = line.split(",");
                    satelliteList.add(new Satellite(id++, data[0], Double.parseDouble(data[1]), Double.parseDouble(data[2]), Double.parseDouble(data[3]), Double.parseDouble(data[4]), Double.parseDouble(data[5]), Double.parseDouble(data[6])));
                }
            }
        } catch (FileNotFoundException e) {
            Log.warn("Unable to find file: " + fileName);
            e.printStackTrace();
        } catch (IOException e) {
            Log.error("IOException: " + fileName);
            e.printStackTrace();
        }

        return satelliteList;
    }


}
