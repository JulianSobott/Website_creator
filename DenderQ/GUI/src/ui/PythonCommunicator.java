package ui;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.file.Path;
import java.nio.file.Paths;

public class PythonCommunicator {

    private static Output call(String commands){
        String projectDir = System.getProperty("user.dir");
        String reqPath = "..\\req.py";
        Path absPath = Paths.get(projectDir, reqPath);
        ProcessBuilder pb = new ProcessBuilder("python", absPath.toString(), commands);
        Process process;
        Output output;

        int exitCode;
        try {
            process = pb.start();
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            BufferedReader errorOut = new BufferedReader(new InputStreamReader(process.getErrorStream()));

            String line;
            StringBuilder outString = new StringBuilder();
            StringBuilder errorString = new StringBuilder();
            while ( (line = reader.readLine()) != null) {
                outString.append(line).append(System.lineSeparator());
            }
            while ( (line = errorOut.readLine()) != null) {
                errorString.append(line).append(System.lineSeparator());
            }
            exitCode = process.exitValue();
            output = new Output(outString.toString(), errorString.toString(), exitCode);
        } catch (IOException e) {
            e.printStackTrace();
            output = new Output();
        }
        return output;
    }

    public static Output createProject(){
        String args = "?";
        Output out = PythonCommunicator.call(args);
        System.out.println(out.toFullString());
        return out;
    }
}
