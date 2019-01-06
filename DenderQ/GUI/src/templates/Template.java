package templates;

import org.json.JSONObject;

public class Template {

    private final String name;
    private JSONObject jsonObject;

    Template(String name, JSONObject json){
        this.name = name;
        this.jsonObject = json;
    }

    public String getName() {
        return name;
    }

    public JSONObject getJsonObject() {
        return jsonObject;
    }
}
