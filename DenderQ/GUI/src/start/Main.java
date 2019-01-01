package start;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.layout.*;
import javafx.stage.Stage;

import java.util.Locale;
import java.util.ResourceBundle;

import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.Logger;

public class Main extends Application {

    public static void main(String[] args) {
        launch(args);
    }


    @Override
    public void start(Stage primaryStage) {
        try {
            ResourceBundle bundle = ResourceBundle.getBundle("bundles.lang", new Locale("en", "US"));
            Parent root = FXMLLoader.load(Main.class.getResource("start_page.fxml"), bundle);
            primaryStage.setScene(new Scene(root, 800, 600));
            primaryStage.setTitle(bundle.getString("application.title"));
            primaryStage.show();
        } catch (Exception ex) {
            Logger.getLogger(Main.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
}
