package scenes.create_project;

import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.CheckBox;
import javafx.scene.control.TextField;
import javafx.scene.input.InputMethodEvent;
import javafx.stage.DirectoryChooser;
import javafx.stage.Stage;
import scenes.Utils;
import ui.Output;
import ui.PythonCommunicator;
import utils.Logging;

import java.io.File;
import java.net.URL;
import java.util.ResourceBundle;
import java.nio.file.Paths;
import java.nio.file.Path;
import java.util.logging.Level;


public class Controller implements Initializable {

    private ResourceBundle bundle;
    private final String DEFAULT_PROJECT_NAME = "Project1";
    private final Path DEFAULT_DIR_START_PATH = Paths.get("E:\\Programmieren\\Java\\Tests"); //LocPaths.get(System.getProperty("user.home"));
    private final String DEFAULT_TEMPLATE_NAME = "default";

    private String currentProjectName = DEFAULT_PROJECT_NAME;
    private Path currentDirStartPath = DEFAULT_DIR_START_PATH;
    private Path currentProjectPath = Paths.get(currentDirStartPath.toString(), currentProjectName);

    private String currentTemplateName = DEFAULT_TEMPLATE_NAME;
    private boolean initWithGit = true;

    @FXML
    private TextField tfProjectPath;
    @FXML
    private TextField tfProjectName;
    @FXML
    private CheckBox cbInitWithGit;

    public void clickedShowDirChooser(ActionEvent event){
        System.out.println("Clicked show dir chooser");
        DirectoryChooser dirChooser = new DirectoryChooser();
        dirChooser.setTitle("DenderQ - Project location");
        dirChooser.setInitialDirectory(new File(DEFAULT_DIR_START_PATH.toString()));
        File selectedFolder = dirChooser.showDialog(Utils.getStageOfEvent(event));
        if(selectedFolder != null){
            currentDirStartPath = Paths.get(selectedFolder.toString());
            update_project_path();
        }
    }

    public void clickedCreateProject(ActionEvent event){
        Output out = PythonCommunicator.createProject(currentProjectPath.toString(), currentProjectName, currentTemplateName, initWithGit);
        if(!out.wasSuccessfull()){
            Logging.logger.log(Level.SEVERE, "Creating project failed!");
        }
    }

    @Override
    public void initialize(URL location, ResourceBundle resources) {
        this.bundle = resources;
        tfProjectName.setText(DEFAULT_PROJECT_NAME);
        update_project_path(DEFAULT_DIR_START_PATH.toString(), DEFAULT_PROJECT_NAME);
        tfProjectName.textProperty().addListener((observable, oldValue, newValue) -> {
            currentProjectName = newValue;
            update_project_path(currentDirStartPath.toString(), newValue);
        });
        cbInitWithGit.setSelected(initWithGit);
        cbInitWithGit.selectedProperty().addListener(((observable, oldValue, newValue) -> initWithGit = newValue));
    }

    private void update_project_path(){
        update_project_path(currentDirStartPath.toString(), currentProjectName);
    }

    private void update_project_path(String parentDir, String projectName){
        currentProjectPath = Paths.get(parentDir, projectName);
        tfProjectPath.setText(currentProjectPath.toString());
    }
}
