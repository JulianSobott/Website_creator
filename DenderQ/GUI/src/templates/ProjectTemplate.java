package templates;

import org.json.JSONObject;

public class ProjectTemplate extends Template {

    private final String name;
    private JSONObject jsonObject;

    ProjectTemplate(String name, JSONObject json){
        this.name = name;
        this.jsonObject = json;
    }

    public String getName() {
        return name;
    }
}
