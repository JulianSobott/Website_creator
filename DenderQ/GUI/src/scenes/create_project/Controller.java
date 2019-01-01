package scenes.create_project;

import javafx.event.ActionEvent;
import javafx.fxml.Initializable;
import javafx.stage.DirectoryChooser;
import javafx.stage.Stage;

import java.io.File;
import java.net.URL;
import java.util.ResourceBundle;

public class Controller implements Initializable {

    private ResourceBundle bundle;

    public void showDirChooser(ActionEvent event){
        System.out.println("Clicked show dir chooser");
        DirectoryChooser dirChooser = new DirectoryChooser();
        dirChooser.setTitle("DenderQ - Project location");
        //File selectedFolder = dirChooser.showDialog(getStageOfEvent(event));
        //tfProjectPath.setText(selectedFolder.toString());
    }

    @Override
    public void initialize(URL location, ResourceBundle resources) {
        this.bundle = resources;
    }
}
