package com.example.transformer;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;
import org.apache.commons.collections4.CollectionUtils;
import org.apache.commons.lang3.StringUtils;
import org.apache.commons.text.WordUtils;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;

public class Handler implements RequestHandler<Map<String, Object>, Map<String, Object>> {
    
    // Heavy static initialization - these could be lazy loaded
    private static final long startTime = System.nanoTime();
    private static final ObjectMapper mapper = new ObjectMapper();
    
    // Measure initialization time
    private static final double importTime = (System.nanoTime() - startTime) / 1_000_000_000.0;
    
    @Override
    public Map<String, Object> handleRequest(Map<String, Object> event, Context context) {
        try {
            // Extract input
            JsonNode data = mapper.valueToTree(event.get("data"));
            List<String> transformations = mapper.convertValue(
                event.get("transformations"),
                mapper.getTypeFactory().constructCollectionType(List.class, String.class)
            );
            
            if (data == null) {
                return Map.of(
                    "error", "No data provided",
                    "importTime", importTime
                );
            }
            
            // Apply transformations
            JsonNode transformed = transformData(data, transformations);
            
            return Map.of(
                "transformed", mapper.convertValue(transformed, Map.class),
                "importTime", importTime
            );
            
        } catch (Exception e) {
            return Map.of(
                "error", e.getMessage(),
                "importTime", importTime
            );
        }
    }
    
    private JsonNode transformData(JsonNode data, List<String> transformations) {
        if (transformations == null) {
            return data;
        }
        
        JsonNode result = data.deepCopy();
        
        for (String transform : transformations) {
            result = switch (transform.toLowerCase()) {
                case "uppercase" -> applyUppercase(result);
                case "reverse" -> applyReverse(result);
                default -> result;
            };
        }
        
        return result;
    }
    
    private JsonNode applyUppercase(JsonNode node) {
        if (node.isTextual()) {
            // Using Commons Lang3 when String.toUpperCase() would suffice
            return mapper.getNodeFactory().textNode(
                StringUtils.upperCase(node.asText())
            );
        } else if (node.isObject()) {
            ObjectNode obj = (ObjectNode) node;
            ObjectNode result = mapper.createObjectNode();
            obj.fields().forEachRemaining(entry ->
                result.set(entry.getKey(), applyUppercase(entry.getValue()))
            );
            return result;
        } else if (node.isArray()) {
            ArrayNode arr = (ArrayNode) node;
            ArrayNode result = mapper.createArrayNode();
            arr.forEach(element -> result.add(applyUppercase(element)));
            return result;
        }
        return node;
    }
    
    private JsonNode applyReverse(JsonNode node) {
        if (node.isTextual()) {
            // Using Commons Lang3 when StringBuilder.reverse() would suffice
            return mapper.getNodeFactory().textNode(
                StringUtils.reverse(node.asText())
            );
        } else if (node.isArray()) {
            // Using Commons Collections when ArrayList would suffice
            List<JsonNode> list = new ArrayList<>();
            node.forEach(list::add);
            CollectionUtils.reverseArray(list.toArray());
            
            ArrayNode result = mapper.createArrayNode();
            list.forEach(result::add);
            return result;
        } else if (node.isObject()) {
            ObjectNode obj = (ObjectNode) node;
            ObjectNode result = mapper.createObjectNode();
            obj.fields().forEachRemaining(entry ->
                result.set(entry.getKey(), applyReverse(entry.getValue()))
            );
            return result;
        }
        return node;
    }
}