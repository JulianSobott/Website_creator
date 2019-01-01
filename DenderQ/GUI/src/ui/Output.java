package ui;

public class Output {
    private String output;
    private String errors;
    private int exitCode;
    Output(String output, String errors, int exitCode){
        this.output = output;
        this.errors = errors;
        this.exitCode = exitCode;
    }
    Output(){
        this.output = "";
        this.errors = "";
        this.exitCode = -1;
    }

    public String toString(){
        return Integer.toString(this.exitCode);
    }

    String toFullString(){
        String str = "ExitCode: " + this.exitCode + "\n";
        str += "Output: " + this.output + "\n";
        str += "Errors: " + this.errors + "\n";
        return str;
    }
}
