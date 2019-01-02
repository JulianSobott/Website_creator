package scenes;

import javafx.event.ActionEvent;
import javafx.scene.Node;
import javafx.stage.Stage;

public class Utils {

    public static Stage getStageOfEvent(ActionEvent event){
        return (Stage)((Node)event.getSource()).getScene().getWindow();
    }
}
