package scenes.create_project;

import javafx.collections.ObservableList;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.event.EventType;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.geometry.Insets;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.layout.AnchorPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;
import javafx.scene.text.Font;
import javafx.stage.DirectoryChooser;
import javafx.stage.Popup;
import javafx.stage.Stage;
import org.json.JSONObject;
import scenes.Utils;
import templates.ProjectTemplate;
import templates.Template;
import ui.Output;
import ui.PythonCommunicator;
import utils.Logging;
import templates.Templates;

import java.io.File;
import java.net.URL;
import java.util.Iterator;
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
    @FXML
    private AnchorPane anchorPane;
    private Stage window;

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

        anchorPane.sceneProperty().addListener((observable, oldScene, newScene) -> {
            if (oldScene == null && newScene != null) {
                // scene is set for the first time. Now its the time to listen stage changes.
                newScene.windowProperty().addListener((observableWindow, oldWindow, newWindow) -> {
                    if (oldWindow == null && newWindow != null) {
                        // stage is set. now is the right time to do whatever we need to the stage in the controller.
                        window = (Stage)newWindow;
                    }
                });
            }
        });
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
            HBox hbTemplateContainer = new HBox();
            RadioButton rbTemplate = new RadioButton();
            rbTemplate.setText(template.getName());
            rbTemplate.setToggleGroup(groupTemplates);
            HBox.setMargin(rbTemplate, new Insets(10, 0, 0, 20));

            Button btnTemplateStructure = new Button();
            btnTemplateStructure.setOnAction(event -> showTemplateStructure(template));
            Image imgShowTemplateStructure = new Image(getClass().getResourceAsStream("/info_black_18dp.png"));
            btnTemplateStructure.setGraphic(new ImageView(imgShowTemplateStructure));
            btnTemplateStructure.getStyleClass().add("btnTemplateStructure");
            HBox.setMargin(btnTemplateStructure, new Insets(10, 0, 0, 9));

            hbTemplateContainer.getChildren().addAll(rbTemplate, btnTemplateStructure);
            vbTemplatesContainer.getChildren().add(hbTemplateContainer);
        }
        ObservableList<Toggle> addedButtons = groupTemplates.getToggles();
        if (!addedButtons.isEmpty()) {
            groupTemplates.selectToggle(addedButtons.get(0));
        }
    }

    private void showTemplateStructure(Template template){
        Stage stPopupTemplate = new Stage();

        VBox vbStructureContainer = new VBox();
        vbStructureContainer.getChildren().add(getVBoxOfTemplate(template.getName(), template.getJsonObject(), 0));

        vbStructureContainer.getStylesheets().add("scenes/create_project/create_project.css");
        vbStructureContainer.getStyleClass().add("vbStructureContainer");

        Scene scPopupTemplate = new Scene(vbStructureContainer);
        stPopupTemplate.setScene(scPopupTemplate);
        stPopupTemplate.show();
    }

    private VBox getVBoxOfTemplate(String name, JSONObject values, int level){
        int indention = 20;
        VBox vbTemplate = new VBox();

        Label lblTemplateLine = new Label(name);
        VBox.setMargin(lblTemplateLine, new Insets(2, 0, 2, indention * level));

        vbTemplate.getChildren().add(lblTemplateLine);

        Iterator<String> jsonKeys = values.keys();
        while(jsonKeys.hasNext()){
            String key = jsonKeys.next();

            Object keyObject = values.get(key);
            if (keyObject instanceof JSONObject){
                vbTemplate.getChildren().add(getVBoxOfTemplate(key, (JSONObject)keyObject, level + 1));
            }else if(keyObject instanceof String){
                Label lblInnerTemplateLine = new Label(key);
                VBox.setMargin(lblInnerTemplateLine, new Insets(2, 0, 2, indention * (level + 1)));
                vbTemplate.getChildren().add(lblInnerTemplateLine);
            }
        }
        return vbTemplate;
    }
}
