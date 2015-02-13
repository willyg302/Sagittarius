/**
 * Sagittarius - Java Starter Kit
 * Copyright WillyG Productions
 * @Authors: William Gaul
 */
package com.willyg.sagittarius;

import junit.framework.Test;
import junit.framework.TestCase;
import junit.framework.TestSuite;

public class SagittariusTest extends TestCase {
    public SagittariusTest(String testName) {
        super(testName);
    }

    public static Test suite() {
        return new TestSuite(SagittariusTest.class);
    }

    public void testSagittarius() {
        assertTrue(true);
    }
}
