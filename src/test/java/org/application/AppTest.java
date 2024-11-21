package org.application;

import junit.framework.Test;
import junit.framework.TestCase;
import junit.framework.TestSuite;

import java.io.IOException;
import java.util.ArrayList;

/**
 * Unit test for simple App.
 */
public class AppTest
        extends TestCase {

    /**
     * Create the test case
     *
     * @param testName name of the test case
     */
    public AppTest(String testName) {
        super(testName);
    }


    /**
     * @return the suite of tests being tested
     */
    public static Test suite() {
        return new TestSuite(AppTest.class);
    }

    /**
     * Rigourous Test :-)
     */
    public void testApp() {
        try {
            ArrayList<double[]> coordinateList = App.extractCoordinates("./outputs/polygons_tpo_750.json", 100);
            coordinateList.forEach(c -> System.out.println(c[0] + " " + c[1]));
        } catch (IOException e) {
            fail();
            throw new RuntimeException(e);
        }
        assertTrue(true);
    }
}
