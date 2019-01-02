package templates;

import jdk.nashorn.internal.parser.JSONParser;
import org.json.*;
import utils.LocPaths;
import utils.Logging;

import java.io.*;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.logging.Level;

public class Templates {

    public static List<ProjectTemplate> getAllProjectTemplates(){
        List<ProjectTemplate> templates = new ArrayList<>();

        Path jsonPath = LocPaths.getPathOfProjectFile(Paths.get("DenderQ/Templates/templates.json"));
        String jsonString = getJsonString(jsonPath);
        JSONObject json = new JSONObject(jsonString);
        Iterator<String> jsonKeys = json.keys();
        while(jsonKeys.hasNext()){
            String key = jsonKeys.next();
            Object keyObject = json.get(key);
            if (keyObject instanceof JSONObject){
                ProjectTemplate projectTemplate = new ProjectTemplate(key, (JSONObject) keyObject);
                templates.add(projectTemplate);
            }
        }
        return templates;
    }


    private static String getJsonString(Path filePath){
        StringBuilder jsonString = new StringBuilder();
        try {
            BufferedReader reader = new BufferedReader(new FileReader(filePath.toString()));

            String line;
            while((line = reader.readLine()) != null) {
                jsonString.append(line);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return jsonString.toString();
    }

}
