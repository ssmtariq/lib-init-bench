package com.example.transformer;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.List;
import java.util.Map;

class HandlerTest {
    private final Handler handler = new Handler();
    
    @Test
    void testBasicTransformation() {
        Map<String, Object> input = Map.of(
            "data", Map.of(
                "text", "Hello World",
                "number", 42,
                "list", List.of(1, 2, 3)
            ),
            "transformations", List.of("uppercase", "reverse")
        );
        
        Map<String, Object> result = handler.handleRequest(input, null);
        
        assertNotNull(result);
        assertTrue(result.containsKey("transformed"));
        assertTrue(result.containsKey("importTime"));
        
        @SuppressWarnings("unchecked")
        Map<String, Object> transformed = (Map<String, Object>) result.get("transformed");
        assertEquals("DLROW OLLEH", transformed.get("text"));
        assertEquals(42, transformed.get("number"));
        
        @SuppressWarnings("unchecked")
        List<Integer> reversedList = (List<Integer>) transformed.get("list");
        assertEquals(List.of(3, 2, 1), reversedList);
    }
    
    @Test
    void testNoData() {
        Map<String, Object> input = Map.of(
            "transformations", List.of("uppercase")
        );
        
        Map<String, Object> result = handler.handleRequest(input, null);
        
        assertNotNull(result);
        assertTrue(result.containsKey("error"));
        assertTrue(result.containsKey("importTime"));
    }
    
    @Test
    void testNoTransformations() {
        Map<String, Object> input = Map.of(
            "data", Map.of("text", "Hello")
        );
        
        Map<String, Object> result = handler.handleRequest(input, null);
        
        assertNotNull(result);
        assertTrue(result.containsKey("transformed"));
        
        @SuppressWarnings("unchecked")
        Map<String, Object> transformed = (Map<String, Object>) result.get("transformed");
        assertEquals("Hello", transformed.get("text"));
    }
    
    @Test
    void testInvalidTransformation() {
        Map<String, Object> input = Map.of(
            "data", Map.of("text", "Hello"),
            "transformations", List.of("invalid")
        );
        
        Map<String, Object> result = handler.handleRequest(input, null);
        
        assertNotNull(result);
        assertTrue(result.containsKey("transformed"));
        
        @SuppressWarnings("unchecked")
        Map<String, Object> transformed = (Map<String, Object>) result.get("transformed");
        assertEquals("Hello", transformed.get("text"));
    }
}