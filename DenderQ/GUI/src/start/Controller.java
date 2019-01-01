package start;

import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.control.TextField;
import javafx.scene.input.MouseEvent;
import javafx.fxml.Initializable;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URL;
import java.util.ResourceBundle;
import java.nio.file.Paths;
import java.nio.file.Path;
import ui.PythonCommunicator;

public class Controller{

    @FXML
    private Button btnCreateNewProject;
    private Button btnOpenProject;

    @FXML
    public void create_new_project(ActionEvent event){
        System.out.println("Pressed create new project");
        PythonCommunicator.createProject();
    }

    @FXML
    public void open_project(ActionEvent event){
        System.out.println("Pressed open_project");
    }
}