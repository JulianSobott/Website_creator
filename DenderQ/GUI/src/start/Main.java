package start;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;


import java.util.Locale;
import java.util.ResourceBundle;
import java.util.logging.Level;
import java.util.logging.Logger;


public class Main extends Application {

    private Stage window;
    private ResourceBundle bundle;

    public static void main(String[] args) {
        launch(args);
    }


    @Override
    public void start(Stage primaryStage) {
        window = primaryStage;
        bundle = ResourceBundle.getBundle("bundles.lang", new Locale("en", "US"));
        window.setTitle(bundle.getString("application.title"));
        Parent root;
        //Controller controller = new Controller(window, bundle);
        window.show();
        Main.setScene(window, bundle, "/scenes/startpage/layout");
    }

    public static void setScene(Stage window, ResourceBundle bundle, String resourceName){
        Parent root;
        try {
            root = FXMLLoader.load(Main.class.getResource(resourceName + ".fxml"), bundle);
            window.setScene(new Scene(root, 800, 600));
        } catch (Exception ex) {
            Logger.getLogger(Main.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

}
