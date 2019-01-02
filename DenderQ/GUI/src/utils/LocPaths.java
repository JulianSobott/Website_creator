package utils;


import java.nio.file.Path;
import java.nio.file.Paths;

public class LocPaths {

    public static Path getProjectPath(){
        String guiDir = System.getProperty("user.dir");
        return Paths.get(guiDir, "..\\..").normalize();
    }
}
