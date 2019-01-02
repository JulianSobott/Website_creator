package scenes.startpage;

import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.fxml.Initializable;
import javafx.scene.Node;
import javafx.scene.Parent;
import javafx.scene.Scene;

import java.net.URL;
import java.util.ResourceBundle;
import java.util.logging.Level;
import java.util.logging.Logger;

import javafx.stage.Stage;
import scenes.Utils;
import start.Main;

public class Controller implements Initializable {

    private ResourceBundle bundle;

    @Override
    public void initialize(URL location, ResourceBundle resources) {
        this.bundle = resources;
    }

    @FXML
    public void create_new_project(ActionEvent event){
        System.out.println("Pressed create new project");
        Stage window = Utils.getStageOfEvent(event);
        Main.setScene(window, bundle, "/scenes/create_project/layout");
        //PythonCommunicator.createProject();
    }

    @FXML
    public void open_project(ActionEvent event){
        System.out.println("Pressed open_project");
    }


}