package ui;

import java.io.*;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Formatter;
import java.util.List;
import java.util.logging.Level;


public class PythonCommunicator {


    private static Output call(String commands){
        String projectDir = System.getProperty("user.dir");
        String reqPath = "..\\req.py";
        Path absPath = Paths.get(projectDir, reqPath);
        List<String> args = new ArrayList<String>();
        args.add("python");
        args.add(absPath.toString());
        args.addAll(Arrays.asList(commands.split("\\s+")));

        ProcessBuilder pb = new ProcessBuilder(args);
        Logging.logger.log(Level.INFO, args.toString());
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
                System.out.println(line);
            }
            while ( (line = errorOut.readLine()) != null) {
                errorString.append(line).append(System.lineSeparator());
                System.out.println(line);
            }
            exitCode = process.exitValue();
            output = new Output(outString.toString(), errorString.toString(), exitCode);
        } catch (IOException e) {
            e.printStackTrace();
            output = new Output();
        }
        return output;
    }

    public static Output createProject(String fullProjectPath, String projectName, String templateName){
        StringBuilder args = new StringBuilder();
        Formatter formatter = new Formatter(args);
        formatter.format("init name=\"%s\" template=\"%s\" root=\"%s\"", projectName, templateName, fullProjectPath);
        Output out = PythonCommunicator.call(args.toString());
        System.out.println(out.toFullString());
        return out;
    }
}
