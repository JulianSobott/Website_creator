package scenes.create_project;

import javafx.collections.ObservableList;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.geometry.Insets;
import javafx.scene.control.*;
import javafx.scene.layout.VBox;
import javafx.stage.DirectoryChooser;
import scenes.Utils;
import templates.ProjectTemplate;
import templates.Template;
import ui.Output;
import ui.PythonCommunicator;
import utils.Logging;
import templates.Templates;

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
    @FXML
    private VBox vbTemplatesContainer;
    private ToggleGroup groupTemplates;

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
        currentTemplateName = ((RadioButton)groupTemplates.getSelectedToggle()).getText();
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
        createTemplatesSection();
    }

    private void update_project_path(){
        update_project_path(currentDirStartPath.toString(), currentProjectName);
    }

    private void update_project_path(String parentDir, String projectName){
        currentProjectPath = Paths.get(parentDir, projectName);
        tfProjectPath.setText(currentProjectPath.toString());
    }

    private void createTemplatesSection(){
        groupTemplates = new ToggleGroup();
        for(ProjectTemplate template : Templates.getAllProjectTemplates()){
            RadioButton rbTemplate = new RadioButton();
            rbTemplate.setText(template.getName());
            rbTemplate.setToggleGroup(groupTemplates);
            VBox.setMargin(rbTemplate, new Insets(10, 0, 0, 20));
            vbTemplatesContainer.getChildren().add(rbTemplate);
        }
        ObservableList<Toggle> addedButtons = groupTemplates.getToggles();
        if (!addedButtons.isEmpty()) {
            groupTemplates.selectToggle(addedButtons.get(0));
        }
    }
}
